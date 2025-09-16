import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------------
# Default dataset (simplified)
default_data = {
    "Aluminium (Raw)": 16,
    "Aluminium (Recycled)": 4,
    "Copper (Raw)": 8,
    "Copper (Recycled)": 2,
}

# ---------------------
# Title
st.title("AI-Driven LCA Tool for Circularity in Metallurgy & Mining")
st.caption("Prototype developed for Smart India Hackathon 2025")

st.markdown(
    """
    This AI-powered tool helps estimate **Life Cycle Assessment (LCA)** and **Circularity Scores**  
    for metals like Aluminium and Copper, aligned with Government of India’s sustainability goals.
    """
)

# ---------------------
# User Inputs
metal = st.selectbox("Select Metal", ["Aluminium", "Copper"])
route = st.selectbox("Production Route", ["Raw", "Recycled", "Mixed"])
energy = st.selectbox("Energy Source", ["Coal-based", "Renewable", "Mixed"])
transport = st.slider("Transport Distance (km)", 10, 2000, 100)
recycled_content = st.slider("Recycled Content (%)", 0, 100, 30)
end_of_life = st.selectbox("End-of-Life Option", ["Landfill", "Recycling", "Reuse"])

# ---------------------
# AI-style gap filling (calculation logic)
if route == "Mixed":
    co2 = (default_data[f"{metal} (Raw)"] * (100 - recycled_content) / 100) + \
          (default_data[f"{metal} (Recycled)"] * recycled_content / 100)
else:
    co2 = default_data[f"{metal} ({route})"]

# Adjust for energy
if energy == "Coal-based":
    co2 *= 1.2
elif energy == "Renewable":
    co2 *= 0.8

# Adjust for transport
co2 += transport * 0.01

# Circularity Score (simple formula for demo)
circularity = recycled_content * 0.5
if end_of_life == "Recycling":
    circularity += 30
elif end_of_life == "Reuse":
    circularity += 40

circularity = min(100, circularity)

# ---------------------
# Results
st.subheader("Results")
st.write(f"**Estimated CO₂ Emissions:** {co2:.2f} kg CO₂ per kg {metal}")
st.write(f"**Circularity Score:** {circularity:.1f}/100")

if co2 < 5:
    st.success("✅ Meets sustainability threshold under India’s Net-Zero 2070 vision.")
else:
    st.warning("⚠️ High emissions – improvement needed for policy compliance.")

# ---------------------
# Chart
fig, ax = plt.subplots()
ax.bar(["CO₂ Emissions", "Circularity Score"], [co2, circularity], color=["red", "green"])
ax.set_ylabel("Value")
st.pyplot(fig)

# ---------------------
# PDF Export
if st.button("Export Report as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "AI-Driven LCA Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Metal: {metal}", ln=True)
    pdf.cell(200, 10, f"Production Route: {route}", ln=True)
    pdf.cell(200, 10, f"Energy Source: {energy}", ln=True)
    pdf.cell(200, 10, f"Transport Distance: {transport} km", ln=True)
    pdf.cell(200, 10, f"Recycled Content: {recycled_content}%", ln=True)
    pdf.cell(200, 10, f"End-of-Life Option: {end_of_life}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, f"Estimated CO₂: {co2:.2f} kg CO₂/kg", ln=True)
    pdf.cell(200, 10, f"Circularity Score: {circularity:.1f}/100", ln=True)
    pdf.output("LCA_Report.pdf")
    st.success("Report exported as **LCA_Report.pdf**")
