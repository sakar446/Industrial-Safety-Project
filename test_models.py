import unittest
import numpy as np
from dispersion_models import concentration, plume_sigmas, puff_sigmas, concentration_to_ppmv, arrival_time_s


class TestDispersionModels(unittest.TestCase):
    def test_plume_sigmas_lecture_example(self):
        sy, sz = plume_sigmas(500.0, "D")
        self.assertAlmostEqual(float(sy), 39.0, delta=0.2)
        self.assertAlmostEqual(float(sz), 22.7, delta=0.2)

    def test_so2_lecture_example(self):
        c = float(concentration("case10", 500.0, 0.0, 0.0,
                                mass_rate_kg_s=0.08, wind_speed=6.0,
                                release_height_m=60.0, stability="D"))
        c_g_m3 = c * 1000.0
        self.assertAlmostEqual(c_g_m3, 1.45e-4, delta=0.02e-4)

    def test_so2_crosswind_lecture_example(self):
        c = float(concentration("case10", 500.0, 50.0, 0.0,
                                mass_rate_kg_s=0.08, wind_speed=6.0,
                                release_height_m=60.0, stability="D"))
        self.assertAlmostEqual(c * 1000.0, 6.37e-5, delta=0.1e-5)

    def test_chlorine_puff_arrival_time(self):
        self.assertAlmostEqual(arrival_time_s(500.0, 2.0), 250.0)

    def test_chlorine_puff_center_is_positive(self):
        c = float(concentration("case9", 500.0, 0.0, 0.0,
                                mass_kg=1.0, wind_speed=2.0,
                                time_s=250.0, stability="F"))
        self.assertGreater(c, 0.0)

    def test_all_cases_return_nonnegative_or_nan_at_source_singularity(self):
        cases = {
            "case1": dict(mass_rate_kg_s=0.01, k_iso=10),
            "case2": dict(mass_kg=1, k_iso=10, time_s=10),
            "case3": dict(mass_rate_kg_s=0.01, k_iso=10, time_s=10),
            "case4": dict(mass_rate_kg_s=0.01, k_iso=10, wind_speed=2),
            "case5": dict(mass_kg=1, kx=10, ky=5, kz=2, wind_speed=2, time_s=10),
            "case6": dict(mass_kg=1, kx=10, ky=5, kz=2, time_s=10),
            "case7": dict(mass_rate_kg_s=0.01, kx=10, ky=5, kz=2, wind_speed=2),
            "case8": dict(mass_rate_kg_s=0.01, kx=10, ky=5, kz=2, wind_speed=2, release_height_m=10),
            "case9": dict(mass_kg=1, wind_speed=2, time_s=10, stability="D"),
            "case10": dict(mass_rate_kg_s=0.01, wind_speed=2, stability="D"),
        }
        for model, kwargs in cases.items():
            c = concentration(model, 100.0, 10.0, 0.0, **kwargs)
            self.assertTrue(np.isfinite(float(c)), model)
            self.assertGreaterEqual(float(c), 0.0, model)

    def test_ppm_conversion_positive(self):
        ppm = float(concentration_to_ppmv(1e-4, 70.9, 298.15, 101325))
        self.assertGreater(ppm, 0)


if __name__ == "__main__":
    unittest.main()
