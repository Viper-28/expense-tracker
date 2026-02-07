# 📒 Expense Tracker

A simple and intuitive expense tracking application built with Streamlit and PostgreSQL.

## Features

- ✅ **Add Expenses** - Log expenses with date, name, amount, and category
- 📋 **View All Expenses** - See all your expenses in a clean table format
- 📅 **Filter by Date Range** - View expenses within a specific time period
- 🏷️ **Filter by Category** - Filter expenses by Food, Entertainment, or College
- 💵 **Total Spending** - See your total spending for filtered results
- 📊 **Average Daily Spending** - Track your average daily expenditure

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL
- **Data Processing**: Pandas

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Viper-28/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variable for database:

   ```bash
   export DATABASE_URL="your_postgresql_connection_string"
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Deployment

This app is configured for deployment on Render. The `setup.sh` script handles Streamlit server configuration.

## Usage

1. **Add an Expense**: Fill in the date, expense name, amount, and select a category, then click "Add Expense"
2. **View Expenses**: All expenses are displayed in a table below the form
3. **Filter Data**: Use the date range picker and category dropdown to filter your expenses
4. **Review Statistics**: View total spending and average daily spending for filtered results

## License

MIT License
