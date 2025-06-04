import streamlit as st

st.title("Rental Application Evaluator")
st.write("Welcome to the rental application evaluator tool.")
import streamlit as st

st.set_page_config(page_title="Rental Application Evaluator", layout="centered")

st.title("🏡 Rental Application Evaluator")

with st.form("applicant_form"):
    st.subheader("Enter Applicant Details")
    name = st.text_input("Applicant Name")
    income = st.number_input("Monthly Income (R)", min_value=0)
    debt = st.number_input("Monthly Debt (R)", min_value=0)
    rent = st.number_input("Requested Rent (R)", min_value=0)
    tpn_score = st.selectbox("TPN Rating", ["Excellent", "Good", "Average", "Poor", "Unknown"])
    deposit_ready = st.radio("Is Deposit Ready?", ["Yes", "No"])
    rental_history = st.selectbox("Rental History", ["Clean", "Issues", "None"])
    red_flags = st.text_area("Red Flags (optional)")

    submitted = st.form_submit_button("Evaluate Applicant")

if submitted:
    # Initial score
    score = 100

    # Affordability
    affordability = (debt + rent) / income if income > 0 else 1
    if affordability > 0.6:
        score -= 30
    elif affordability > 0.45:
        score -= 15

    # TPN score effect
    if tpn_score == "Good":
        score += 5
    elif tpn_score == "Average":
        score -= 10
    elif tpn_score == "Poor":
        score -= 25

    # Deposit
    if deposit_ready == "No":
        score -= 10

    # Rental History
    if rental_history == "Issues":
        score -= 20
    elif rental_history == "None":
        score -= 5

    # Red flags check
    if "eviction" in red_flags.lower():
        score -= 50
    elif red_flags.strip() != "":
        score -= 10

    # Final verdict
    if score >= 80:
        result = "✅ Approved"
        color = "green"
    elif score >= 60:
        result = "🟡 Borderline"
        color = "orange"
    else:
        result = "❌ Declined"
        color = "red"

    st.markdown("---")
    st.subheader("📋 Result")
    st.markdown(f"**Applicant:** {name}")
    st.markdown(f"**Score:** `{score}`")
    st.markdown(f"<span style='color:{color}; font-size:28px'>{result}</span>", unsafe_allow_html=True)




