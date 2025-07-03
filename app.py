import streamlit as st
import pandas as pd
import psycopg2
import os
from datetime import datetime

# Get DB URL from environment variable (Render will set this)
DB_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
@st.cache_resource
def get_connection():
    return psycopg2.connect(DB_URL)

conn = get_connection()
cursor = conn.cursor()

# Initialize table if it doesn't exist
def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE,
            name TEXT,
            amount FLOAT,
            category TEXT
        );
    """)
    conn.commit()

init_db()

# Save new expense
def save_data(date, name, amount, category):
    cursor.execute("""
        INSERT INTO expenses (date, name, amount, category)
        VALUES (%s, %s, %s, %s);
    """, (date, name, amount, category))
    conn.commit()

# Load all expenses
def load_data():
    cursor.execute("SELECT date, name, amount, category FROM expenses ORDER BY date DESC;")
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["Date", "Expense Name", "Amount", "Category"])

# ========== Streamlit UI ==========

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("📒 Expense Tracker")

# Input Form
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=datetime.today())
        name = st.text_input("Expense Name")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        category = st.selectbox("Category", ["Food", "Entertainment", "College"])

    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if not name.strip():
            st.warning("⚠️ Please enter an expense name.")
        elif amount <= 0:
            st.warning("⚠️ Please enter an amount greater than 0.")
        else:
            save_data(date, name, amount, category)
            st.success("✅ Expense added!")

# Load and Display
st.subheader("📋 All Expenses")
df = load_data()
st.dataframe(df, use_container_width=True)

# Filter by Date + Category
st.subheader("📅 Filter by Date Range and Category")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=df["Date"].min())
    with col2:
        end_date = st.date_input("End Date", value=df["Date"].max())

    category_options = ["All"] + sorted(df["Category"].dropna().unique())
    selected_category = st.selectbox("Filter by Category", category_options)

    if start_date > end_date:
        st.error("🚫 Start date must be before end date.")
    else:
        filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]

        st.write(f"Showing expenses from {start_date} to {end_date}")
        st.dataframe(filtered_df, use_container_width=True)

        # Total and average
        total = filtered_df["Amount"].sum()
        days = (end_date - start_date).days + 1
        average = total / days if days > 0 else 0
        st.success(f"💵 Total Spent: ₹{total:,.2f}")
        st.info(f"📊 Average Daily Spending: ₹{average:,.2f}")
else:
    st.info("No expenses found.")
