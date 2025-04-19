
import streamlit as st

# Intervention data
interventions = [
    {"name": "Smoking cessation", "arr": 17},
    {"name": "Statin (atorvastatin 80 mg)", "arr": 9},
    {"name": "Ezetimibe", "arr": 2},
    {"name": "PCSK9 inhibitor", "arr": 5},
    {"name": "Antiplatelet (ASA or clopidogrel)", "arr": 6},
    {"name": "BP control (ACEi/ARB ± CCB)", "arr": 12},
    {"name": "Semaglutide 2.4 mg", "arr": 4},
    {"name": "Weight loss to ideal BMI", "arr": 10},
    {"name": "Empagliflozin", "arr": 6},
    {"name": "Icosapent ethyl (TG ≥1.5)", "arr": 5},
    {"name": "Mediterranean diet", "arr": 9},
    {"name": "Physical activity", "arr": 9},
    {"name": "Alcohol moderation", "arr": 5},
    {"name": "Stress reduction", "arr": 3}
]

# ARR scaler based on age
def scale_arr_by_age(base_arr, age):
    if age <= 50:
        return base_arr * 1.1
    elif age <= 60:
        return base_arr * 1.0
    elif age <= 70:
        return base_arr * 0.8
    else:
        return base_arr * 0.6

# ARR calculator with age, LDL, HbA1c adjustment
def calculate_arr(selected, age, ldl=None, hba1c=None):
    remaining_risk = 100.0
    cumulative_arr = 0.0

    for i, selected_flag in enumerate(selected):
        if selected_flag:
            base_arr = interventions[i]["arr"]
            adj_arr = scale_arr_by_age(base_arr, age)
            reduced = remaining_risk * (adj_arr / 100)
            cumulative_arr += reduced
            remaining_risk -= reduced

    if ldl is not None:
        if ldl >= 2.5:
            adj = 5
        elif ldl >= 1.8:
            adj = 3
        elif ldl >= 1.4:
            adj = 1.5
        elif ldl >= 1.0:
            adj = 0
        else:
            adj = -1
        remaining_risk += adj
        cumulative_arr -= adj

    if hba1c is not None:
        if hba1c >= 9.0:
            adj = 4
        elif hba1c >= 8.0:
            adj = 3
        elif hba1c >= 7.0:
            adj = 1.5
        elif hba1c >= 6.0:
            adj = 0
        else:
            adj = -1
        remaining_risk += adj
        cumulative_arr -= adj

    return round(cumulative_arr, 1), round(remaining_risk, 1)

# Streamlit UI
st.title("CVD Risk Reduction Estimator")

age = st.slider("Age", 30, 90, 60)
ldl = st.number_input("LDL-C (mmol/L)", min_value=0.5, max_value=6.0, value=1.8, step=0.1)
hba1c = st.number_input("HbA1c (%)", min_value=4.5, max_value=12.0, value=7.0, step=0.1)

st.markdown("### Select Interventions")
selection = [st.checkbox(intervention["name"], value=False) for intervention in interventions]

if st.button("Calculate Risk Reduction"):
    cumulative, remaining = calculate_arr(selection, age, ldl, hba1c)
    st.success(f"Estimated Cumulative ARR: {cumulative}%")
    st.info(f"Estimated Remaining Lifetime Risk: {remaining}%")
