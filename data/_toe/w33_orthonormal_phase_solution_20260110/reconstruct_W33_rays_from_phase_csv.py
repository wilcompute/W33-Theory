import cmath
import math

import numpy as np
import pandas as pd

pi = math.pi


def entry(mag, k):
    if mag == 0 or pd.isna(k):
        return 0j
    return mag * cmath.exp(1j * (int(k) * pi / 6))


# optional normalize
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def main():
    df = pd.read_csv("W33_point_rays_C4_12throot_phases.csv")
    V = np.zeros((len(df), 4), dtype=complex)
    for i, row in df.iterrows():
        for j in range(4):
            V[i, j] = entry(row[f"c{j}_mag"], row[f"c{j}_phase_k"])
    print("Loaded", V.shape)


if __name__ == "__main__":
    main()
