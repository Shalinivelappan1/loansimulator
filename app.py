import streamlit as st
import math

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Debt Decision Lab",
    page_icon="🧪",
    layout="centered"
)

# =========================
# Finance Functions
# =========================
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

# =========================
# Header
# =========================
st.title("🧪 Debt Decision Lab")
st.caption("Explore loans, escape faster, and decide smarter")

st.info(
    "This lab is for **learning and exploration**. It is not for judging past choices.\n\n"
    "You will explore:\n"
    "1) How loans really behave\n"
    "2) How prepayment changes your future\n"
    "3) Whether prepaying or investing is mathematically smarter"
)

st.markdown("---")

# =========================
# Global Inputs
# =========================
st.subheader("📥 Your Loan (for all experiments)")

loan_amount = st.number_input("Outstanding Loan Amount (₹)", min_value=1000, value=500000, step=10000)
interest_rate = st.number_input("Loan Interest Rate (% per year)", min_value=0.0, value=10.0, step=0.1)
remaining_years = st.number_input("Remaining Tenure (Years)", min_value=1, max_value=40, value=5)

emi, n, r = calculate_emi(loan_amount, interest_rate, remaining_years)

st.write(f"💸 Current EMI ≈ **₹ {emi:,.0f} per month**")

st.markdown("---")

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs([
    "🧾 EMI Lab: Understand Your Loan",
    "🧨 Prepayment Lab: Escape Faster",
    "⚖️ Decision Lab: Prepay or Invest?"
])

# ======================================================
# TAB 1 — EMI LAB
# ======================================================
with tab1:
    st.header("🧾 EMI Lab: Understand Your Loan")

    total_payment = emi * n
    total_interest = total_payment - loan_amount
    interest_ratio = total_interest / loan_amount

    st.subheader("📊 Loan Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly EMI", f"₹ {emi:,.0f}")
    col2.metric("Total Interest", f"₹ {total_interest:,.0f}")
    col3.metric("Total Payment", f"₹ {total_payment:,.0f}")

    st.subheader("⏳ Time Commitment")
    st.write(f"You are committing **{n} months** (**{remaining_years} years of your life**) to this loan.")

    st.subheader("⚠️ Burden Meter")

    if interest_ratio < 0.25:
        st.success("🟢 Light Burden: Interest load is relatively low.")
    elif interest_ratio < 0.6:
        st.warning("🟠 Heavy Burden: A large part of what you repay is interest.")
    else:
        st.error("🔴 Suffocating Burden: You are paying huge interest over time.")

    st.info(
        "🧠 A loan is not a number. It is a **multi-year contract with your future self**."
    )

# ======================================================
# TAB 2 — PREPAYMENT LAB
# ======================================================
with tab2:
    st.header("🧨 Prepayment Lab: Escape Faster")

    st.write("See how **one smart prepayment** can reduce years of your life in debt.")

    colp1, colp2 = st.columns(2)

    with colp1:
        prepay_year = st.number_input(
            "Prepay after how many years?",
            min_value=1,
            max_value=max(1, remaining_years - 1),
            value=min(2, remaining_years - 1)
        )

    with colp2:
        prepay_amount = st.number_input(
            "Prepayment Amount (₹)",
            min_value=1000,
            max_value=int(loan_amount),
            value=50000,
            step=10000
        )

    k = prepay_year * 12

    balance_before = remaining_balance(loan_amount, r, emi, k)
    new_balance = balance_before - prepay_amount

    if new_balance <= 0:
        st.success("🎉 This prepayment completely closes your loan!")
    else:
        new_n = math.log(emi / (emi - new_balance * r)) / math.log(1 + r)
        new_n = int(math.ceil(new_n))

        original_remaining = n - k

        original_remaining_payment = emi * original_remaining
        new_remaining_payment = emi * new_n

        interest_saved = original_remaining_payment - new_remaining_payment

        st.subheader("📉 Prepayment Impact")

        colr1, colr2, colr3 = st.columns(3)
        colr1.metric("⏳ Months Reduced", f"{original_remaining - new_n}")
        colr2.metric("💰 Interest Saved", f"₹ {interest_saved:,.0f}")
        colr3.metric("🏁 New Remaining Tenure", f"{new_n} months")

        st.success("💡 Small actions can **buy back years of your life**.")

# ======================================================
# TAB 3 — DECISION LAB
# ======================================================
with tab3:
    st.header("⚖️ Decision Lab: Should I Prepay or Invest?")

    extra_monthly = st.number_input("Extra money available per month (₹)", min_value=500, value=5000, step=500)
    expected_return = st.number_input("Expected investment return (% per year)", min_value=0.0, value=12.0, step=0.5)

    # ---- Option A: Prepay simulation ----
    balance = loan_amount
    months = 0
    total_payment_with_prepay = 0

    while balance > 0 and months < 1000:
        interest = balance * r
        payment = emi + extra_monthly

        if payment > balance + interest:
            payment = balance + interest

        principal_paid = payment - interest
        balance -= principal_paid

        total_payment_with_prepay += payment
        months += 1

    original_total_payment = emi * n
    interest_without_prepay = original_total_payment - loan_amount
    interest_with_prepay = total_payment_with_prepay - loan_amount

    interest_saved = interest_without_prepay - interest_with_prepay
    years_saved = (n - months) / 12

    # ---- Option B: Invest ----
    fv = future_value_monthly_sip(extra_monthly, expected_return, n)

    st.subheader("📊 Comparison")

    colc1, colc2 = st.columns(2)

    with colc1:
        st.write("🅰️ **Prepay Loan**")
        st.write(f"Loan closes in: **{months} months**")
        st.write(f"Years saved: **{years_saved:.1f}**")
        st.write(f"Interest saved: **₹ {interest_saved:,.0f}**")

    with colc2:
        st.write("🅱️ **Invest Instead**")
        st.write(f"Future investment value: **₹ {fv:,.0f}**")

    st.markdown("---")

    st.subheader("🏁 Verdict")

    if fv > interest_saved:
        st.success("📈 **Mathematically, INVESTING wins** in this scenario.")
    else:
        st.warning("📉 **Mathematically, PREPAYING wins** in this scenario.")

    st.info(
        "🧠 Prepaying gives a **guaranteed return** equal to the loan interest rate.\n\n"
        "Investing gives a **risky but potentially higher return**.\n\n"
        "Great decisions balance **math, risk, and peace of mind**."
    )
