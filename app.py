from __future__ import annotations

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import streamlit as st

from dispersion_models import (
    MODEL_NAMES, CONTINUOUS_CASES, PUFF_CASES, NO_WIND_CASES,
    concentration, concentration_to_ppmv, concentration_to_mg_m3,
    plume_sigmas, puff_sigmas, arrival_time_s,
)

st.set_page_config(page_title="ToxiDisp | Gas Dispersion Predictor", page_icon="🌫️", layout="wide")
st.title("ToxiDisp – Atmospheric Toxic Gas Dispersion Predictor")
st.caption("Educational project based on the dispersion models in Lectures 19–21. All calculations use SI units internally.")

with st.sidebar:
    st.header("1. Model selection")
    model_keys = list(MODEL_NAMES.keys())
    model = st.selectbox("Select lecture model", model_keys, format_func=lambda k: MODEL_NAMES[k], index=9)
    st.divider()
    st.header("2. Chemical and toxic threshold")
    chemical_default = "Chlorine" if model == "case9" else "Sulfur dioxide"
    mw_default = 70.906 if model == "case9" else 64.066
    chemical = st.text_input("Chemical name", chemical_default, key=f"chemical_{model}")
    mw = st.number_input("Molecular weight (g/mol)", min_value=0.001, value=mw_default, step=0.1, format="%.3f", key=f"mw_{model}")
    threshold_ppm = st.number_input("Concentration threshold (ppmv)", min_value=0.001, value=1.0, step=0.5, key=f"threshold_{model}", help="Enter a substance-specific value from an authoritative source. The lecture's chlorine example uses ERPG-1 = 1 ppm.")
    temperature_c = st.number_input("Ambient temperature (°C)", min_value=-50.0, max_value=80.0, value=25.0, step=1.0)
    pressure_kpa = st.number_input("Ambient pressure (kPa)", min_value=1.0, max_value=200.0, value=101.325, step=1.0)
    st.divider()
    st.header("3. Release and weather inputs")

    if model in CONTINUOUS_CASES:
        q_g_s = st.number_input("Continuous release rate (g/s)", min_value=0.0001, value=80.0 if model == "case10" else 10.0, step=1.0, format="%.4f")
        mass_kg = 1.0
    else:
        mass_kg = st.number_input("Instantaneously released mass (kg)", min_value=0.000001, value=1.0, step=0.1, format="%.6f")
        q_g_s = 10.0

    wind_required = model not in {"case1", "case2", "case3", "case6"}
    if wind_required:
        wind_speed = st.number_input("Wind speed (m/s)", min_value=0.001, value=6.0 if model == "case10" else 2.0, step=0.1)
    else:
        wind_speed = 0.0
        st.caption("This lecture case assumes no wind; wind speed is fixed at 0 m/s.")

    time_required = model in {"case2", "case3", "case5", "case6", "case9"}
    if time_required:
        time_s = st.number_input("Time since release (s)", min_value=0.001, value=250.0 if model == "case9" else 60.0, step=1.0)
    else:
        time_s = 60.0

    if model in {"case8", "case10"}:
        release_height = st.number_input("Effective release height (m)", min_value=0.0, value=60.0 if model == "case10" else 10.0, step=1.0)
    else:
        release_height = 0.0

    stability = "D"
    if model in {"case9", "case10"}:
        stability = st.selectbox("Pasquill–Gifford stability class", ["A", "B", "C", "D", "E", "F"], index=3 if model == "case10" else 5)
        st.caption("The supplied lecture correlations are for rural conditions; the app uses those coefficients.")

    k_iso = 10.0
    kx, ky, kz = 10.0, 5.0, 2.0
    if model in {"case1", "case2", "case3", "case4"}:
        k_iso = st.number_input("Isotropic eddy diffusivity K (m²/s)", min_value=0.0001, value=10.0, step=1.0)
    if model in {"case5", "case6", "case7", "case8"}:
        st.caption("Eddy diffusivities are model inputs; the lectures do not provide universal values.")
        kx = st.number_input("Kx (m²/s)", min_value=0.0001, value=10.0, step=1.0)
        ky = st.number_input("Ky (m²/s)", min_value=0.0001, value=5.0, step=1.0)
        kz = st.number_input("Kz (m²/s)", min_value=0.0001, value=2.0, step=1.0)

st.subheader("4. Concentration at a selected point")
point_col1, point_col2, point_col3 = st.columns(3)
with point_col1:
    x_point = st.number_input("Downwind / x coordinate (m)", min_value=-100000.0, value=500.0, step=10.0)
with point_col2:
    y_point = st.number_input("Crosswind / y coordinate (m)", min_value=-100000.0, value=0.0, step=10.0)
with point_col3:
    z_point = st.number_input("Height / z coordinate (m)", min_value=0.0, value=0.0, step=1.0)

