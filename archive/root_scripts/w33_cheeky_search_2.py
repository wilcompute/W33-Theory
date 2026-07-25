import math
from itertools import combinations

def deep_cheeky_search(target, name, tolerance=1e-3, use_pow=False):
    print(f"\n--- Searching for {name} ({target}) ---")
    
    primitives = {
        'q': 3, 'mu': 4, 'q!': 6, 'Phi6': 7, 'Phi4': 10, 'k': 12, 'Phi3': 13, 
        'g': 15, 'f': 24, 'q^q': 27, 'T7': 28, 'v': 40, 'H1': 81, 'alpha': 137, 
        'tom': 192, 'E': 240, 'E8': 248, 'tau_O': 384, 'W_E6': 51840,
        'pi': math.pi, 'phi': (1 + math.sqrt(5))/2, 'e': math.e,
        'Leech': 196560, 'M_rep': 196883
    }
    
    results = []
    keys = list(primitives.keys())
    
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i == j: continue
            k1, k2 = keys[i], keys[j]
            v1, v2 = primitives[k1], primitives[k2]
            
            exprs = [
                (f"{k1} * {k2}", v1 * v2),
                (f"{k1} / {k2}", v1 / v2 if v2 != 0 else -1),
                (f"({k1}^2) * {k2}", (v1**2) * v2),
                (f"{k1} * ({k2}^2)", v1 * (v2**2)),
                (f"{k1}^3 / {k2}", (v1**3) / v2 if v2 != 0 else -1),
                (f"{k1} / math.sqrt({k2})", v1 / math.sqrt(abs(v2)) if v2 > 0 else -1),
                (f"math.sqrt({k1}) * {k2}", math.sqrt(abs(v1)) * v2 if v1 > 0 else -1)
            ]
            
            for m in range(len(keys)):
                if m == i or m == j: continue
                k3 = keys[m]
                v3 = primitives[k3]
                exprs.extend([
                    (f"({k1} * {k2}) / {k3}", (v1*v2)/v3 if v3 != 0 else -1),
                    (f"({k1} + {k2}) * {k3}", (v1+v2)*v3),
                    (f"{k1}^2 / ({k2}*{k3})", (v1**2)/(v2*v3) if v2*v3 != 0 else -1),
                    (f"({k1} * {k2}) / math.sqrt({k3})", (v1*v2)/math.sqrt(abs(v3)) if v3 > 0 else -1),
                    (f"math.sqrt({k1} * {k2}) * {k3}", math.sqrt(abs(v1*v2))*v3 if v1*v2 > 0 else -1)
                ])
                
            for expr, val in exprs:
                if abs(val - target) < tolerance:
                    results.append((abs(val - target), expr, val))
                    
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
    # 1. Proton-to-electron mass ratio ~ 1836.152
    deep_cheeky_search(1836.152, "m_p / m_e (1836.152)", tolerance=5.0)
    
    # 2. Neutrino mass splitting (atm) m_nu3 ~ 0.05 eV. Ratio to m_e (511000 eV) is 9.78e-8
    # Search inverse: m_e / m_nu3 = 10220000
    deep_cheeky_search(10220000, "m_e / m_nu3 (10220000)", tolerance=50000)
    
    # 3. Ratio of 3215 scalar to Higgs 125.2 = 25.678
    deep_cheeky_search(25.678, "M_Scalar / M_Higgs (25.678)", tolerance=0.1)
    
    # 4. Baryogenesis asymmetry eta_B ~ 6.1e-10. Inverse is 1.639e9
    deep_cheeky_search(1639344262, "1 / eta_B (1.639e9)", tolerance=10000000)
