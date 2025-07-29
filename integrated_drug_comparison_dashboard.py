
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Synthetic drug data
drug_data = {
    "Atorvastatin": {"dosages": ["10mg", "20mg"], "generic_price": 12, "brand_price": 45},
    "Lisinopril": {"dosages": ["10mg", "20mg"], "generic_price": 8, "brand_price": 30},
    "Metformin": {"dosages": ["500mg", "1000mg"], "generic_price": 10, "brand_price": 35},
    "Omeprazole": {"dosages": ["20mg", "40mg"], "generic_price": 9, "brand_price": 32},
    "Simvastatin": {"dosages": ["10mg", "20mg"], "generic_price": 11, "brand_price": 38}
}

pharmacies = ["Pharmacy A", "Pharmacy B", "Pharmacy C"]

# Synthetic pricing function
def get_pharmacy_prices(drug, dosage):
    base_generic = drug_data[drug]["generic_price"]
    base_brand = drug_data[drug]["brand_price"]
    return {
        "Pharmacy A": {"Generic": base_generic, "Brand": base_brand},
        "Pharmacy B": {"Generic": base_generic + 2, "Brand": base_brand + 5},
        "Pharmacy C": {"Generic": base_generic - 1, "Brand": base_brand - 3}
    }

# Streamlit UI
st.title("Integrated Drug Cost Comparison Dashboard")

selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()))

drug_dosages = {}
for drug in selected_drugs:
    dosage = st.selectbox(f"Select dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    drug_dosages[drug] = dosage

if selected_drugs:
    st.subheader("Price Comparison Table")
    comparison_rows = []
    for drug in selected_drugs:
        dosage = drug_dosages[drug]
        prices = get_pharmacy_prices(drug, dosage)
        for pharmacy in pharmacies:
            comparison_rows.append({
                "Drug": drug,
                "Dosage": dosage,
                "Pharmacy": pharmacy,
                "Generic Price": prices[pharmacy]["Generic"],
                "Brand Price": prices[pharmacy]["Brand"]
            })
    df_comparison = pd.DataFrame(comparison_rows)
    st.dataframe(df_comparison)

    st.subheader("Generic vs Brand Price Comparison")
    for drug in selected_drugs:
        dosage = drug_dosages[drug]
        prices = get_pharmacy_prices(drug, dosage)
        generic_prices = [prices[p]["Generic"] for p in pharmacies]
        brand_prices = [prices[p]["Brand"] for p in pharmacies]

        fig, ax = plt.subplots()
        x = range(len(pharmacies))
        ax.bar(x, generic_prices, width=0.4, label='Generic', align='center')
        ax.bar([i + 0.4 for i in x], brand_prices, width=0.4, label='Brand', align='center')
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels(pharmacies)
        ax.set_ylabel("Price ($)")
        ax.set_title(f"{drug} ({dosage}) - Generic vs Brand")
        ax.legend()
        st.pyplot(fig)
