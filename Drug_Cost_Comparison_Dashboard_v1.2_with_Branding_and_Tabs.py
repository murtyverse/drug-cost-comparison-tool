
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Synthetic drug data with medical conditions
drug_data = {
    "Atorvastatin (Cholesterol)": {"dosages": ["10mg", "20mg"], "generic_price": 15, "brand_price": 45},
    "Lisinopril (Blood Pressure)": {"dosages": ["10mg", "20mg"], "generic_price": 10, "brand_price": 30},
    "Metformin (Diabetes)": {"dosages": ["500mg", "1000mg"], "generic_price": 12, "brand_price": 35},
    "Omeprazole (Acid Reflux)": {"dosages": ["20mg", "40mg"], "generic_price": 14, "brand_price": 40},
    "Amlodipine (Blood Pressure)": {"dosages": ["5mg", "10mg"], "generic_price": 11, "brand_price": 32}
}

# Synthetic therapeutic alternatives
therapeutic_alternatives = {
    "Atorvastatin (Cholesterol)": [("Simvastatin", 12), ("Rosuvastatin", 18)],
    "Lisinopril (Blood Pressure)": [("Enalapril", 9), ("Ramipril", 11)],
    "Metformin (Diabetes)": [("Glipizide", 10), ("Glyburide", 13)],
    "Omeprazole (Acid Reflux)": [("Pantoprazole", 13), ("Esomeprazole", 16)],
    "Amlodipine (Blood Pressure)": [("Nifedipine", 10), ("Felodipine", 12)]
}

# Synthetic efficacy scores and suitability indicators
efficacy_scores = {
    "Atorvastatin (Cholesterol)": 8.5,
    "Lisinopril (Blood Pressure)": 8.0,
    "Metformin (Diabetes)": 9.0,
    "Omeprazole (Acid Reflux)": 7.5,
    "Amlodipine (Blood Pressure)": 8.2
}

suitability_indicators = {
    "Atorvastatin (Cholesterol)": "✔️ Suitable for adults, caution in liver disease",
    "Lisinopril (Blood Pressure)": "✔️ Not recommended during pregnancy",
    "Metformin (Diabetes)": "✔️ Suitable for most adults, caution in kidney issues",
    "Omeprazole (Acid Reflux)": "✔️ Short-term use preferred",
    "Amlodipine (Blood Pressure)": "✔️ Suitable for elderly, monitor for swelling"
}

# Synthetic insurance coverage data
insurance_coverage = {
    "Atorvastatin (Cholesterol)": 0.8,
    "Lisinopril (Blood Pressure)": 0.75,
    "Metformin (Diabetes)": 0.85,
    "Omeprazole (Acid Reflux)": 0.7,
    "Amlodipine (Blood Pressure)": 0.78
}

pharmacies = ["PharmaOne", "HealthPlus", "MediCare"]

# Sidebar for role selection
st.sidebar.title("🔐 User Role")
role = st.sidebar.selectbox("Select your role", ["Patient", "Doctor", "Pharmacist", "Insurance Analyst"])

# Sidebar for drug selection
st.sidebar.title("💊 Drug Selection")
selected_drugs = st.sidebar.multiselect("Select Drugs", list(drug_data.keys()))

