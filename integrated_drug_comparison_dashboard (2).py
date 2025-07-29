import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

drug_data = {
    "Atorvastatin": {"dosages": ["10mg", "20mg", "40mg"], "generic": "Atorvastatin", "brand": "Lipitor"},
    "Lisinopril": {"dosages": ["5mg", "10mg", "20mg"], "generic": "Lisinopril", "brand": "Prinivil"},
    "Metformin": {"dosages": ["500mg", "850mg", "1000mg"], "generic": "Metformin", "brand": "Glucophage"},
    "Amlodipine": {"dosages": ["2.5mg", "5mg", "10mg"], "generic": "Amlodipine", "brand": "Norvasc"},
    "Simvastatin": {"dosages": ["10mg", "20mg", "40mg"], "generic": "Simvastatin", "brand": "Zocor"},
    "Omeprazole": {"dosages": ["10mg", "20mg", "40mg"], "generic": "Omeprazole", "brand": "Prilosec"},
}

pharmacies = ["PharmaOne", "MediSave", "HealthHub"]

st.title("💊 Integrated Drug Cost Comparison Dashboard")

selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()), default=["Atorvastatin", "Lisinopril"])

def generate_pricing(drug, dosage):
    base_price = random.uniform(10, 50)
    generic_price = round(base_price, 2)
    brand_price = round(base_price * random.uniform(1.5, 2.5), 2)
    return generic_price, brand_price

comparison_rows = []
savings_summary = []

for drug in selected_drugs:
    st.subheader(f"💊 {drug}")
    dosage = st.selectbox(f"Select dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    generic_name = drug_data[drug]["generic"]
    brand_name = drug_data[drug]["brand"]
    generic_price, brand_price = generate_pricing(drug, dosage)

    for pharmacy in pharmacies:
        pharmacy_generic_price = round(generic_price * random.uniform(0.9, 1.1), 2)
        pharmacy_brand_price = round(brand_price * random.uniform(0.9, 1.1), 2)
        comparison_rows.append({
            "Drug": drug,
            "Dosage": dosage,
            "Pharmacy": pharmacy,
            "Generic": pharmacy_generic_price,
            "Brand": pharmacy_brand_price
        })

    st.markdown("**Generic vs Brand Price Comparison**")
    fig, ax = plt.subplots()
    ax.bar(["Generic", "Brand"], [generic_price, brand_price], color=["green", "red"])
    ax.set_ylabel("Price ($)")
    ax.set_title(f"{drug} ({dosage})")
    st.pyplot(fig)

    monthly_savings = round((brand_price - generic_price) * 30, 2)
    annual_savings = round(monthly_savings * 12, 2)
    savings_summary.append({
        "Drug": drug,
        "Dosage": dosage,
        "Monthly Savings ($)": monthly_savings,
        "Annual Savings ($)": annual_savings
    })

st.subheader("📊 Price Comparison Across Pharmacies")
df_comparison = pd.DataFrame(comparison_rows)
st.dataframe(df_comparison)

st.subheader("💰 Estimated Savings")
df_savings = pd.DataFrame(savings_summary)
st.dataframe(df_savings)
