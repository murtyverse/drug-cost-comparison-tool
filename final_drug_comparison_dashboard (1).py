
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Synthetic drug data
drug_data = {
    "Atorvastatin": {"dosages": ["10mg", "20mg"], "generic_price": 15, "brand_price": 45},
    "Lisinopril": {"dosages": ["10mg", "20mg"], "generic_price": 10, "brand_price": 30},
    "Metformin": {"dosages": ["500mg", "1000mg"], "generic_price": 12, "brand_price": 35},
    "Omeprazole": {"dosages": ["20mg", "40mg"], "generic_price": 14, "brand_price": 40},
    "Amlodipine": {"dosages": ["5mg", "10mg"], "generic_price": 11, "brand_price": 32}
}

# Synthetic therapeutic alternatives
therapeutic_alternatives = {
    "Atorvastatin": [("Simvastatin", 12), ("Rosuvastatin", 18)],
    "Lisinopril": [("Enalapril", 9), ("Ramipril", 11)],
    "Metformin": [("Glipizide", 10), ("Glyburide", 13)],
    "Omeprazole": [("Pantoprazole", 13), ("Esomeprazole", 16)],
    "Amlodipine": [("Nifedipine", 10), ("Felodipine", 12)]
}

# Synthetic pharmacy data
pharmacies = ["PharmaOne", "HealthPlus", "MediCare"]

# Sidebar Navigation
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to Section", [
    "🏠 Home",
    "💊 Price Comparison",
    "📊 Generic vs Brand",
    "💰 Savings Estimator",
    "🧠 Therapeutic Alternatives"
])

# Top Navigation
st.markdown("""
<style>
.navbar {
    display: flex;
    gap: 20px;
    font-size: 18px;
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 5px;
}
.navbar a {
    text-decoration: none;
    color: #0366d6;
    font-weight: bold;
}
</style>
<div class='navbar'>
<span>🏠 Home</span>
<span>💊 Price Comparison</span>
<span>📊 Generic vs Brand</span>
<span>💰 Savings Estimator</span>
<span>🧠 Therapeutic Alternatives</span>
</div>
""", unsafe_allow_html=True)

st.title("Integrated Drug Cost Comparison Dashboard")

# Drug selection
selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()))
drug_selections = {}
for drug in selected_drugs:
    dosage = st.selectbox(f"Select Dosage for {drug}", drug_data[drug]["dosages"])
    drug_selections[drug] = dosage

# Section: Price Comparison
if nav_option == "💊 Price Comparison" and drug_selections:
    st.subheader("💊 Price Comparison Across Pharmacies")
    comparison_rows = []
    seq = 1
    for drug, dosage in drug_selections.items():
        for pharmacy in pharmacies:
            generic_price = drug_data[drug]["generic_price"] + random.randint(-2, 2)
            brand_price = drug_data[drug]["brand_price"] + random.randint(-5, 5)
            comparison_rows.append({
                "S.No": seq,
                "Drug": drug,
                "Dosage": dosage,
                "Pharmacy": pharmacy,
                "Generic Price ($)": generic_price,
                "Brand Price ($)": brand_price
            })
            seq += 1
    df_comparison = pd.DataFrame(comparison_rows)
    st.dataframe(df_comparison)

# Section: Generic vs Brand Visualization
if nav_option == "📊 Generic vs Brand" and drug_selections:
    st.subheader("📊 Generic vs Brand Price Comparison")
    for i, drug in enumerate(drug_selections, start=1):
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        fig, ax = plt.subplots()
        ax.bar(["Generic", "Brand"], [generic, brand], color=["green", "red"])
        ax.set_title(f"{i}. {drug} Price Comparison")
        ax.set_ylabel("Price ($)")
        st.pyplot(fig)

# Section: Savings Estimator
if nav_option == "💰 Savings Estimator" and drug_selections:
    st.subheader("💰 Estimated Savings")
    savings_rows = []
    for i, drug in enumerate(drug_selections, start=1):
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        monthly_savings = brand - generic
        annual_savings = monthly_savings * 12
        savings_rows.append({
            "S.No": i,
            "Drug": drug,
            "Monthly Savings ($)": monthly_savings,
            "Annual Savings ($)": annual_savings
        })
    df_savings = pd.DataFrame(savings_rows)
    st.dataframe(df_savings)

# Section: Therapeutic Alternatives
if nav_option == "🧠 Therapeutic Alternatives" and drug_selections:
    st.subheader("🧠 Therapeutic Alternatives Suggestion")
    for i, drug in enumerate(drug_selections, start=1):
        st.markdown(f"**{i}. Alternatives for {drug}:**")
        alt_rows = []
        original_price = drug_data[drug]["generic_price"]
        for j, (alt_drug, alt_price) in enumerate(therapeutic_alternatives.get(drug, []), start=1):
            savings = original_price - alt_price
            alt_rows.append({
                "S.No": j,
                "Alternative Drug": alt_drug,
                "Synthetic Price ($)": alt_price,
                "Estimated Savings ($)": savings
            })
        df_alt = pd.DataFrame(alt_rows)
        st.dataframe(df_alt)