drug_selections = {}
for drug in selected_drugs:
    dosage = st.sidebar.selectbox(f"Select Dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    drug_selections[drug] = dosage

st.set_page_config(layout="wide")
st.title("Integrated Drug Cost Comparison Dashboard")

# Price Comparison Table
if drug_selections and role in ["Patient", "Doctor", "Pharmacist", "Insurance Analyst"]:
    st.subheader("💊 Price Comparison Across Pharmacies")
    comparison_rows = []
    for drug, dosage in drug_selections.items():
        for pharmacy in pharmacies:
            generic_price = drug_data[drug]["generic_price"] + random.randint(-2, 2)
            brand_price = drug_data[drug]["brand_price"] + random.randint(-5, 5)
            comparison_rows.append({
                "Drug": drug,
                "Dosage": dosage,
                "Pharmacy": pharmacy,
                "Generic Price ($)": generic_price,
                "Brand Price ($)": brand_price
            })
    df_comparison = pd.DataFrame(comparison_rows)
    df_comparison.reset_index(drop=True, inplace=True)
    df_comparison.insert(0, "Sr. No.", range(1, len(df_comparison) + 1))
    st.dataframe(df_comparison)

# Generic vs Brand Visualization
if drug_selections and role in ["Patient", "Doctor", "Pharmacist"]:
    st.subheader("📊 Generic vs Brand Price Comparison")
    for drug in drug_selections:
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        fig, ax = plt.subplots()
        ax.bar(["Generic", "Brand"], [generic, brand], color=["green", "red"])
        ax.set_title(f"{drug} Price Comparison")
        ax.set_ylabel("Price ($)")
        st.pyplot(fig)

# Savings Estimator
if drug_selections and role in ["Patient", "Insurance Analyst"]:
    st.subheader("💰 Estimated Savings")
    savings_rows = []
    for drug in drug_selections:
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        monthly_savings = brand - generic
        annual_savings = monthly_savings * 12
        savings_rows.append({
            "Drug": drug,
            "Monthly Savings ($)": monthly_savings,
            "Annual Savings ($)": annual_savings
        })
    df_savings = pd.DataFrame(savings_rows)
    df_savings.reset_index(drop=True, inplace=True)
    df_savings.insert(0, "Sr. No.", range(1, len(df_savings) + 1))
    st.dataframe(df_savings)

# Insurance Coverage Estimator
if drug_selections and role == "Patient":
    st.subheader("🛡️ Insurance Coverage Estimator")
    coverage_rows = []
    for drug in drug_selections:
        coverage = insurance_coverage.get(drug, 0.7)
        generic_price = drug_data[drug]["generic_price"]
        brand_price = drug_data[drug]["brand_price"]
        generic_covered = round(generic_price * coverage, 2)
        brand_covered = round(brand_price * coverage, 2)
        generic_copay = round(generic_price - generic_covered, 2)
        brand_copay = round(brand_price - brand_covered, 2)
        coverage_rows.append({
            "Drug": drug,
            "Coverage %": f"{int(coverage * 100)}%",
            "Generic Covered ($)": generic_covered,
            "Generic Co-pay ($)": generic_copay,
            "Brand Covered ($)": brand_covered,
            "Brand Co-pay ($)": brand_copay
        })
    df_coverage = pd.DataFrame(coverage_rows)
    df_coverage.reset_index(drop=True, inplace=True)
    df_coverage.insert(0, "Sr. No.", range(1, len(df_coverage) + 1))
    st.dataframe(df_coverage)

# Therapeutic Alternatives Suggestion
if drug_selections and role in ["Doctor", "Pharmacist"]:
    st.subheader("🧠 Therapeutic Alternatives Suggestion")
    for drug in drug_selections:
        st.markdown(f"**Alternatives for {drug}:**")
        alt_rows = []
        original_price = drug_data[drug]["generic_price"]
        for alt_drug, alt_price in therapeutic_alternatives.get(drug, []):
            savings = original_price - alt_price
            alt_rows.append({
                "Alternative Drug": alt_drug,
                "Synthetic Price ($)": alt_price,
                "Estimated Savings ($)": savings
            })
        df_alt = pd.DataFrame(alt_rows)
        df_alt.reset_index(drop=True, inplace=True)
        df_alt.insert(0, "Sr. No.", range(1, len(df_alt) + 1))
        st.dataframe(df_alt)

# Clinical Efficacy Scores and Suitability Indicators
if drug_selections and role in ["Doctor", "Patient"]:
    st.subheader("📈 Clinical Efficacy & Suitability")
    info_rows = []
    for drug in drug_selections:
        info_rows.append({
            "Drug": drug,
            "Efficacy Score (1-10)": efficacy_scores.get(drug, "N/A"),
            "Suitability Notes": suitability_indicators.get(drug, "N/A")
        })
    df_info = pd.DataFrame(info_rows)
    df_info.reset_index(drop=True, inplace=True)
    df_info.insert(0, "Sr. No.", range(1, len(df_info) + 1))
    st.dataframe(df_info)
