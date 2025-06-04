import streamlit as st

st.set_page_config(page_title="Rental Scoring Tool", layout="centered")
st.title("🏡 Rental Application Scoring Tool")

st.markdown("""
This tool helps you evaluate rental applications based on income, debt, rent, and other factors.
""")

# Initialize session state if not set
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "score" not in st.session_state:
    st.session_state.score = None

# Input form
with st.form("rental_form"):
    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input("Total Net Income (Monthly)", min_value=0, step=500)
        debt = st.number_input("Monthly Debt Obligations", min_value=0, step=500)
        rent = st.number_input("Expected Rent", min_value=0, step=500)

    with col2:
        tpn_status = st.selectbox("TPN Status", ["Good", "Average", "Poor", "Unknown"])
        deposit_ready = st.selectbox("Deposit Ready", ["Yes", "No", "Unknown"])
        rental_history = st.selectbox("Rental History", ["Yes", "No", "Unknown"])
        red_flags = st.selectbox("Any Red Flags?", ["No", "Yes", "Unclear"])

    submitted = st.form_submit_button("Score Applicant")

# Scoring logic
if submitted:
    st.session_state.submitted = True
    score = 0
    explanations = []

    if income <= 0 or rent <= 0:
        st.error("Please enter both income and rent values greater than 0.")
        st.stop()

    affordability = income - debt
    rent_to_income_ratio = rent / income

    # Rent to income ratio
    if rent_to_income_ratio <= 0.3:
        score += 30
        explanations.append("✅ Rent is less than 30% of income")
    elif rent_to_income_ratio <= 0.4:
        score += 20
        explanations.append("🟡 Rent is 30-40% of income")
    else:
        explanations.append("🔴 Rent is more than 40% of income")

    # Affordability
    if affordability >= rent:
        score += 20
        explanations.append("✅ Enough disposable income after debt to afford rent")
    elif affordability >= rent * 0.8:
        score += 10
        explanations.append("🟡 Barely enough income after debt")
    else:
        explanations.append("🔴 Not enough income after debt")

    # TPN status
    if tpn_status == "Good":
        score += 20
        explanations.append("✅ Good TPN status")
    elif tpn_status == "Average":
        score += 10
        explanations.append("🟡 Average TPN status")
    elif tpn_status == "Poor":
        explanations.append("🔴 Poor TPN status")
    else:
        explanations.append("⚪ TPN status unknown")

    # Deposit
    if deposit_ready == "Yes":
        score += 10
        explanations.append("✅ Deposit ready")
    elif deposit_ready == "Unknown":
        score += 5
        explanations.append("🟡 Deposit readiness unknown")
    else:
        explanations.append("🔴 No deposit ready")

    # Rental History
    if rental_history == "Yes":
        score += 10
        explanations.append("✅ Rental history available")
    elif rental_history == "Unknown":
        score += 5
        explanations.append("🟡 Rental history unknown")
    else:
        explanations.append("⚪ No rental history")

    # Red Flags
    if red_flags == "Yes":
        score -= 10
        explanations.append("🔴 Red flags present")
    elif red_flags == "Unclear":
        score += 0
        explanations.append("🟡 Red flags unclear")
    else:
        explanations.append("✅ No red flags")

    st.session_state.score = score

# Output score
if st.session_state.submitted and st.session_state.score is not None:
    st.markdown("---")
    st.subheader("Applicant Score")

    score = st.session_state.score
    if score >= 80:
        st.success(f"🟢 Strong Candidate — Score: {score}/100")
    elif score >= 60:
        st.info(f"🟡 Borderline Candidate — Score: {score}/100")
    else:
        st.error(f"🔴 Weak Candidate — Score: {score}/100")

    st.markdown("### Reasoning:")
    for reason in explanations:
        st.write("-", reason)

# Reset button without st.experimental_rerun (which causes issues)
if st.button("🔄 Reset Form"):
    st.session_state.submitted = False
    st.session_state.score = None
    st.experimental_set_query_params()
    st.experimental_rerun()
