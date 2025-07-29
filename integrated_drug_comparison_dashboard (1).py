import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Synthetic drug data
drug_data = {
    "Atorvastatin": {"dosages": ["10mg", "20mg"], "brand_price": 120, "generic_price": 30},
    "Lisinopril": {"dosages": ["10mg", "20mg"], "brand_price": 90, "generic_price": 25},
    "Metformin": {"dosages": ["500mg", "1000mg"], "brand_price": 80, "generic_price": 20},
}

pharmacies = ["Pharmacy A", "Pharmacy B", "Pharmacy C"]

# Streamlit UI
st.title("Integrated Drug Cost Comparison Dashboard")

# Drug selection
selected_drugs = st.multiselect("Select Drugs", list(drug_data.keys()))

drug_selections = {}
for drug in selected_drugs:
    dosage = st.selectbox(f"Select dosage for {drug}", drug_data[drug]["dosages"], key=drug)
    drug_selections[drug] = dosage

# Display comparison table
if drug_selections:
    st.subheader("Price Comparison Table")
    comparison_rows = []
    for drug, dosage in drug_selections.items():
        comparison_rows.append({
            "Drug": drug,
            "Dosage": dosage,
            "Brand Price": f"${drug_data[drug]['brand_price']}",
            "Generic Price": f"${drug_data[drug]['generic_price']}"
        })
    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df)

    # Bar chart for generic vs brand
    st.subheader("Generic vs Brand Price Comparison")
    fig, ax = plt.subplots()
    brand_prices = [drug_data[drug]["brand_price"] for drug in drug_selections]
    generic_prices = [drug_data[drug]["generic_price"] for drug in drug_selections]
    x = range(len(drug_selections))
    ax.bar(x, brand_prices, width=0.4, label='Brand', align='center')
    ax.bar([i + 0.4 for i in x], generic_prices, width=0.4, label='Generic', align='center')
    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(list(drug_selections.keys()))
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)

    # Savings Estimator
    st.subheader("Estimated Savings")
    usage_per_month = 30  # synthetic usage frequency
    savings_rows = []
    for drug in drug_selections:
        brand_cost = drug_data[drug]["brand_price"] * usage_per_month
        generic_cost = drug_data[drug]["generic_price"] * usage_per_month
        monthly_savings = brand_cost - generic_cost
        annual_savings = monthly_savings * 12
        savings_rows.append({
            "Drug": drug,
            "Monthly Savings": f"${monthly_savings}",
            "Annual Savings": f"${annual_savings}"
        })
    savings_df = pd.DataFrame(savings_rows)
    st.dataframe(savings_df)
