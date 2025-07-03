import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === Configuration ===
EXCEL_FILE = 'expenses.xlsx'
COLUMNS = ["Date", "Expense Name", "Amount", "Category"]

# === Initialize Excel File ===
def initialize_excel():
    if not os.path.exists(EXCEL_FILE) or os.path.getsize(EXCEL_FILE) == 0:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(EXCEL_FILE, index=False)

initialize_excel()

# === Load & Save Data ===
def load_data():
    return pd.read_excel(EXCEL_FILE)

def save_data(date, name, amount, category):
    df = load_data()
    new_entry = {
        "Date": date,
        "Expense Name": name,
        "Amount": amount,
        "Category": category
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

# === Page Setup ===
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("📒 Expense Tracker")

# === Expense Entry Form ===
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
            st.warning("⚠️ Please enter a valid amount greater than 0.")
        elif not category:
            st.warning("⚠️ Please select a category.")
        else:
            save_data(date, name, amount, category)
            st.success("✅ Expense added!")

# === Load and Show All Data ===
st.subheader("📋 All Expenses")
df = load_data()
st.dataframe(df, use_container_width=True)

# === Filter Section ===
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
        # Apply filters
        filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]

        st.write(f"Showing expenses from {start_date} to {end_date}")
        st.dataframe(filtered_df, use_container_width=True)

        # Total and Average Calculation
        total_filtered = filtered_df["Amount"].sum()
        num_days = (end_date - start_date).days + 1  # +1 to include the end date
        average_daily = total_filtered / num_days if num_days > 0 else 0

        st.success(f"💵 Total Spent in this period: ₹ {total_filtered:,.2f}")
        st.info(f"📊 Average Daily Spending: ₹ {average_daily:,.2f}")
else:
    st.info("No expenses available yet.")
