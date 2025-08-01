
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Branding
st.set_page_config(layout="wide")
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; background-color: #0033A0; padding: 10px 20px; color: white;'>
        <div style='font-size: 24px; font-weight: bold;'>Integrated Drug Cost Comparison Dashboard</div>
        <img src='https://upload.wikimedia.org/wikipedia/commons/3/3e/Cognizant_logo_2022.svg' width='160'/>
    </div>
""", unsafe_allow_html=True)

# Synthetic drug data with medical conditions
drug_data = {
    "Atorvastatin (Cholesterol)": {"dosages": ["10mg", "20mg"], "generic_price": 15, "brand_price": 45, "efficacy": 8.5},
    "Lisinopril (Hypertension)": {"dosages": ["10mg", "20mg"], "generic_price": 10, "brand_price": 30, "efficacy": 8.0},
    "Metformin (Diabetes)": {"dosages": ["500mg", "1000mg"], "generic_price": 12, "brand_price": 35, "efficacy": 9.0},
    "Omeprazole (Acid Reflux)": {"dosages": ["20mg", "40mg"], "generic_price": 14, "brand_price": 40, "efficacy": 7.5},
    "Amlodipine (Hypertension)": {"dosages": ["5mg", "10mg"], "generic_price": 11, "brand_price": 32, "efficacy": 8.2}
}

# Synthetic therapeutic alternatives
therapeutic_alternatives = {
    "Atorvastatin (Cholesterol)": [("Simvastatin", 12), ("Rosuvastatin", 18)],
    "Lisinopril (Hypertension)": [("Enalapril", 9), ("Ramipril", 11)],
    "Metformin (Diabetes)": [("Glipizide", 10), ("Glyburide", 13)],
    "Omeprazole (Acid Reflux)": [("Pantoprazole", 13), ("Esomeprazole", 16)],
    "Amlodipine (Hypertension)": [("Nifedipine", 10), ("Felodipine", 12)]
}

pharmacies = ["PharmaOne", "HealthPlus", "MediCare"]

# Sidebar
st.sidebar.title("🔐 User Role")
role = st.sidebar.selectbox("Select your role", ["Patient", "Doctor", "Pharmacist", "Insurance Analyst"])

st.sidebar.title("💊 Drug Selection")
selected_drugs = st.sidebar.multiselect("Select Drugs", list(drug_data.keys()))

drug_selections = {}
for drug in selected_drugs:
    dosage = st.sidebar.selectbox(f"Select Dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    drug_selections[drug] = dosage

# Price Comparison
if drug_selections:
    st.subheader("💊 Price Comparison Across Pharmacies")
    rows = []
    for drug, dosage in drug_selections.items():
        for pharmacy in pharmacies:
            generic = drug_data[drug]["generic_price"] + random.randint(-2, 2)
            brand = drug_data[drug]["brand_price"] + random.randint(-5, 5)
            rows.append({
                "Drug": drug,
                "Dosage": dosage,
                "Pharmacy": pharmacy,
                "Generic Price ($)": generic,
                "Brand Price ($)": brand
            })
    df = pd.DataFrame(rows)
    df.reset_index(drop=True, inplace=True)
    df.insert(0, "Sr. No.", range(1, len(df)+1))
    st.dataframe(df)

# Generic vs Brand Chart
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
    rows = []
    for drug in drug_selections:
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        rows.append({
            "Drug": drug,
            "Monthly Savings ($)": brand - generic,
            "Annual Savings ($)": (brand - generic) * 12
        })
    df = pd.DataFrame(rows)
    df.reset_index(drop=True, inplace=True)
    df.insert(0, "Sr. No.", range(1, len(df)+1))
    st.dataframe(df)

# Insurance Coverage Estimator
if drug_selections and role == "Patient":
    st.subheader("🛡️ Insurance Coverage Estimator")
    rows = []
    for drug in drug_selections:
        coverage = random.choice([60, 70, 80, 90])
        generic = drug_data[drug]["generic_price"]
        brand = drug_data[drug]["brand_price"]
        rows.append({
            "Drug": drug,
            "Coverage (%)": coverage,
            "Generic Covered ($)": round(generic * coverage / 100, 2),
            "Generic Co-pay ($)": round(generic * (100 - coverage) / 100, 2),
            "Brand Covered ($)": round(brand * coverage / 100, 2),
            "Brand Co-pay ($)": round(brand * (100 - coverage) / 100, 2)
        })
    df = pd.DataFrame(rows)
    df.reset_index(drop=True, inplace=True)
    df.insert(0, "Sr. No.", range(1, len(df)+1))
    st.dataframe(df)

# Therapeutic Alternatives
if drug_selections and role in ["Doctor", "Pharmacist"]:
    st.subheader("🧠 Therapeutic Alternatives Suggestion")
    for drug in drug_selections:
        st.markdown(f"**Alternatives for {drug}:**")
        rows = []
        original = drug_data[drug]["generic_price"]
        for alt, price in therapeutic_alternatives.get(drug, []):
            rows.append({
                "Alternative Drug": alt,
                "Synthetic Price ($)": price,
                "Estimated Savings ($)": original - price
            })
        df = pd.DataFrame(rows)
        df.reset_index(drop=True, inplace=True)
        df.insert(0, "Sr. No.", range(1, len(df)+1))
        st.dataframe(df)

# Clinical Efficacy & Suitability
if drug_selections and role in ["Doctor", "Pharmacist"]:
    st.subheader("📈 Clinical Efficacy & Patient Suitability")
    rows = []
    for drug in drug_selections:
        efficacy = drug_data[drug]["efficacy"]
        suitability = random.choice(["✔️ Suitable", "⚠️ Use with caution", "❌ Not recommended"])
        rows.append({
            "Drug": drug,
            "Efficacy Score (1-10)": efficacy,
            "Patient Suitability": suitability
        })
    df = pd.DataFrame(rows)
    df.reset_index(drop=True, inplace=True)
    df.insert(0, "Sr. No.", range(1, len(df)+1))
    st.dataframe(df)
