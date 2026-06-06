"""
BT441: N*=8 Tier Reinterpretation
Fractal depth N* = 2^q = 8 is FINITE (BT439 correction).
Tiers 1..8 = octonion nesting (E8 sphere packing saturates here).
Tiers >8   = embedding regime (not nesting).
"""
import math, json

q, mu, lam, V, N_star = 3, 4, 2, 40, 8

tier_data = []
for n in range(1, 13):
    mode = "NESTING" if n <= N_star else "EMBEDDING"
    if n == 3:
        packing = 0.2536
    elif n == 4:
        packing = 0.001929
    elif n <= N_star:
        packing = 0.2536 * (0.5 ** (n - 3))
    else:
        packing = 0.2536 * (N_star / n) ** mu
    info = (q**2) * (lam**n) if n <= N_star else (q**2) * (lam**N_star) * n
    tier_data.append({"tier": n, "mode": mode, "dim": 2**n,
                      "sphere_packing_density": round(packing, 6),
                      "info_capacity_bits": round(info, 2)})

print(f"N* = 2^q = {N_star} (E8 saturation boundary)")
for r in tier_data:
    print(f"  Tier {r['tier']:2d} [{r['mode']:10s}] dim={r['dim']:5d}  rho={r['sphere_packing_density']:.6f}  I={r['info_capacity_bits']:.1f} bits")

with open("BT441_results.json", "w") as f:
    json.dump({"N_star": N_star, "tiers": tier_data}, f, indent=2)
print("BT441 complete.")
