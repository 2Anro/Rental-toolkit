import streamlit as st

st.title("Rental Application Evaluator")
st.write("Welcome to the rental application evaluator tool.")
im
def evaluate_applicant(applicant):
    income = applicant['income']
    debt = applicant['debt']
    rent = applicant['rent']
    tpn = applicant['tpn']
    deposit_ready = applicant['deposit_ready']
    rental_history = applicant['rental_history']
    red_flags = applicant['red_flags']

    net_income = income - debt
    rent_to_income = rent / net_income if net_income else 1  # avoid division by zero
    debt_to_income = debt / income if income else 1

    # Scoring system
    score = 0
    if rent_to_income <= 0.33:
        score += 5
    if debt_to_income <= 0.4:
        score += 3
    if tpn.lower() == "good":
        score += 3
    if deposit_ready.lower() == "yes":
        score += 2
    if rental_history.lower() == "good":
        score += 2
    if red_flags.lower() == "no":
        score += 2

    # Decision logic
    if score >= 15:
        decision = "Accept"
        risk = "Green"
    elif score >= 10:
        decision = "Review"
        risk = "Orange"
    else:
        decision = "Decline"
        risk = "Red"

    return {
        "Net Income": net_income,
        "Rent-to-Income Ratio": round(rent_to_income, 2),
        "Debt-to-Income Ratio": round(debt_to_income, 2),
        "Score": score,
        "Decision": decision,
        "Risk Level": risk
    }


if __name__ == "__main__":
    # Sample data to test
    applicant = {
        "income": 31000,
        "debt": 9000,
        "rent": 17500,
        "tpn": "Good",
        "deposit_ready": "Unknown",
        "rental_history": "No History",
        "red_flags": "Unknown"
    }

    result = evaluate_applicant(applicant)
    for k, v in result.items():
        print(f"{k}: {v}")
port streamlit as st

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




