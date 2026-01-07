import streamlit as st
import math

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Prepay vs Invest Simulator",
    page_icon="⚖️",
    layout="centered"
)

# ---------------------------
# Finance Functions
# ---------------------------
def calculate_emi(principal, annual_rate, years):
    r = annual_rate / (12 * 100)
    n = years * 12
    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return emi, n, r

def remaining_balance(P, r, emi, k):
    return P * (1 + r)**k - emi * ((1 + r)**k - 1) / r

def future_value_monthly_sip(pmt, annual_return, months):
    r = annual_return / (12 * 100)
    if r == 0:
        return pmt * months
    return pmt * ((1 + r)**months - 1) / r

# ---------------------------
# Header
# ---------------------------
st.title("⚖️ Should I Prepay or Invest?")
st.caption("A simulator to decide what to do with your extra money")

st.info(
    "This tool compares two smart choices:\n"
    "1) Use extra money to **close your loan faster**\n"
    "2) Use the same money to **invest and grow wealth**\n\n"
    "There is no moral answer. Only **math and risk preference**."
)

st.markdown("---")

# ---------------------------
# Inputs
# ---------------------------
st.subheader("📥 Your Loan")

loan_amount = st.number_input("Outstanding Loan Amount (₹)", min_value=1000, value=500000, step=10000)
interest_rate = st.number_input("Loan Interest Rate (% per year)", min_value=0.0, value=10.0, step=0.1)
remaining_years = st.number_input("Remaining Tenure (Years)", min_value=1, max_value=40, value=5)

emi, n, r = calculate_emi(loan_amount, interest_rate, remaining_years)

st.write(f"💸 Your current EMI is approximately: **₹ {emi:,.0f} per month**")

st.markdown("---")

st.subheader("💰 Your Extra Money")

extra_monthly = st.number_input("Extra amount you can use every month (₹)", min_value=500, value=5000, step=500)

expected_return = st.number_input("Expected Investment Return (% per year)", min_value=0.0, value=12.0, step=0.5)

st.markdown("---")

# ---------------------------
# Option A: Prepay
# ---------------------------
st.header("🅰️ Option A: Use Extra Money to Prepay Loan")

# Simulate month by month
balance = loan_amount
months = 0
total_payment = 0

while balance > 0 and months < 1000:
    interest = balance * r
    payment = emi + extra_monthly

    if payment > balance + interest:
        payment = balance + interest

    principal_paid = payment - interest
    balance -= principal_paid

    total_payment += payment
    months += 1

original_total_payment = emi * n
interest_without_prepay = original_total_payment - loan_amount
interest_with_prepay = total_payment - loan_amount

interest_saved = interest_without_prepay - interest_with_prepay
years_saved = (n - months) / 12

st.success(f"🏁 You will close the loan in **{months} months** instead of {n} months.")
st.success(f"⏳ You become debt-free **{years_saved:.1f} years earlier**.")
st.success(f"💰 You save **₹ {interest_saved:,.0f}** in interest.")

st.markdown("---")

# ---------------------------
# Option B: Invest
# ---------------------------
st.header("🅱️ Option B: Invest the Extra Money Instead")

fv = future_value_monthly_sip(extra_monthly, expected_return, n)

st.info(
    f"If you invest **₹ {extra_monthly:,.0f} per month** for {remaining_years} years "
    f"at {expected_return}% return,\n\n"
    f"📈 You may accumulate approximately: **₹ {fv:,.0f}**"
)

st.markdown("---")

# ---------------------------
# Final Verdict
# ---------------------------
st.header("🏁 The Math-Based Comparison")

st.write(f"💰 Interest saved by prepaying: **₹ {interest_saved:,.0f}**")
st.write(f"📈 Wealth created by investing: **₹ {fv:,.0f}**")

if fv > interest_saved:
    st.success("📊 **Mathematically, INVESTING wins** in this scenario.")
else:
    st.warning("📊 **Mathematically, PREPAYING wins** in this scenario.")

# ---------------------------
# Teaching Insight
# ---------------------------
st.markdown("---")
st.subheader("🧠 The Real Insight")

st.write(
    """
- Prepaying a loan gives you a **guaranteed, risk-free return** equal to the loan interest rate.
- Investing gives you a **probabilistic, risky return**.

So:

> If your **loan interest rate** is very high → **Prepaying is usually smarter**  
> If your **investment return** is likely much higher → **Investing may win**

But psychologically:

> **Peace of mind of being debt-free** has value beyond math.
"""
)

st.info(
    "Great financial decisions are not just about returns. They are about **risk, freedom, and sleep quality** 😄"
)
