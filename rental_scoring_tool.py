import streamlit as st
import streamlit as st

st.set_page_config(page_title="Rental Check", layout="centered")

st.title("🏡 Rental Application Evaluator")

# Main Form
income = st.number_input("Monthly Income (R)", min_value=0)
debt = st.number_input("Monthly Debt (R)", min_value=0)
rent = st.number_input("Requested Rent (R)", min_value=0)
tpn = st.selectbox("TPN Score", ["Excellent", "Good", "Average", "Poor", "Unknown"])
deposit_ready = st.radio("Deposit Ready?", ["Yes", "No"])
rental_history = st.selectbox("Rental History", ["Clean", "Issues", "None"])
red_flags = st.text_area("Red Flags (if any)")

if st.button("Evaluate"):
    score = 100

    # Affordability
    affordability_ratio = (debt + rent) / income if income > 0 else 1
    if affordability_ratio > 0.6:
        score -= 30
    elif affordability_ratio > 0.45:
        score -= 15

    # TPN impact
    if tpn == "Good":
        score += 5
    elif tpn == "Average":
        score -= 10
    elif tpn == "Poor":
        score -= 25

    if deposit_ready == "No":
        score -= 10

    if rental_history == "Issues":
        score -= 20
    elif rental_history == "None":
        score -= 5

    if "eviction" in red_flags.lower():
        score -= 50
    elif red_flags.strip() != "":
        score -= 10

    # Result
    if score >= 80:
        verdict = "✅ Approved"
        color = "green"
    elif score >= 60:
        verdict = "🟡 Borderline"
        color = "orange"
    else:
        verdict = "❌ Declined"
        color = "red"

    st.markdown("---")
    st.markdown(f"<h3 style='color:{color}'>{verdict}</h3>", unsafe_allow_html=True)
    st.text(f"Score: {score}")
# Your Evaluate button logic here...
# Then add this at the end:
st.markdown("---")
if st.button("Reset"):
    st.session_state.clear()







