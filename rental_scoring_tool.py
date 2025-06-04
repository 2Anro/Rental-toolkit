import streamlit as st

st.title("Rental Application Evaluator")
st.write("Welcome to the rental application evaluator tool.")

import streamlit as st

st.set_page_config(page_title="Rental Application Evaluator", layout="centered")

st.title("🏠 Rental Application Evaluator")

st.markdown("Enter applicant details below to determine rental suitability.")

with st.form("applicant_form"):
    name = st.text_input("Applicant Name")
    income = st.number_input("Monthly Income (R)", min_value=0)
    debt = st.number_input("Monthly Debt Obligations (R)", min_value=0)
    rent = st.number_input("Requested Rent Amount (R)", min_value=0)
    tpn_score = st.selectbox("TPN Status", ["Excellent", "Good", "Average", "Poor", "Unknown"])
    deposit_ready = st.radio("Deposit Ready?", ["Yes", "No"])
    rental_history = st.selectbox("Rental History", ["Clean", "Issues", "None"])
    red_flags = st.text_area("Red Flags (Optional)", "")

    submitted = st.form_submit_button("Evaluate")

if submitted:
    affordability_ratio = (rent + debt) / income if income > 0 else 1
    score = 100

    # Score adjustments
    if affordability_ratio > 0.6:
        score -= 30
    elif affordability_ratio > 0.45:
        score -= 15

    if tpn_score == "Good":
        score += 10
    elif tpn_score == "Average":
        score -= 10
    elif tpn_score == "Poor":
        score -= 30

    if deposit_ready == "No":
        score -= 10

    if rental_history == "Issues":
        score -= 15
    elif rental_history == "None":
        score -= 5

    if "eviction" in red_flags.lower():
        score -= 50

    # Result
    if score >= 80:
        verdict = "✅ Approved"
        color = "green"
    elif 60 <= score < 80:
        verdict = "🟡 Borderline"
        color = "orange"
    else:
        verdict = "❌ Declined"
        color = "red"

    st.markdown("---")
    st.subheader("Evaluation Result")
    st.markdown(f"**Score:** `{score}`")
    st.markdown(f"<span style='color:{color}; font-size:24px'>{verdict}</span>", unsafe_allow_html=True)

