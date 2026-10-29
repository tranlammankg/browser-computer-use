#!/usr/bin/env python3
"""
Unit tests for Computer Use calculations and Bezier curves.
"""

import unittest
import math
import sys
import os

# Include skills script directory in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "browser-computer-use", "scripts")))

from computer_use import _bezier_point

class TestComputerUse(unittest.TestCase):

    def test_bezier_endpoints(self):
        """Bezier curve at t=0 must equal start point, at t=1 must equal end point."""
        p0, p1, p2, p3 = 100.0, 150.0, 300.0, 500.0
        self.assertAlmostEqual(_bezier_point(p0, p1, p2, p3, 0.0), p0)
        self.assertAlmostEqual(_bezier_point(p0, p1, p2, p3, 1.0), p3)

    def test_bezier_interpolation(self):
        """Bezier curve at t=0.5 must be between start and end for monotone control points."""
        p0, p1, p2, p3 = 0.0, 25.0, 75.0, 100.0
        mid = _bezier_point(p0, p1, p2, p3, 0.5)
        self.assertTrue(0.0 < mid < 100.0)

    def test_bezier_continuity(self):
        """Points along the curve must be continuous without sudden jumps."""
        p0, p1, p2, p3 = 50.0, 120.0, 400.0, 600.0
        prev = p0
        for i in range(1, 101):
            t = i / 100.0
            cur = _bezier_point(p0, p1, p2, p3, t)
            self.assertTrue(abs(cur - prev) < 15.0)
            prev = cur

if __name__ == "__main__":
    unittest.main()
