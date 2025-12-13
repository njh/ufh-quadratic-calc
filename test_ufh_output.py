#!/usr/bin/env python3
import unittest
from ufh_output_funcs import ufh_heat_output

# Acceptable percentage error
ERROR_TOLERANCE = 1.8

class TestCalculations(unittest.TestCase):
    def assert_percent_error(self, actual, expected, threshold_percent=2):
        percent_error = abs(actual - expected) / expected * 100
        assert percent_error < threshold_percent, (
            f"Error {percent_error:.2f}% exceeds threshold of {threshold_percent}%: "
            f"expected={expected}, actual={actual}")

    def test_100_010_35_20(self):
        watts_m2 = ufh_heat_output(pipe_spacing=100, r_value=0.10, flow_temp=35, room_temp=20)
        self.assert_percent_error(watts_m2, 38.9, ERROR_TOLERANCE)

    def test_150_000_40_20(self):
        watts_m2 = ufh_heat_output(pipe_spacing=150, r_value=0.00, flow_temp=40, room_temp=20)
        self.assert_percent_error(watts_m2, 86.4, ERROR_TOLERANCE)

    def test_200_015_35_22(self):
        watts_m2 = ufh_heat_output(pipe_spacing=200, r_value=0.15, flow_temp=35, room_temp=22)
        self.assert_percent_error(watts_m2, 21.6, ERROR_TOLERANCE)

    def test_250_010_50_24(self):
        watts_m2 = ufh_heat_output(pipe_spacing=250, r_value=0.10, flow_temp=50, room_temp=24)
        self.assert_percent_error(watts_m2, 60, ERROR_TOLERANCE)

    def test_300_005_55_18(self):
        watts_m2 = ufh_heat_output(pipe_spacing=300, r_value=0.05, flow_temp=55, room_temp=18)
        self.assert_percent_error(watts_m2, 96.9, ERROR_TOLERANCE)

if __name__ == '__main__':
    unittest.main()
