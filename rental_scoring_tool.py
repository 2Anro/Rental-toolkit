import streamlit as st
import streamlit as st

st.set_page_config(page_title="Rental Application Scoring Tool", layout="centered")

st.title("🏠 Rental Application Scoring Tool")
st.markdown("This tool helps evaluate whether an applicant can afford a property.")

# Input fields with keys for reset
income = st.number_input("Monthly Income", min_value=0, step=100, key="income_input")
rent = st.number_input("Proposed Rent", min_value=0, step=100, key="rent_input")
debt = st.number_input("Monthly Debt Obligations", min_value=0, step=100, key="debt_input")

# Extra checkboxes
has_good_tpn = st.checkbox("TPN record is good", key="tpn_input")
has_deposit = st.checkbox("Deposit is ready", key="deposit_input")
has_rental_history = st.checkbox("Positive rental history", key="rental_history_input")
has_red_flags = st.checkbox("Red flags present (e.g. judgments, defaults)", key="red_flags_input")

if st.button("Evaluate"):
    # Handle invalid inputs
    if income <= 0 or rent <= 0:
        st.warning("Missing or invalid input. Applicant automatically scored as 'Rejected'.")
        score = "Rejected"
    else:
        # Basic affordability rule: rent should be less than 33% of income
        rent_to_income_ratio = rent / income
        debt_to_income_ratio = debt / income if income else 0

        score = "Borderline"

        if rent_to_income_ratio > 0.5 or debt_to_income_ratio > 0.5:
            score = "Rejected"
        elif rent_to_income_ratio <= 0.33 and debt_to_income_ratio <= 0.33:
            score = "Good"

        # Adjustments
        if not has_good_tpn or has_red_flags:
            score = "Rejected"
        elif has_good_tpn and has_deposit and has_rental_history:
            if score == "Borderline":
                score = "Good"

        st.subheader(f"🏁 Final Score: {score}")

# Reset button
if st.button("Reset"):
    for key in [
        "income_input", "rent_input", "debt_input",
        "tpn_input", "deposit_input", "rental_history_input", "red_flags_input"
    ]:
        if key in st.session_state:
            del st.session_state[key]
    
   







