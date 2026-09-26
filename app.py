import streamlit as st
import pandas as pd
import math

st.title("Car Payment Calculator")

col1, col2 = st.columns(2)

vehicle_price = col1.number_input("Enter the vehicle price")
trade_in = col1.number_input("Enter the trade-in value")
down_payment = col2.number_input("Enter the down payment")
sales_tax = col2.number_input("Enter the sales tax")/100

sales_payment = (vehicle_price - trade_in) * sales_tax

p = vehicle_price + sales_payment - trade_in - down_payment

r = st.number_input("Enter the interest rate (APR)")/12/100
n = int(st.number_input("Enter the amount of months"))

monthly_payment = p * (r * (r + 1)** n)/ (((r + 1)**n) -1)

total_payment = monthly_payment * n

total_interest = total_payment - p

col1, col2, col3 = st.columns(3)

col1.metric(label="Monthly Payment", value=f"${monthly_payment:,.02f}")
col2.metric(label="Total Payment", value=f"${total_payment:,.02f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.02f}")

schedule = []
remaining_balance = p
for i in range(1, n + 1):
    interest_payment = remaining_balance * r
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12)
    schedule.append({"Remaining Balance": remaining_balance, "Year": year})

df = pd.DataFrame(schedule)
payment_df = df[["Year", "Remaining Balance"]].groupby("Year").min()

st.line_chart(payment_df)
