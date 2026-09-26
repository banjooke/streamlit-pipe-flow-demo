"""A simple pipe-flow calculator with SI unit conversions."""

import math

import streamlit as st


st.set_page_config(page_title="Pipe Flow Quick Check", layout="centered")
st.title("Pipe Flow Quick Check")
st.write("Estimate average velocity and flow regime for a full circular pipe.")

left, right = st.columns(2)
with left:
    flow_m3_h = st.number_input(
        "Volumetric flow rate (m³/h)", value=10.0, step=0.1, format="%.4f"
    )
    diameter_mm = st.number_input(
        "Internal pipe diameter (mm)", value=50.0, step=1.0, format="%.4f"
    )
with right:
    density = st.number_input(
        "Fluid density (kg/m³)", value=1000.0, step=1.0, format="%.4f"
    )
    viscosity_mpa_s = st.number_input(
        "Dynamic viscosity (mPa·s)", value=1.0, step=0.1, format="%.4f"
    )

inputs = {
    "Volumetric flow rate": flow_m3_h,
    "Internal pipe diameter": diameter_mm,
    "Fluid density": density,
    "Dynamic viscosity": viscosity_mpa_s,
}
invalid = [name for name, value in inputs.items() if not math.isfinite(value) or value <= 0]

if invalid:
    st.error("Enter a finite value greater than zero for: " + ", ".join(invalid) + ".")
else:
    # Convert to SI units; density is already in kg/m³.
    flow = flow_m3_h / 3600.0
    diameter = diameter_mm / 1000.0
    viscosity = viscosity_mpa_s / 1000.0
    try:
        area = math.pi * diameter**2 / 4.0
        velocity = flow / area
        reynolds = density * velocity * diameter / viscosity
        if not all(math.isfinite(value) and value > 0 for value in (area, velocity, reynolds)):
            raise ValueError("Results outside numerical range")
    except (OverflowError, ZeroDivisionError, ValueError):
        st.error("These inputs exceed the calculator's numerical range. Use less extreme values.")
    else:
        if reynolds < 2300:
            regime = "Laminar"
        elif reynolds < 4000:
            regime = "Transitional"
        else:
            regime = "Turbulent"

        st.subheader("Results")
        area_card, velocity_card = st.columns(2)
        area_card.metric("Pipe cross-sectional area (m²)", f"{area:.6g}")
        velocity_card.metric("Average flow velocity (m/s)", f"{velocity:.6g}")
        reynolds_card, regime_card = st.columns(2)
        reynolds_card.metric("Reynolds number (dimensionless)", f"{reynolds:.6g}")
        regime_card.metric("Flow regime", regime)

with st.expander("Equations and unit conversions"):
    st.markdown("**Convert inputs to SI units**")
    st.latex(r"Q\,[\mathrm{m^3/s}] = Q\,[\mathrm{m^3/h}] / 3600")
    st.latex(r"D\,[\mathrm{m}] = D\,[\mathrm{mm}] / 1000")
    st.latex(r"\mu\,[\mathrm{Pa\cdot s}] = \mu\,[\mathrm{mPa\cdot s}] / 1000")
    st.markdown("Density $\\rho$ is already in SI units (kg/m³).")
    st.markdown("**Calculate area, average velocity, and Reynolds number**")
    st.latex(r"A = \frac{\pi D^2}{4}, \qquad v = \frac{Q}{A}, \qquad \mathrm{Re} = \frac{\rho v D}{\mu}")
    st.markdown(
        "Here, $A$ is area (m²), $v$ is average velocity (m/s), and Re is dimensionless.\n\n"
        "- **Laminar:** Re < 2300\n"
        "- **Transitional:** 2300 ≤ Re < 4000\n"
        "- **Turbulent:** Re ≥ 4000"
    )

st.caption(
    "Engineering disclaimer: This preliminary check assumes steady flow of a Newtonian "
    "fluid in a full circular pipe. It does not assess pressure loss or establish design "
    "safety; verify assumptions and results before engineering use."
)
