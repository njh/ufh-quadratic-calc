#!/usr/bin/env python3

import pandas as pd
import numpy as np
from pathlib import Path

# --- CONFIG ---

# New CSV file name
SOLID_CSV = Path("mcs-solid-16mm-table.csv")

# Available floor covering R-values and pipe spacings
FLOOR_R_VALUES = [0.00, 0.05, 0.10, 0.15]
PIPE_SPACING_MM = [100, 150, 200, 250, 300]



# --- FUNCTIONS ---


def load_sheet(path: Path):
    """
    Load CSV and build nested data structure:
    data[r_value][pipe_spacing][flow_temp][room_temp] = {"watt_output": ..., "surface_temp": ...}
    """
    df = pd.read_csv(path)

    # Map columns to r_value and pipe_spacing
    data = {}

    # Build nested dict
    for i, row in df.iterrows():
        flow_temp = row["flow_temp"]
        room_temp = row["room_temp"]

        for r_value in FLOOR_R_VALUES:
            for spacing_mm in PIPE_SPACING_MM:
                # Work out column names - convert r_value to integer for filename
                col_params = f"{int(r_value*100):03d}_{spacing_mm:03d}"
                watt_output = row[f"{col_params}_output"]
                surface_temp = row[f"{col_params}_temp"]
                #print(f"R={r_value}, spacing={spacing_mm}, output={watt_output}, surface_temp={surface_temp}")
    
                # Add to nested dict
                data.setdefault(r_value, {})
                data[r_value].setdefault(spacing_mm, {})
                data[r_value][spacing_mm].setdefault(flow_temp, {})
                data[r_value][spacing_mm][flow_temp][room_temp] = {
                     "watt_output": watt_output,
                     "surface_temp": surface_temp
                }
    return data



def fit_linear_for_covering(data, r_value, spacing_mm):
    """
    Finds the best straight-line relationship between temperature difference and output for a specific R value and pipe spacing.

    For a given R and spacing, fit:
        output ≈ m_i * dT - c_i
    Returns (m_i, c_i).
    """
    dT_list = []
    y_list = []

    # Traverse all flow_temp and room_temp combinations
    for flow_temp in data[r_value][spacing_mm]:
        for room_temp, vals in data[r_value][spacing_mm][flow_temp].items():
            output = vals.get("watt_output", np.nan)
            dT_list.append(flow_temp - room_temp)
            y_list.append(output)

    dT = np.array(dT_list)
    y = np.array(y_list)

    #print(f"Fitting linear for R={r_value}, spacing={spacing_mm} with {len(dT)} points")

    # Least-squares fit: y ≈ m_i * dT + b_i
    A = np.column_stack([dT, np.ones_like(dT)])
    m_i, b_i = np.linalg.lstsq(A, y, rcond=None)[0]

    # Convert to y ≈ m_i * dT - c_i  => c_i = -b_i
    c_i = -b_i
    return m_i, c_i



def fit_quadratics_for_spacing(data, spacing_mm):
    """
    Fit m_i, c_i for spacing_mm, then fit quadratic m(R) and c(R).
    """
    m_vals = []
    c_vals = []

    for r in FLOOR_R_VALUES:
        m_i, c_i = fit_linear_for_covering(data, r, spacing_mm)
        m_vals.append(m_i)
        c_vals.append(c_i)
        print(f"R={r:0.2f}, spacing={spacing_mm}:  m_i={m_i:8.4f},  c_i={c_i:8.4f}")

    # Quadratic fit: m(R) ~ a_m*R^2 + b_m*R + c_m
    coeff_m = np.polyfit(FLOOR_R_VALUES, m_vals, 2)
    coeff_c = np.polyfit(FLOOR_R_VALUES, c_vals, 2)

    print("\nQuadratic for m(R):")
    print(
        "m = {a:.4f}*R*R + {b:.4f}*R + {c:.5f}".format(
            a=coeff_m[0], b=coeff_m[1], c=coeff_m[2]
        )
    )

    print("\nQuadratic for c(R):")
    print(
        "c = {a:.4f}*R*R + {b:.4f}*R + {c:.5f}".format(
            a=coeff_c[0], b=coeff_c[1], c=coeff_c[2]
        )
    )

    return coeff_m, coeff_c



if __name__ == "__main__":
    # Solid floor 16mm pipe
    data_solid = load_sheet(SOLID_CSV)

    for spacing_mm in PIPE_SPACING_MM:
       print(f"\n=== Quadratic fit for spacing={spacing_mm} ===")
       fit_quadratics_for_spacing(data_solid, spacing_mm)
