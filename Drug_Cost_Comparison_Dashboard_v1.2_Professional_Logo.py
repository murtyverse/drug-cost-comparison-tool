
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Synthetic drug data with medical conditions
drug_data = {
    "Atorvastatin": {"condition": "High Cholesterol", "dosages": ["10mg", "20mg"], "generic_price": 15, "brand_price": 45},
    "Lisinopril": {"condition": "High Blood Pressure", "dosages": ["10mg", "20mg"], "generic_price": 10, "brand_price": 30},
    "Metformin": {"condition": "Type 2 Diabetes", "dosages": ["500mg", "1000mg"], "generic_price": 12, "brand_price": 35},
    "Omeprazole": {"condition": "Acid Reflux", "dosages": ["20mg", "40mg"], "generic_price": 14, "brand_price": 40},
    "Amlodipine": {"condition": "Hypertension", "dosages": ["5mg", "10mg"], "generic_price": 11, "brand_price": 32}
}

# Synthetic therapeutic alternatives
therapeutic_alternatives = {
    "Atorvastatin": [("Simvastatin", 12), ("Rosuvastatin", 18)],
    "Lisinopril": [("Enalapril", 9), ("Ramipril", 11)],
    "Metformin": [("Glipizide", 10), ("Glyburide", 13)],
    "Omeprazole": [("Pantoprazole", 13), ("Esomeprazole", 16)],
    "Amlodipine": [("Nifedipine", 10), ("Felodipine", 12)]
}

# Synthetic insurance coverage data
insurance_coverage = {
    "Atorvastatin": {"generic_coverage": 80, "brand_coverage": 50},
    "Lisinopril": {"generic_coverage": 85, "brand_coverage": 55},
    "Metformin": {"generic_coverage": 90, "brand_coverage": 60},
    "Omeprazole": {"generic_coverage": 75, "brand_coverage": 45},
    "Amlodipine": {"generic_coverage": 88, "brand_coverage": 52}
}

# Synthetic clinical efficacy scores
efficacy_scores = {
    "Atorvastatin": 8.5,
    "Lisinopril": 8.0,
    "Metformin": 9.0,
    "Omeprazole": 7.5,
    "Amlodipine": 8.2
}

# Synthetic patient suitability indicators
suitability_indicators = {
    "Atorvastatin": "Suitable for adults over 40",
    "Lisinopril": "Not recommended during pregnancy",
    "Metformin": "Monitor kidney function",
    "Omeprazole": "Short-term use preferred",
    "Amlodipine": "Use with caution in elderly"
}

pharmacies = ["PharmaOne", "HealthPlus", "MediCare"]

# Sidebar for role selection
st.set_page_config(layout="wide")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5e/Professional_icon.png", width=100)
st.sidebar.title("🔐 User Role")
role = st.sidebar.selectbox("Select your role", ["Patient", "Doctor", "Pharmacist", "Insurance Analyst"])

# Sidebar for drug selection
st.sidebar.title("💊 Drug Selection")
selected_drugs = st.sidebar.multiselect("Select Drugs", list(drug_data.keys()))

drug_selections = {}
for drug in selected_drugs:
    dosage = st.sidebar.selectbox(f"Select Dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    drug_selections[drug] = dosage

st.markdown("<h1 style='text-align: center; color: navy;'>Integrated Drug Cost Comparison Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Price Comparison Table
if drug_selections and role in ["Patient", "Doctor", "Pharmacist", "Insurance Analyst"]:
    st.subheader("💊 Price Comparison Across Pharmacies")
    comparison_rows = []
    for drug, dosage in drug_selections.items():
        for pharmacy in pharmacies:
            generic_price = drug_data[drug]["generic_price"] + random.randint(-2, 2)
            brand_price = drug_data[drug]["brand_price"] + random.randint(-5, 5)
            comparison_rows.append({
                "Drug": f"{drug} ({drug_data[drug]['condition']})",
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
        ax.set_title(f"{drug} ({drug_data[drug]['condition']}) Price Comparison")
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
            "Drug": f"{drug} ({drug_data[drug]['condition']})",
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
        generic_price = drug_data[drug]["generic_price"]
        brand_price = drug_data[drug]["brand_price"]
        coverage = insurance_coverage.get(drug, {"generic_coverage": 0, "brand_coverage": 0})
        generic_covered = round(generic_price * coverage["generic_coverage"] / 100, 2)
        brand_covered = round(brand_price * coverage["brand_coverage"] / 100, 2)
        generic_copay = round(generic_price - generic_covered, 2)
        brand_copay = round(brand_price - brand_covered, 2)
        coverage_rows.append({
            "Drug": f"{drug} ({drug_data[drug]['condition']})",
            "Generic Coverage %": coverage["generic_coverage"],
            "Brand Coverage %": coverage["brand_coverage"],
            "Generic Covered Amount ($)": generic_covered,
            "Brand Covered Amount ($)": brand_covered,
            "Generic Co-pay ($)": generic_copay,
            "Brand Co-pay ($)": brand_copay
        })
    df_coverage = pd.DataFrame(coverage_rows)
    df_coverage.reset_index(drop=True, inplace=True)
    df_coverage.insert(0, "Sr. No.", range(1, len(df_coverage) + 1))
    st.dataframe(df_coverage)

# Clinical Efficacy Scores and Suitability Indicators
if drug_selections and role in ["Doctor", "Pharmacist"]:
    st.subheader("🧪 Clinical Efficacy & Suitability")
    info_rows = []
    for drug in drug_selections:
        info_rows.append({
            "Drug": f"{drug} ({drug_data[drug]['condition']})",
            "Efficacy Score (1-10)": efficacy_scores.get(drug, "N/A"),
            "Suitability Notes": suitability_indicators.get(drug, "N/A")
        })
    df_info = pd.DataFrame(info_rows)
    df_info.reset_index(drop=True, inplace=True)
    df_info.insert(0, "Sr. No.", range(1, len(df_info) + 1))
    st.dataframe(df_info)

# Therapeutic Alternatives Suggestion
if drug_selections and role in ["Doctor", "Pharmacist"]:
    st.subheader("🧠 Therapeutic Alternatives Suggestion")
    for drug in drug_selections:
        st.markdown(f"**Alternatives for {drug} ({drug_data[drug]['condition']}):**")
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
