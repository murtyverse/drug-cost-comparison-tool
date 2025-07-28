
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Synthetic drug data
drug_data = {
    "Atorvastatin": {
        "10mg": {"generic": 12.50, "brand": 45.00},
        "20mg": {"generic": 14.00, "brand": 48.00}
    },
    "Lisinopril": {
        "10mg": {"generic": 10.00, "brand": 38.00},
        "20mg": {"generic": 11.50, "brand": 40.00}
    },
    "Metformin": {
        "500mg": {"generic": 8.00, "brand": 30.00},
        "1000mg": {"generic": 9.50, "brand": 32.00}
    }
}

# Synthetic pharmacy pricing data
pharmacy_data = pd.DataFrame([
    {"Pharmacy": "HealthPlus", "Drug": "Atorvastatin", "Dosage": "10mg", "Price": 13.00},
    {"Pharmacy": "WellCare", "Drug": "Atorvastatin", "Dosage": "10mg", "Price": 12.75},
    {"Pharmacy": "MediStore", "Drug": "Atorvastatin", "Dosage": "10mg", "Price": 12.90},
    {"Pharmacy": "HealthPlus", "Drug": "Lisinopril", "Dosage": "10mg", "Price": 10.25},
    {"Pharmacy": "WellCare", "Drug": "Lisinopril", "Dosage": "10mg", "Price": 10.10},
    {"Pharmacy": "MediStore", "Drug": "Lisinopril", "Dosage": "10mg", "Price": 10.30},
    {"Pharmacy": "HealthPlus", "Drug": "Metformin", "Dosage": "500mg", "Price": 8.10},
    {"Pharmacy": "WellCare", "Drug": "Metformin", "Dosage": "500mg", "Price": 8.00},
    {"Pharmacy": "MediStore", "Drug": "Metformin", "Dosage": "500mg", "Price": 8.05}
])

# Streamlit UI
st.title("💊 Real-Time Drug Cost Comparison Tool")

# Drug selection
drug = st.selectbox("Select Drug", list(drug_data.keys()))
dosage = st.selectbox("Select Dosage", list(drug_data[drug].keys()))

# Display synthetic pharmacy pricing
st.subheader("📋 Pharmacy Pricing")
filtered_pharmacies = pharmacy_data[(pharmacy_data["Drug"] == drug) & (pharmacy_data["Dosage"] == dosage)]
st.dataframe(filtered_pharmacies)

# Generic vs Brand comparison chart
st.subheader("📊 Generic vs Brand Price Comparison")
prices = drug_data[drug][dosage]
fig, ax = plt.subplots()
ax.bar(["Generic", "Brand"], [prices["generic"], prices["brand"]], color=["green", "red"])
ax.set_ylabel("Price (USD)")
ax.set_title(f"{drug} {dosage} - Price Comparison")
for i, v in enumerate([prices["generic"], prices["brand"]]):
    ax.text(i, v + 1, f"${v:.2f}", ha='center')
st.pyplot(fig)

# Insight message
savings = prices["brand"] - prices["generic"]
st.markdown(f"💡 **Insight**: Choosing the generic version of {drug} {dosage} can save approximately **${savings:.2f}** per prescription.")
