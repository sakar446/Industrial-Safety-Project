# ToxiDisp presentation guide

## Suggested 8-slide presentation

1. **Title and team** – ToxiDisp: Atmospheric Toxic Gas Dispersion Predictor. Add course, department, faculty name, all four group members and roll numbers.
2. **Problem statement** – Accidental toxic releases can form a moving plume or puff. The project predicts concentration and visualises a threshold-exceedance zone.
3. **Dispersion fundamentals** – Explain wind transport, turbulent mixing, atmospheric stability, ground conditions and release height.
4. **Models implemented** – Show the distinction between continuous plume and instantaneous puff. Mention all ten lecture cases, with focus on Cases 9 and 10 (Pasquill–Gifford).
5. **Software architecture** – User inputs → model selection → concentration engine → ppm conversion/threshold check → contour plot and CSV output.
6. **Demonstration 1: SO2 plume** – Use Lecture 21 data: 80 g/s, effective height 60 m, wind 6 m/s, rural, class D. At 500 m centreline, expected concentration is about 1.45 × 10^-4 g/m³; 50 m crosswind is about 6.37 × 10^-5 g/m³. The lecture estimates maximum ground-level concentration around 1200 m at about 4.18 × 10^-4 g/m³.
7. **Demonstration 2: chlorine puff** – Use Lecture 21 data: 1 kg instantaneous chlorine release at ground level, wind 2 m/s, residential area 500 m away. Advective arrival estimate is 250 s (4.17 min). The lecture's class-F example uses ERPG-1 = 1 ppm and estimates a high centre concentration.
8. **Conclusion, limitations and future work** – State the neutrally buoyant assumption, rural coefficient use, no dense-gas CFD, grid-limited impact area, and possible future work (wind-direction rotation, time-varying wind, dense-gas model, GIS map, chemical-property database).

## Suggested four-member division

- **Member 1 – Theory:** Explain the transport equation and Cases 1–8; check the eddy-diffusivity equations.
- **Member 2 – Gaussian models:** Explain P-G plume/puff models and coefficient tables; validate the Lecture 21 examples.
- **Member 3 – Software:** Demonstrate inputs, model selection, point concentration and contour plots.
- **Member 4 – Toxic effects/integration:** Explain ppm conversion, threshold comparison, affected area, limitations and conclusion.

All members should understand the overall flow and be able to explain what the app takes as input and returns as output.

## Likely viva questions

**1. What is dispersion?**

The transport and spreading of released material in the atmosphere due to mean wind and turbulent mixing.

**2. What is the difference between plume and puff?**

A plume represents a continuous release (mass per time); a puff represents a fixed mass released instantaneously.

**3. What is atmospheric stability?**

A description of the atmosphere's tendency to enhance or suppress vertical mixing. The lecture uses classes A–F, from extremely unstable to moderately stable.

**4. What are sigma-y and sigma-z?**

Pasquill–Gifford dispersion coefficients describing horizontal crosswind and vertical spread, respectively.

**5. Why does wind speed matter?**

It controls downwind advection and appears in the denominator of the steady Gaussian plume expression; for a fixed release and other inputs, lower wind speed can increase predicted concentrations.

**6. What does ERPG-1/2/3 mean?**

The three emergency-response concentration guideline levels described in Lecture 21, for mild effects, serious/irreversible effects or impaired protective action, and life-threatening effects respectively. They are exposure-duration-specific criteria, not generic limits for every duration.

**7. Why convert kg/m³ to ppm?**

Toxic-effect criteria are often reported as volume fractions (ppmv), while dispersion equations return mass concentration. The conversion requires molecular weight, temperature and pressure.

**8. What is the main limitation of your application?**

The Gaussian/P-G approach assumes neutrally buoyant gas and simplified meteorology/terrain. It does not simulate dense-gas behaviour, complex buildings, chemical reactions or time-varying weather.

**9. What is a contour plot?**

A map of equal concentration values. The selected threshold contour bounds the region where predicted concentration is at or above the user-entered threshold.

**10. Is this suitable for an actual chlorine emergency?**

No. It is an academic screening demonstration. A real event requires trained emergency responders and validated, site-specific models and procedures.
