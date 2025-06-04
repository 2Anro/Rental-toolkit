import streamlit as st

st.title("Rental Application Evaluator")
st.write("Welcome to the rental application evaluator tool.")

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
