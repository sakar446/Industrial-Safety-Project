"""Reproduce the two worked examples in Lecture 21 (with stated rounding)."""
import math
from dispersion_models import plume_sigmas, puff_sigmas, concentration, concentration_to_ppmv


def run_validation():
    print("VALIDATION 1: Lecture 21 SO2 plume example")
    x, y, z = 500.0, 0.0, 0.0
    sy, sz = plume_sigmas(x, "D")
    c = float(concentration(
        "case10", x, y, z,
        mass_rate_kg_s=0.080, wind_speed=6.0,
        release_height_m=60.0, stability="D"
    ))
    c_cross = float(concentration(
        "case10", x, 50.0, z,
        mass_rate_kg_s=0.080, wind_speed=6.0,
        release_height_m=60.0, stability="D"
    ))
    print(f"sigma_y = {float(sy):.2f} m (lecture: 39.0 m)")
    print(f"sigma_z = {float(sz):.2f} m (lecture: 22.7 m)")
    print(f"C(500, 0, 0) = {c*1e3:.3e} g/m^3 (lecture: 1.45e-4 g/m^3)")
    print(f"C(500, 50, 0) = {c_cross*1e3:.3e} g/m^3 (lecture: 6.37e-5 g/m^3)")

    print("\nVALIDATION 2: Lecture 21 chlorine puff example")
    sx, sy, sz = puff_sigmas(500.0, "F")
    c_puff = float(concentration(
        "case9", 500.0, 0.0, 0.0,
        mass_kg=1.0, wind_speed=2.0, time_s=250.0, stability="F"
    ))
    ppm = float(concentration_to_ppmv(c_puff, 70.906, 298.0, 101325.0))
    print(f"arrival time = {500/2:.1f} s (lecture: 250 s)")
    print(f"sigma_x = sigma_y = {float(sx):.2f} m (lecture rounds to 5.0 m)")
    print(f"sigma_z = {float(sz):.2f} m (lecture rounds to 2.2 m)")
    print(f"centre concentration = {c_puff:.3e} kg/m^3")
    print(f"centre concentration = {ppm:.1f} ppmv (lecture: approximately 798 ppm after rounding sigmas)")


if __name__ == "__main__":
    run_validation()