st.subheader("5. Concentration contour map")
plot_col1, plot_col2, plot_col3 = st.columns(3)
with plot_col1:
    max_x = st.number_input("Maximum x extent (m)", min_value=100.0, max_value=20000.0, value=2000.0, step=100.0)
with plot_col2:
    max_y = st.number_input("Crosswind half-width (m)", min_value=25.0, max_value=10000.0, value=500.0, step=25.0)
with plot_col3:
    grid_n = st.select_slider("Grid resolution", options=[40, 60, 80, 100, 120, 150, 200], value=100)

st.info("The contour plot is a ground-level (z = 0) snapshot/field. The selected-point calculation uses your entered z coordinate.")

run = st.button("Run dispersion simulation", type="primary", use_container_width=True)

if run:
    try:
        q_kg_s = q_g_s / 1000.0
        temp_k = temperature_c + 273.15
        pressure_pa = pressure_kpa * 1000.0
        c_point = float(concentration(
            model, x_point, y_point, z_point,
            mass_rate_kg_s=q_kg_s, mass_kg=mass_kg,
            wind_speed=wind_speed, time_s=time_s,
            release_height_m=release_height,
            k_iso=k_iso, kx=kx, ky=ky, kz=kz,
            stability=stability,
        ))
        point_ppm = float(concentration_to_ppmv(c_point, mw, temp_k, pressure_pa))
        point_mg = float(concentration_to_mg_m3(c_point))

        st.markdown("### Selected-point result")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Concentration", f"{c_point:.4e} kg/m³")
        m2.metric("Concentration", f"{point_mg:.4g} mg/m³")
        m3.metric("Concentration", f"{point_ppm:.4g} ppmv")
        m4.metric("Threshold comparison", "EXCEEDS" if point_ppm >= threshold_ppm else "Below threshold")
        st.write(f"At **x = {x_point:g} m, y = {y_point:g} m, z = {z_point:g} m**, the predicted concentration of **{chemical}** is **{point_ppm:.4g} ppmv** against the user-entered threshold of **{threshold_ppm:g} ppmv**.")

        # Grid domain: symmetric for no-wind cases; downwind domain for wind-driven models.
        if model in NO_WIND_CASES:
            x_values = np.linspace(-max_x, max_x, grid_n)
        else:
            x_values = np.linspace(0.0, max_x, grid_n)
        y_values = np.linspace(-max_y, max_y, grid_n)
        X, Y = np.meshgrid(x_values, y_values)
        C = concentration(
            model, X, Y, 0.0,
            mass_rate_kg_s=q_kg_s, mass_kg=mass_kg,
            wind_speed=wind_speed, time_s=time_s,
            release_height_m=release_height,
            k_iso=k_iso, kx=kx, ky=ky, kz=kz,
            stability=stability,
        )
        Cppm = concentration_to_ppmv(C, mw, temp_k, pressure_pa)
        finite = np.isfinite(Cppm)
        Cppm_plot = np.where(finite, Cppm, np.nan)
        cmax = float(np.nanmax(Cppm_plot)) if np.any(finite) else 0.0
        dx = float(x_values[1] - x_values[0]) if len(x_values) > 1 else 0.0
        dy = float(y_values[1] - y_values[0]) if len(y_values) > 1 else 0.0
        affected = finite & (Cppm_plot >= threshold_ppm)
        affected_area = float(np.count_nonzero(affected) * abs(dx * dy))

        if np.any(affected):
            if model in NO_WIND_CASES:
                radius = np.sqrt(X[affected] ** 2 + Y[affected] ** 2)
                reach = float(np.nanmax(radius))
                reach_label = "Farthest affected radius in plotted domain"
            else:
                reach = float(np.nanmax(X[affected]))
                reach_label = "Farthest downwind affected distance in plotted domain"
        else:
            reach = 0.0
            reach_label = "Farthest affected distance"

        st.markdown("### Affected-zone assessment")
        r1, r2, r3 = st.columns(3)
        r1.metric("Maximum ground-level concentration", f"{cmax:.4g} ppmv")
        r2.metric("Estimated affected area", f"{affected_area:,.0f} m²")
        r3.metric(reach_label, f"{reach:,.1f} m")
        if np.any(affected):
            st.warning(f"At the selected threshold of {threshold_ppm:g} ppmv, some cells in the plotted domain are above the threshold. The area and distance are grid-based estimates limited to the plotted domain.")
        else:
            st.success("No grid cell in the plotted domain exceeded the selected threshold.")

        fig, ax = plt.subplots(figsize=(10, 6))
        if cmax > 0:
            floor = max(cmax * 1e-6, 1e-30)
            levels = np.geomspace(floor, max(cmax, floor * 1.01), 24)
            positive = np.ma.masked_where((~np.isfinite(Cppm_plot)) | (Cppm_plot <= 0), Cppm_plot)
            contour = ax.contourf(X, Y, positive, levels=levels, norm=LogNorm(vmin=floor, vmax=max(cmax, floor * 1.01)), cmap="viridis", extend="max")
            cbar = fig.colorbar(contour, ax=ax)
            cbar.set_label("Concentration (ppmv, logarithmic scale)")
            if np.nanmin(Cppm_plot) <= threshold_ppm <= np.nanmax(Cppm_plot):
                ax.contour(X, Y, Cppm_plot, levels=[threshold_ppm], colors="red", linewidths=2)
                ax.plot([], [], color="red", linewidth=2, label=f"Threshold = {threshold_ppm:g} ppmv")
                ax.legend(loc="upper right")
        else:
            ax.text(0.5, 0.5, "No positive concentration values in this domain", transform=ax.transAxes, ha="center")
        ax.scatter([0], [0], marker="*", s=150, color="red", edgecolor="black", label="Release point")
        ax.set_xlabel("Downwind / x coordinate (m)" if model not in NO_WIND_CASES else "x coordinate (m)")
        ax.set_ylabel("Crosswind / y coordinate (m)")
        ax.set_title(f"{MODEL_NAMES[model]} – ground-level concentration")
        ax.grid(alpha=0.2)
        ax.legend(loc="best")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Optional model-specific supporting values.
        if model == "case10":
            sy, sz = plume_sigmas(max(x_point, 1.0), stability)
            st.caption(f"At x = {max(x_point, 1.0):g} m: σy = {float(sy):.3f} m, σz = {float(sz):.3f} m (rural P-G plume correlations).")
        elif model == "case9":
            sx, sy, sz = puff_sigmas(max(wind_speed * time_s, 1.0), stability)
            st.caption(f"At puff-centre travel distance ut = {wind_speed*time_s:g} m: σx = {float(sx):.3f} m, σy = {float(sy):.3f} m, σz = {float(sz):.3f} m (rural P-G puff correlations).")

        if model in {"case9", "case10"}:
            st.caption("Pasquill–Gifford assumptions: neutrally buoyant gas, turbulent mixing dominant, rural coefficient correlations, and lecture-stated limitations (typically 0.1–10 km; averaged concentrations). This is not a dense-gas CFD model.")
        if model in {"case1", "case3", "case4"} and np.isnan(c_point):
            st.caption("The ideal point-source solution is singular at the exact release point; choose a non-zero distance.")

        # CSV export for the plotted ground-level field.
        export_df = pd.DataFrame({
            "x_m": X.ravel(),
            "y_m": Y.ravel(),
            "concentration_kg_m3": np.asarray(C).ravel(),
            "concentration_ppmv": np.asarray(Cppm).ravel(),
            "above_threshold": affected.ravel(),
        })
        st.download_button(
            "Download contour data (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="toxidisp_contour_data.csv",
            mime="text/csv",
        )

        if model in {"case9", "case2", "case5", "case6"}:
            if wind_speed > 0:
                travel = arrival_time_s(max(x_point, 0.0), wind_speed)
                st.caption(f"Simple advective travel-time estimate to x = {max(x_point,0):g} m: {travel:.2f} s ({travel/60:.2f} min). This uses x/u and does not account for turbulent cloud-front spread.")
            else:
                st.caption("No-wind case selected; the cloud does not have a wind-driven arrival time.")

    except Exception as exc:
        st.error(f"Could not run the simulation: {exc}")

with st.expander("Model assumptions and limitations – read before interpreting results"):
    st.markdown("""
    - The application implements the idealised equations and assumptions presented in the supplied Lectures 19–21.
    - Gaussian/Pasquill–Gifford models assume neutrally buoyant dispersion with turbulent mixing dominant. They are not suitable as a substitute for dense-gas models for heavy gases near a release.
    - Lecture 20 gives a typical Gaussian applicability distance of approximately 0.1–10 km and describes predicted concentrations as time averages; short-lived local peaks can be higher.
    - Rural Pasquill–Gifford coefficient correlations are used. The code does not infer stability class automatically; the user selects A–F.
    - Eddy diffusivities K, Kx, Ky and Kz are user inputs. The lecture slides do not establish universal default values.
    - The toxic threshold is user-entered. Only the chlorine example in Lecture 21 explicitly gives ERPG-1 = 1 ppm. Confirm chemical-specific ERPG/AEGL/IDLH values from authoritative sources before using them.
    - A threshold contour is a screening visualization, not an evacuation boundary or a real emergency-response recommendation. Actual incidents require qualified emergency responders and validated site-specific tools.
    """)

st.markdown("---")
st.caption("Academic demonstration only • Not for live emergency response, siting decisions, or safety-critical design.")
