#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIG ---
CSV_PATH = "mcs-solid-16mm-table.csv"
FLOOR_R_VALUES = [0.00, 0.05, 0.10, 0.15]
PIPE_SPACING_MM = [100, 150, 200, 250, 300]

# Function for 150mm pipe spacing
def heat_output_150(r_value, dT):
    m = 86.6934 * (r_value ** 2) - 31.5422 * r_value + 5.74376
    c = 424.6747 * (r_value ** 2) - 156.4000 * r_value + 28.70193
    return (m * dT) - c



# Read CSV
df = pd.read_csv(CSV_PATH)

for pipe_spacing in [150]:

    plt.figure(figsize=(8,6))
    dT_range = np.linspace(0, 40, 200)

    for r in FLOOR_R_VALUES:
        # Plot fitted line
        y_fit = [heat_output_150(r, dT) for dT in dT_range]
        plt.plot(dT_range, y_fit, label=f"R={r:.2f} m²·K/W")
        # Plot MCS data points
        col = f"{int(r*100):03d}_{pipe_spacing:03d}_output"
        if col in df.columns:
            dT_mcs = df["flow_temp"] - df["room_temp"]
            y_mcs = df[col]
            mask = ~pd.isna(dT_mcs) & ~pd.isna(y_mcs)
            plt.scatter(dT_mcs[mask], y_mcs[mask], marker='o', s=40, edgecolor='k', facecolor='none')

    plt.xlabel("Delta T (flow_temp - room_temp) [°C]")
    plt.ylabel("Watt Output (W/m²)")
    plt.title(f"Delta T vs Watt Output for {pipe_spacing}mm Spacing")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()

    plt.savefig(f"deltaT_vs_output_{pipe_spacing}mm.png", dpi=144)
    print(f"Plot saved as deltaT_vs_output_{pipe_spacing}mm.png")
