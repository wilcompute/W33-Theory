#!/usr/bin/env python3
import numpy as np

def mod3(x): 
    return np.mod(x, 3).astype(np.int8)

def lift_h3_to_line_weights(x88, npz_path="lift_matrices_mod3.npz"):
    """Return 90-vector of line weights mod 3, defined up to adding constant all-ones vector."""
    data=np.load(npz_path)
    M=data["M_H3_to_90"] % 3
    x=mod3(np.array(x88, dtype=np.int16).reshape(88))
    w=mod3(M @ x)
    return w

def normalize_coset(w90, idx=0):
    """Fix a representative in the coset mod <ones> by forcing coordinate idx to 0."""
    w=mod3(w90)
    c=int(w[idx])
    w = mod3(w - c*np.ones_like(w))
    return w

if __name__ == "__main__":
    # example
    x=np.zeros(88, dtype=np.int8); x[0]=1
    w=lift_h3_to_line_weights(x)
    print("raw weights:", w.tolist())
    print("normalized (coord0=0):", normalize_coset(w,0).tolist())
