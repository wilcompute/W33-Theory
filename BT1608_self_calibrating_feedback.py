"""BT1608: Self-Calibrating Feedback Agent

The feedback agent updates 168 SNSPD bin thresholds each cycle.
Convergence rate is determined by S_min = log2(168/40) = 2.0704 bits.
"""
import math

Stab_Fano  = 40
Stab_SNSPD = 168
N_bins     = 168

# Per-cycle update rule: threshold_new = threshold_old * (1 - alpha) + target * alpha
alpha = 1 - (Stab_Fano / Stab_SNSPD)  # = 0.7619
S_min = math.log2(Stab_SNSPD / Stab_Fano)

print(f"SNSPD bins: {N_bins}")
print(f"S_min = {S_min:.6f} bits")
print(f"Per-cycle alpha = {alpha:.6f}  ({alpha*100:.1f}% error eliminated per cycle)")

# Convergence analysis
print("\nConvergence table (fraction of initial error remaining):")
for cycle in range(1, 7):
    remaining = (1 - alpha)**cycle
    print(f"  Cycle {cycle}: {remaining:.4f} ({remaining*100:.1f}% error remaining)")

# Threshold update: bins converge to BT1614 bench specification within 3 cycles
print(f"\nCycles to <5% error: {math.ceil(math.log(0.05)/math.log(1-alpha))}")
print(f"Cycles to <1% error: {math.ceil(math.log(0.01)/math.log(1-alpha))}")
print(f"Time to <5% error at 45min/cycle: {math.ceil(math.log(0.05)/math.log(1-alpha))*0.75:.2f} hours")

print("\nBT1608 COMPLETE.")
