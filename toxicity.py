"""Toxicity threshold utilities for ToxiDisp."""
from dispersion_models import concentration_to_ppmv


def assess_threshold(c_kg_m3: float, threshold_ppmv: float, molecular_weight_g_mol: float,
                     temperature_K: float = 298.15, pressure_Pa: float = 101325.0):
    """Return a simple threshold comparison, not a medical risk prediction."""
    predicted_ppmv = float(concentration_to_ppmv(
        c_kg_m3, molecular_weight_g_mol, temperature_K, pressure_Pa
    ))
    return {
        "predicted_ppmv": predicted_ppmv,
        "threshold_ppmv": float(threshold_ppmv),
        "exceeds": predicted_ppmv >= threshold_ppmv,
        "ratio": predicted_ppmv / threshold_ppmv if threshold_ppmv > 0 else float("inf"),
    }
