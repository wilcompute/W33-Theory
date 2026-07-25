import math
from itertools import combinations
import numpy as np

def cheeky_search(target, name, tolerance=1e-4):
    print(f"\n--- Searching for {name} ({target}) ---")
    
    # Core W(3,3) primitives
    primitives = {
        'q': 3, 
        'mu': 4, 
        'q!': 6, 
        'Phi6': 7, 
        'Phi4': 10, 
        'k': 12, 
        'Phi3': 13, 
        'g': 15, 
        'f': 24, 
        'q^q': 27,
        'T7': 28,
        'v': 40, 
        'H1': 81, 
        'alpha_inv_tree': 137, 
        'E': 240, 
        'tau_O': 384,
        'pi': math.pi,
        'phi': (1 + math.sqrt(5))/2,
        'e': math.e
    }
    
    # simple operators: a*b, a/b, a+b, a-b, a^b, log(a)/log(b)
    results = []
    
    keys = list(primitives.keys())
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i == j: continue
            k1, k2 = keys[i], keys[j]
            v1, v2 = primitives[k1], primitives[k2]
            
            exprs = [
                (f"{k1} / {k2}", v1 / v2 if v2 != 0 else -1),
                (f"1 / ({k1}*{k2})", 1.0 / (v1 * v2) if v1*v2 != 0 else -1),
                (f"{k1} / ({k2}^2)", v1 / (v2**2) if v2 != 0 else -1),
                (f"({k1}^2) / {k2}", (v1**2) / v2 if v2 != 0 else -1),
                (f"({k1}*pi) / {k2}", (v1*math.pi) / v2 if v2 != 0 else -1),
                (f"{k1} / ({k2}*pi)", v1 / (v2*math.pi) if v2 != 0 else -1),
                (f"math.log({k1}) / {k2}", math.log(abs(v1)) / v2 if v1 > 0 and v2 != 0 else -1),
                (f"{k1} / math.log({k2})", v1 / math.log(abs(v2)) if v2 > 1 else -1)
            ]
            
            # also add some 3-term things
            for m in range(len(keys)):
                if m == i or m == j: continue
                k3 = keys[m]
                v3 = primitives[k3]
                exprs.extend([
                    (f"({k1} * {k2}) / {k3}", (v1*v2)/v3 if v3 != 0 else -1),
                    (f"{k1} / ({k2} * {k3})", v1/(v2*v3) if v2*v3 != 0 else -1),
                    (f"({k1} + {k2}) / {k3}", (v1+v2)/v3 if v3 != 0 else -1),
                    (f"{k1} / ({k2} + {k3})", v1/(v2+v3) if (v2+v3) != 0 else -1),
                    (f"({k1} * pi) / ({k2} * {k3})", (v1*math.pi)/(v2*v3) if v2*v3 != 0 else -1),
                ])
                
            for expr, val in exprs:
                if abs(val - target) < tolerance:
                    results.append((abs(val - target), expr, val))
                    
    # Sort and print top 10 unique
    seen = set()
    best = []
    for err, expr, val in sorted(results):
        if val not in seen:
            seen.add(val)
            best.append((expr, val, err))
            if len(best) >= 10: break
            
    for expr, val, err in best:
        print(f"Match: {expr} = {val:.6f} (Error: {err:.6f})")

if __name__ == "__main__":
    # 1. Delta_RG = 0.035999 (QED running residue)
    cheeky_search(0.035999, "Delta_RG (0.035999)")
    
    # 2. Proton Mass / EW scale = 0.93827 / 246.22 = 0.0038107
    cheeky_search(0.0038107, "Proton / v_EW ratio (0.0038107)")
    
    # 3. W boson width / W boson mass = 2.085 / 80.379 = 0.02594
    cheeky_search(0.02594, "W_width / M_W (0.02594)")
    
    # 4. Lambda QCD / v_EW = 0.332 / 246.22 = 0.001348 (approx 332 MeV in MSbar 5 flavor)
    cheeky_search(0.001348, "Lambda_QCD / v_EW (0.001348)")
