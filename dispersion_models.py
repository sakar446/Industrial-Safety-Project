"""Atmospheric toxic-gas dispersion models based on the user's Lecture 19-21 PDFs.

All internal concentrations are returned in kg/m^3.
Coordinates are local to the release point: x is downwind, y is crosswind,
and z is height above ground. For no-wind models x/y are ordinary Cartesian
coordinates. SI units are used throughout.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy.special import erfc

PI = np.pi

# Rural Pasquill-Gifford coefficients transcribed from Lecture 21, Table 5-2.
# sigma_y = a_y*x*(1+b_y*x)^(-p_y)
# sigma_z = a_z*x*(1+b_z*x)^(-p_z)
PLUME_PG = {
    "A": (0.22, 0.0001, 0.5, 0.20, 0.0, 0.0),
    "B": (0.16, 0.0001, 0.5, 0.12, 0.0, 0.0),
    "C": (0.11, 0.0001, 0.5, 0.08, 0.0002, 0.5),
    "D": (0.08, 0.0001, 0.5, 0.06, 0.0015, 0.5),
    "E": (0.06, 0.0001, 0.5, 0.03, 0.0003, 1.0),
    "F": (0.04, 0.0001, 0.5, 0.016, 0.0003, 1.0),
}

# Rural Pasquill-Gifford coefficients transcribed from Lecture 20, Table 5-3.
# The first column is sigma_y or sigma_x, as stated in the lecture.
PUFF_PG = {
    "A": (0.18, 0.92, 0.60, 0.75),
    "B": (0.14, 0.92, 0.53, 0.73),
    "C": (0.10, 0.92, 0.34, 0.71),
    "D": (0.06, 0.92, 0.15, 0.70),
    "E": (0.04, 0.92, 0.10, 0.65),
    "F": (0.02, 0.89, 0.05, 0.61),
}

MODEL_NAMES = {
    "case1": "Case 1 - Steady continuous point release, no wind",
    "case2": "Case 2 - Instantaneous puff, no wind",
    "case3": "Case 3 - Non-steady continuous point release, no wind",
    "case4": "Case 4 - Steady continuous point release, wind, no ground boundary",
    "case5": "Case 5 - Instantaneous puff with wind (anisotropic eddy diffusivity)",
    "case6": "Case 6 - Instantaneous puff, no wind, ground-level source",
    "case7": "Case 7 - Steady plume, ground-level source (eddy diffusivity)",
    "case8": "Case 8 - Steady elevated source with ground reflection (eddy diffusivity)",
    "case9": "Case 9 - Gaussian puff, ground-level source (Pasquill-Gifford)",
    "case10": "Case 10 / Lecture 21 - Gaussian plume (ground or elevated; Pasquill-Gifford)",
}

CONTINUOUS_CASES = {"case1", "case3", "case4", "case7", "case8", "case10"}
PUFF_CASES = {"case2", "case5", "case6", "case9"}
NO_WIND_CASES = {"case1", "case2", "case3", "case6"}


def _as_array(v):
    return np.asarray(v, dtype=float)


def _safe_exp(v):
    # Avoid harmless floating-point overflow/underflow in extreme user inputs.
    return np.exp(np.clip(v, -745.0, 100.0))


def plume_sigmas(x_m, stability: str):
    """Return rural Pasquill-Gifford plume sigma_y and sigma_z in metres.

    x_m is downwind distance in metres, in accordance with Lecture 21 Table 5-2.
    """
    if stability not in PLUME_PG:
        raise ValueError("Stability class must be A, B, C, D, E or F.")
    x = np.maximum(_as_array(x_m), 1e-9)
    ay, by, py, az, bz, pz = PLUME_PG[stability]
    sy = ay * x / np.power(1.0 + by * x, py)
    sz = az * x / np.power(1.0 + bz * x, pz)
    return sy, sz


def puff_sigmas(distance_m, stability: str):
    """Return Gaussian-puff sigma_x (=sigma_y) and sigma_z in metres.

    Lecture 20 Table 5-3 uses downwind distance x in metres. For a puff snapshot,
    the implementation evaluates the coefficients at the puff-centre travel
    distance x_c = u*t. A minimum of 1 m avoids zero-width coefficients at t=0.
    """
    if stability not in PUFF_PG:
        raise ValueError("Stability class must be A, B, C, D, E or F.")
    x = np.maximum(_as_array(distance_m), 1.0)
    ax, px, az, pz = PUFF_PG[stability]
    sx = ax * np.power(x, px)
    sz = az * np.power(x, pz)
    return sx, sx.copy(), sz


def concentration(model: str, x, y, z=0.0, *,
                  mass_rate_kg_s=0.01, mass_kg=1.0, wind_speed=2.0,
                  time_s=60.0, release_height_m=0.0,
                  k_iso=10.0, kx=10.0, ky=5.0, kz=2.0,
                  stability="D"):
    """Calculate concentration in kg/m^3 for one of the ten lecture cases.

    Inputs can be scalars or broadcast-compatible NumPy arrays.
    The equations follow Lecture 20 Cases 1-10 and Lecture 21's reflected
    Gaussian plume expression. Case 10 is the ground-source special case;
    a non-zero release_height_m invokes the elevated reflected plume equation
    introduced in Lecture 21 (Eqs. 5-49/5-50).
    """
    if model not in MODEL_NAMES:
        raise ValueError(f"Unknown model: {model}")
    X, Y, Z = np.broadcast_arrays(_as_array(x), _as_array(y), _as_array(z))
    r = np.sqrt(X * X + Y * Y + Z * Z)
    Q = float(mass_rate_kg_s)
    M = float(mass_kg)
    u = float(wind_speed)
    t = float(time_s)
    H = float(release_height_m)
    K = float(k_iso)
    Kx, Ky, Kz = float(kx), float(ky), float(kz)

    if model in {"case1", "case2", "case3", "case4"} and K <= 0:
        raise ValueError("Isotropic eddy diffusivity K must be greater than zero.")
    if model in {"case5", "case6", "case7", "case8"} and min(Kx, Ky, Kz) <= 0:
        raise ValueError("Kx, Ky and Kz must all be greater than zero.")
    if model in {"case2", "case3", "case5", "case6", "case9"} and t <= 0:
        raise ValueError("Time since release must be greater than zero for this model.")
    if model in {"case4", "case5", "case7", "case8", "case9", "case10"} and u < 0:
        raise ValueError("Wind speed must be zero or positive; use wind direction separately.")

    if model == "case1":
        # C = Qm/(4*pi*K*r), steady source in an infinite medium, no wind.
        with np.errstate(divide="ignore", invalid="ignore"):
            C = Q / (4.0 * PI * K * r)
        return np.where(r > 0, C, np.nan)

    if model == "case2":
        # C = M/[8*(pi*K*t)^(3/2)] * exp[-r^2/(4*K*t)]
        pref = M / (8.0 * np.power(PI * K * t, 1.5))
        return pref * _safe_exp(-(r * r) / (4.0 * K * t))

    if model == "case3":
        # C = Q/[4*pi*K*r] * erfc[r/(2*sqrt(K*t))]
        with np.errstate(divide="ignore", invalid="ignore"):
            C = Q / (4.0 * PI * K * r) * erfc(r / (2.0 * np.sqrt(K * t)))
        return np.where(r > 0, C, np.nan)

    if model == "case4":
        # C = Q/[4*pi*K*r] * exp[-u/(2*K)*(r-x)]
        with np.errstate(divide="ignore", invalid="ignore"):
            C = Q / (4.0 * PI * K * r) * _safe_exp(-u * (r - X) / (2.0 * K))
        return np.where(r > 0, C, np.nan)

    if model == "case5":
        # Anisotropic moving puff in an unbounded domain.
        denom = 8.0 * np.power(PI * t, 1.5) * np.sqrt(Kx * Ky * Kz)
        exponent = -0.25 / t * (((X - u * t) ** 2) / Kx + Y ** 2 / Ky + Z ** 2 / Kz)
        return M / denom * _safe_exp(exponent)

    if model == "case6":
        # Ground-level puff with image source: factor 2 relative to free-space puff.
        denom = 4.0 * np.power(PI * t, 1.5) * np.sqrt(Kx * Ky * Kz)
        exponent = -0.25 / t * (X ** 2 / Kx + Y ** 2 / Ky + Z ** 2 / Kz)
        return M / denom * _safe_exp(exponent)

    if model == "case7":
        # Steady plume from ground, anisotropic diffusivity; x must be downwind.
        xp = np.maximum(X, 1e-9)
        denom = 2.0 * PI * xp * np.sqrt(Kx * Ky)
        exponent = -u / (4.0 * xp) * (Y ** 2 / Ky + Z ** 2 / Kz)
        C = Q / denom * _safe_exp(exponent)
        return np.where(X > 0, C, 0.0)

    if model == "case8":
        # Elevated continuous source; ground is an impervious boundary (image term).
        xp = np.maximum(X, 1e-9)
        denom = 4.0 * PI * xp * np.sqrt(Ky * Kz)
        lateral = _safe_exp(-u * Y ** 2 / (4.0 * Ky * xp))
        vertical = (
            _safe_exp(-u * (Z - H) ** 2 / (4.0 * Kz * xp))
            + _safe_exp(-u * (Z + H) ** 2 / (4.0 * Kz * xp))
        )
        C = Q / denom * lateral * vertical
        return np.where(X > 0, C, 0.0)

    if model == "case9":
        # Gaussian puff, ground-level source. The denominator below includes
        # the factor of 2 for the ground image source, matching Lecture 21's
        # chlorine worked example (sqrt(2)*pi^(3/2), not the free-space form).
        xc = max(u * t, 1.0)
        sx, sy, sz = puff_sigmas(xc, stability)
        denom = np.sqrt(2.0) * PI ** 1.5 * sx * sy * sz
        exponent = -0.5 * (((X - u * t) / sx) ** 2 + (Y / sy) ** 2 + (Z / sz) ** 2)
        return M / denom * _safe_exp(exponent)

    if model == "case10":
        # Pasquill-Gifford reflected plume. H=0 reproduces the Lecture 20 Case 10
        # ground source; H>0 is the elevated-source formulation in Lecture 21.
        sy, sz = plume_sigmas(X, stability)
        xp = np.maximum(X, 1e-9)
        denom = 2.0 * PI * u * sy * sz
        lateral = _safe_exp(-0.5 * (Y / sy) ** 2)
        vertical = (
            _safe_exp(-0.5 * ((Z - H) / sz) ** 2)
            + _safe_exp(-0.5 * ((Z + H) / sz) ** 2)
        )
        C = Q / denom * lateral * vertical
        return np.where((X > 0) & (u > 0), C, 0.0)

    raise RuntimeError("Model dispatch failed.")


def concentration_to_ppmv(c_kg_m3, molecular_weight_g_mol: float,
                          temperature_K: float = 298.15,
                          pressure_Pa: float = 101325.0):
    """Convert mass concentration (kg/m3) to ppmv using ideal-gas relation."""
    if molecular_weight_g_mol <= 0 or temperature_K <= 0 or pressure_Pa <= 0:
        raise ValueError("Molecular weight, temperature and pressure must be positive.")
    mw_kg_mol = molecular_weight_g_mol / 1000.0
    R = 8.314462618  # Pa m3/(mol K)
    return _as_array(c_kg_m3) / mw_kg_mol * R * temperature_K / pressure_Pa * 1e6


def concentration_to_mg_m3(c_kg_m3):
    return _as_array(c_kg_m3) * 1e6


def arrival_time_s(distance_m: float, wind_speed_m_s: float):
    if distance_m < 0 or wind_speed_m_s < 0:
        raise ValueError("Distance and wind speed must be non-negative.")
    if wind_speed_m_s == 0:
        return np.inf
    return distance_m / wind_speed_m_s
