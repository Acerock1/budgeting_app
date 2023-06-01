import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from datetime import date
import calendar
import database

st.set_page_config(
    page_title="budgeting_app",
    page_icon="💵",
    layout="centered"
)

# Page config
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Car", "Savings", "Other Expenses"]
currency = "USD"
page_title = "Income and Expense Tracker"
page_icon = "💵"
years = [date.today().year, date.today().year - 1, date.today().year - 2]
months = list(calendar.month_name[1:])


# Database interface
def get_all_periods():
    items = database.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# Data entry column (option menu)
if option_selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("Enter Data", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")

        "_ _ _"
        with st.expander("Incomes"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, step=100, format="%i")
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, step=50, format="%i")
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter your comments here 🥳...")
        
        "_ _ _"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            database.insert_period(period, incomes, expenses, comment)
            st.success("Data saved 🔥")


# Data visualization option menu
if option_selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("Saved Periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            "_ _ _"
            period_data = database.get_period(period)
            comment = period_data.get("comment")
            incomes = period_data.get("incomes")
            expenses = period_data.get("expenses")
            
            # Create metrics
            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remainder = total_income - total_expenses
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income}{currency}")
            col2.metric("Total Expense", f"{total_expenses}{currency}")
            col3.metric("Remaining Budget", f"{remainder}{currency}")
            st.text(f"Comment: {comment}")

            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)

            # Rest of your visualization code...
