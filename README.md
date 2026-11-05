# ToxiDisp – Atmospheric Toxic Gas Dispersion Predictor

A beginner-friendly Python/Streamlit academic project based on the three supplied Process Safety lecture PDFs (Lectures 19–21). The application predicts gas concentration from idealised point releases, plots ground-level concentration contours, and compares the modelled concentration with a user-entered threshold.

> **Important:** This is an educational demonstration, not an emergency-response tool. Do not use it to decide evacuations, define real exclusion zones, or make safety-critical decisions.

## What is included

- `app.py` – Streamlit user interface.
- `dispersion_models.py` – the ten dispersion cases from Lecture 20, plus the elevated Gaussian plume form used in Lecture 21.
- `toxicity.py` – ppmv threshold comparison helpers.
- `validation.py` – numerical checks against the SO2 and chlorine worked examples in Lecture 21.
- `test_models.py` – basic software tests.
- `Project_Report.docx` – project report with placeholders for group/college details.
- `PRESENTATION_GUIDE.md` – suggested 8-slide presentation flow, member division, and viva prompts.
- `requirements.txt` – Python dependencies.

## Easiest way to run it (Windows)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ . During installation, tick **Add Python to PATH**.
2. Extract the ZIP file to a normal folder, for example `Desktop\ToxiDisp_Project`.
3. Open that folder in File Explorer. Click the address bar, type `cmd`, and press Enter.
4. Create a virtual environment (recommended):

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install the required libraries:

   ```bash
   py -m pip install -r requirements.txt
   ```

6. Start the application:

   ```bash
   py -m streamlit run app.py
   ```

7. A browser tab should open. If it does not, copy the local URL printed in Command Prompt (usually `http://localhost:8501`).

To stop the app, return to Command Prompt and press `Ctrl + C`.

## Run the validation checks

In the same activated environment:

```bash
py validation.py
py -m unittest test_models.py
```

The validation script reproduces the Lecture 21 SO2 stack example and the chlorine puff example. The chlorine lecture calculation rounds the dispersion coefficients to 5.0 m and 2.2 m before obtaining approximately 798 ppm; the code retains full precision and therefore gives a slightly different value.

## How to use the application

1. Select one of the ten lecture models in the sidebar.
2. Enter the chemical name and molecular weight.
3. Enter either a continuous release rate (g/s) or an instantaneous released mass (kg), depending on the selected model.
4. Enter wind speed, release height, time, eddy diffusivities, or stability class as requested by the selected model.
5. Enter the point coordinates `(x, y, z)` to obtain a concentration at that location.
6. Set the contour-map dimensions and press **Run dispersion simulation**.
7. Read the concentration in kg/m³, mg/m³ and ppmv; inspect the threshold comparison and contour plot; download the contour grid as CSV if needed.

## Model list

| Case | Implemented model | Main inputs |
|---|---|---|
| 1 | Steady continuous point source, no wind | Q, isotropic K |
| 2 | Instantaneous puff, no wind | M, K, time |
| 3 | Non-steady continuous source, no wind | Q, K, time |
| 4 | Steady continuous point source with wind, no ground boundary | Q, K, wind |
| 5 | Instantaneous puff with wind and anisotropic K | M, Kx, Ky, Kz, wind, time |
| 6 | Instantaneous ground-level puff, no wind | M, Kx, Ky, Kz, time |
| 7 | Steady ground-level plume with wind | Q, Kx, Ky, Kz, wind |
| 8 | Elevated continuous source with ground reflection | Q, Kx, Ky, Kz, wind, height |
| 9 | Pasquill–Gifford Gaussian puff | M, wind, time, stability |
| 10 | Pasquill–Gifford Gaussian plume (ground-source Case 10; elevated reflected form from Lecture 21 also available) | Q, wind, stability, release height |

## Coordinate convention

- `x`: downwind coordinate measured from the release point. In no-wind models it is simply the Cartesian x-coordinate.
- `y`: crosswind coordinate.
- `z`: height above ground.
- Wind direction is assumed to align with the positive x-axis. The plot therefore shows local downwind/crosswind coordinates, not a geographic map.

## Units and conversions

- Mass release rate: entered in g/s and converted to kg/s.
- Instantaneous mass: kg.
- Distances: m.
- Wind speed: m/s.
- Eddy diffusivity: m²/s.
- Concentration: internally kg/m³, also displayed as mg/m³ and ppmv.
- ppmv conversion uses the ideal-gas relation with the entered molecular weight, temperature and pressure.

## Assumptions and limitations

- The model equations and coefficient tables are based on Lectures 19–21.
- Pasquill–Gifford calculations use the **rural** coefficient correlations transcribed from the supplied slides. The atmospheric stability class is selected by the user; it is not inferred automatically from weather data.
- Eddy diffusivities are user inputs. The lecture slides do not specify universal values; the interface's starter values must be replaced with values appropriate to a chosen study scenario.
- Case 9 uses the ground-image normalization shown by the Lecture 21 chlorine example. Its puff dispersion coefficients are evaluated at the puff-centre travel distance `u*t`, with a 1 m numerical floor to avoid zero-width coefficients at the release instant.
- The Lecture 21 chlorine ERPG-1 value of 1 ppm is an example-specific input, not a universal chlorine safety value for all jurisdictions or exposure durations. The app accepts a user-entered threshold and does not provide a chemical regulatory database.
- The Gaussian models assume neutrally buoyant dispersion and turbulent mixing. They are not dense-gas models for heavy-gas slumping, aerosol/liquid droplet behaviour, complex terrain, buildings, chemical reactions, deposition, or time-varying meteorology.
- Lecture 20 describes typical Gaussian model use over approximately 0.1–10 km and notes that model predictions are time-averaged.
- The affected area is a grid-based estimate within the user-selected plotting domain. It is not an official hazard or evacuation boundary.

## References

1. `Lecture 19-Dispersion model.pdf`, supplied class lecture slides: introduction, consequence analysis, atmospheric stability and dispersion parameters.
2. `Lecture 20-Dispersion model-2.pdf`, supplied class lecture slides: Cases 1–10, Pasquill–Gifford coefficients, worst-case conditions and limitations.
3. `Lecture 21-Dispersion model-3.pdf`, supplied class lecture slides: ERPG criteria, SO2 and chlorine worked examples, buoyancy/momentum and mitigation.
