"""Tests for the integer refinement; each targets a mathematical failure mode."""
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
import json
import shutil
import tempfile
import unittest

import check


class IntegerSlackTests(unittest.TestCase):
    def test_two_integer_sharp_points(self):
        for radius, t, q_expected in [(2, 0, F(1)), (3, 1, F(5, 4))]:
            x = check.Profile(radius, radius, radius, radius, (0, 0, 0), (t, t, t))
            self.assertTrue(x.feasible())
            self.assertTrue(x.integral())
            self.assertEqual(x.Q(), q_expected)
            self.assertEqual(x.R(), -1)

    def test_integrality_cannot_be_dropped(self):
        x = check.Profile(*(F(5, 2),) * 4, (0, 0, 0), (F(1, 2),) * 3)
        self.assertTrue(x.feasible())
        self.assertFalse(x.integral())
        self.assertEqual(x.R(), F(-17, 16))

    def test_domain_constraints_are_individual(self):
        x = check.Profile(1, 12, 1, 1, (0, 0, 5), (0, 0, 0))
        self.assertTrue(x.feasible())
        self.assertFalse(replace(x, v=2).feasible())
        self.assertFalse(replace(x, t=(2, 0, 0)).feasible())
        self.assertFalse(replace(x, d=1).feasible())
        self.assertFalse(replace(x, c=0).feasible())
        self.assertFalse(replace(x, p=(-1, 0, 5)).feasible())
        self.assertFalse(replace(x, t=(-1, 0, 0)).feasible())
        self.assertFalse(replace(x, v=-1).feasible())
        self.assertFalse(check.Profile(3, 3, 3, 0, (0, 0, 0), (0, 0, 0)).feasible())

    def test_quadratic_interpolation_detects_cross_and_square_terms(self):
        self.assertEqual(check.quadratic_identity(3, lambda x: F(0)), 10)
        for f in [lambda x: F(1), lambda x: x[0], lambda x: x[1] ** 2,
                  lambda x: x[0] * x[2]]:
            with self.assertRaises(check.VerificationError):
                check.quadratic_identity(3, f)

    def test_inherited_algebra_and_new_lattice(self):
        result = check.check_identities()
        self.assertGreater(result["identities"], 20)
        self.assertGreater(result["exact_evaluations"], 500)

    def test_matrix_reconstruction_and_tighter_constant(self):
        result = check.check_downstream(Path(__file__).parent / "source/original.json")
        self.assertEqual(result["integer_M_bound"], 49)
        self.assertEqual(result["strict_bound"], 50)
        self.assertEqual(result["failed_B49_coordinates"], 3)
        self.assertEqual(result["mode_removal_even_D"], 588)
        self.assertEqual(result["retained_complete_even_D"], 600)
        self.assertEqual(result["minimum_squared_margin"], 194226871915968682337664)

    def test_matrix_and_overstrong_claims_are_rejected(self):
        data = json.loads((Path(__file__).parent / "source/original.json").read_text())
        for key in ("A", "inverse_numerator"):
            changed = deepcopy(data)
            changed[key][0][0] += 1
            with self.assertRaises(check.VerificationError):
                check.downstream_from_data(changed)
        changed = deepcopy(data)
        changed["template"]["bits"][0] = "111"
        with self.assertRaises(check.VerificationError):
            check.downstream_from_data(changed)
        with self.assertRaises(check.VerificationError):
            check.downstream_from_data(data, strict_bound=49)
        with self.assertRaises(check.VerificationError):
            check.downstream_from_data(data, face_constant=F(17, 16))

    def test_source_bytes_are_bound(self):
        root = Path(__file__).parent
        self.assertEqual(check.check_sources(root), 9)
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td)
            shutil.copytree(root/"source", dest/"source")
            shutil.copyfile(root/"source-pins.json", dest/"source-pins.json")
            with (dest/"source/THEOREM.md").open("ab") as f:
                f.write(b"\nChanged source\n")
            with self.assertRaises(check.VerificationError):
                check.check_sources(dest)

    def test_exact_input_requirement(self):
        with self.assertRaises(check.VerificationError):
            check.Profile(2.0, 2, 2, 2, (0, 0, 0), (0, 0, 0))
        with self.assertRaises(check.VerificationError):
            check.Profile(2, 2, 2, 2, (0, 0), (0, 0, 0))

    def test_finite_boundary_grid(self):
        result = check.check_grid()
        self.assertGreater(result["profiles"], 20000)
        self.assertEqual(result["minimum_R"], "-1")
        self.assertEqual(result["boundary_equality_profiles"], 2)

    def test_negative_controls(self):
        result = check.check_controls()
        self.assertGreaterEqual(result["rejected_controls"], 8)


if __name__ == "__main__":
    unittest.main()
