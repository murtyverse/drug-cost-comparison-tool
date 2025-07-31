
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

st.title("Integrated Drug Cost Comparison Dashboard")

# Drug selection
selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()))

drug_selections = {}
for drug in selected_drugs:
    dosage = st.selectbox(f"Select Dosage for {drug}", drug_data[drug]["dosages"])
    drug_selections[drug] = dosage

# Display price comparison table
if drug_selections:
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
    df_comparison.insert(0, "Sr. No.", range(1, len(df_comparison) + 1))
    st.dataframe(df_comparison)

# Generic vs Brand Visualization
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
df_savings.insert(0, "Sr. No.", range(1, len(df_savings) + 1))
st.dataframe(df_savings)

# Therapeutic Alternatives Suggestion
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
    df_alt.insert(0, "Sr. No.", range(1, len(df_alt) + 1))
    st.dataframe(df_alt)
