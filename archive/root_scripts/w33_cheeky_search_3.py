import math

def deep_cheeky_search_cosmo(target, name, tolerance=1e-4):
    print(f"\n--- Searching for {name} ({target}) ---")
    
    # Core W(3,3) parameters + important physical constants
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
                (f"{k1} / {k2}", v1 / v2 if v2 != 0 else -1),
                (f"math.log({k1}) / math.log({k2})", math.log(abs(v1))/math.log(abs(v2)) if v1>0 and v2>1 else -1),
                (f"({k1}*pi) / ({k2}*phi)", (v1*math.pi)/(v2*math.phi if 'phi' in primitives else v2*1.618034) if v2!=0 else -1)
            ]
            
            for m in range(len(keys)):
                if m == i or m == j: continue
                k3 = keys[m]
                v3 = primitives[k3]
                exprs.extend([
                    (f"{k1} / ({k2} * {k3})", v1/(v2*v3) if v2*v3 != 0 else -1),
                    (f"({k1} + {k2}) / ({k3}^2)", (v1+v2)/(v3**2) if v3 != 0 else -1),
                    (f"math.sqrt({k1}) / ({k2} * {k3})", math.sqrt(v1)/(v2*v3) if v1>0 and v2*v3 != 0 else -1),
                    (f"1 / ({k1} * {k2} * {k3})", 1.0/(v1*v2*v3) if v1*v2*v3 != 0 else -1)
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
    # 1. 1 - n_s (scalar tilt residue) ~ 0.0351
    deep_cheeky_search_cosmo(0.0351, "1 - n_s (0.0351)")
    
    # 2. r (tensor to scalar ratio) ~ 0.0222
    deep_cheeky_search_cosmo(0.0222, "r (tensor-to-scalar) (0.0222)")
    
    # 3. Baryon Asymmetry (eta_B) ~ 6.1e-10. Let's look for 6.1e-10 * 1e9 = 0.61
    deep_cheeky_search_cosmo(0.61, "eta_B scaled (0.61)")
    
    # 4. Omega_DarkMatter h^2 = 0.120
    deep_cheeky_search_cosmo(0.120, "Omega_DM h^2 (0.120)")
