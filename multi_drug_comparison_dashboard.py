import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Synthetic data for demonstration
drug_data = {
    'Atorvastatin': {'10mg': {'Pharmacy A': 12.5, 'Pharmacy B': 11.0, 'Pharmacy C': 13.2},
                     '20mg': {'Pharmacy A': 15.0, 'Pharmacy B': 14.5, 'Pharmacy C': 16.0}},
    'Lisinopril': {'10mg': {'Pharmacy A': 8.0, 'Pharmacy B': 7.5, 'Pharmacy C': 9.0},
                   '20mg': {'Pharmacy A': 10.0, 'Pharmacy B': 9.5, 'Pharmacy C': 11.0}},
    'Metformin': {'500mg': {'Pharmacy A': 5.0, 'Pharmacy B': 4.8, 'Pharmacy C': 5.5},
                  '1000mg': {'Pharmacy A': 6.5, 'Pharmacy B': 6.0, 'Pharmacy C': 7.0}}
}

st.title("Multi-Drug Price Comparison Dashboard")

# Drug selection
selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()))

# Dosage selection for each selected drug
selected_dosages = {}
for drug in selected_drugs:
    dosages = list(drug_data[drug].keys())
    selected_dosages[drug] = st.selectbox(f"Select dosage for {drug}", dosages)

# Display comparative table
if selected_drugs:
    st.subheader("Price Comparison Table")
    comparison_rows = []
    for drug in selected_drugs:
        dosage = selected_dosages[drug]
        prices = drug_data[drug][dosage]
        for pharmacy, price in prices.items():
            comparison_rows.append({"Drug": drug, "Dosage": dosage, "Pharmacy": pharmacy, "Price": price})
    df_comparison = pd.DataFrame(comparison_rows)
    st.dataframe(df_comparison)

    # Bar chart visualization
    st.subheader("Price Comparison Chart")
    fig, ax = plt.subplots(figsize=(10, 6))
    for drug in selected_drugs:
        dosage = selected_dosages[drug]
        prices = drug_data[drug][dosage]
        ax.bar([f"{drug} ({pharmacy})" for pharmacy in prices.keys()], prices.values(), label=f"{drug} {dosage}")
    ax.set_ylabel("Price ($)")
    ax.set_title("Drug Prices Across Pharmacies")
    ax.legend()
    st.pyplot(fig)
