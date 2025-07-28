
import streamlit as st
import pandas as pd
import random

# Synthetic data for demonstration
drug_data = {
    "Atorvastatin": {"10mg": 12.50, "20mg": 15.00},
    "Lisinopril": {"10mg": 8.75, "20mg": 10.00},
    "Metformin": {"500mg": 5.00, "1000mg": 7.50}
}

pharmacies = [
    {"name": "HealthPlus Pharmacy", "type": "Retail", "distance": 2},
    {"name": "WellCare Pharmacy", "type": "Mail Order", "distance": 0},
    {"name": "CityMeds", "type": "Retail", "distance": 5},
    {"name": "PharmaDirect", "type": "Mail Order", "distance": 0}
]

insurance_plans = {
    "Plan A": 0.8,
    "Plan B": 0.7,
    "Plan C": 0.6
}

# Streamlit UI
st.title("💊 Real-Time Drug Cost Comparison Tool")
st.markdown("**Powered by synthetic NADAC & FDB datasets**")

# User Inputs
drug_name = st.selectbox("Select Drug Name", list(drug_data.keys()))
dosage = st.selectbox("Select Dosage", list(drug_data[drug_name].keys()))
zip_code = st.text_input("Enter ZIP Code", "12345")
insurance_plan = st.selectbox("Select Insurance Plan", list(insurance_plans.keys()))

# Sidebar Filters
st.sidebar.header("🔍 Filters")
max_distance = st.sidebar.slider("Maximum Distance (miles)", 0, 10, 5)
pharmacy_type = st.sidebar.multiselect("Pharmacy Type", ["Retail", "Mail Order"], default=["Retail", "Mail Order"])

# Calculate base price and copay
base_price = drug_data[drug_name][dosage]
coverage = insurance_plans[insurance_plan]
copay = round(base_price * (1 - coverage), 2)

# Generate results
results = []
for pharmacy in pharmacies:
    if pharmacy["distance"] <= max_distance and pharmacy["type"] in pharmacy_type:
        price_variation = round(random.uniform(-1.0, 1.0), 2)
        final_price = round(base_price + price_variation, 2)
        final_copay = round(final_price * (1 - coverage), 2)
        results.append({
            "Pharmacy": pharmacy["name"],
            "Type": pharmacy["type"],
            "Distance (mi)": pharmacy["distance"],
            "Price ($)": final_price,
            "Copay Estimate ($)": final_copay,
            "Formulary Status": "Covered" if final_price < 20 else "Not Covered"
        })

# Display results
st.subheader("📋 Comparison Results")
if results:
    df = pd.DataFrame(results)
    st.dataframe(df)

    # Alert for cheaper alternatives
    cheapest = min(results, key=lambda x: x["Price ($)"])
    if cheapest["Price ($)"] > 15:
        st.warning("💡 Consider asking your provider about generic alternatives to reduce cost.")
    else:
        st.success(f"✅ Best price found at {cheapest['Pharmacy']} for ${cheapest['Price ($)']}")
else:
    st.info("No pharmacies found matching your filters.")

# Footer
st.markdown("---")
st.caption("Synthetic data used for demonstration. Not for clinical or commercial use.")
