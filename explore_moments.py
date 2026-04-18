#!/usr/bin/env python3
"""
Explore the sequence of spectral moments tr(A^j) for W(3,3).
"""

n, k, r, s, fr, fs = 40, 12, 2, -4, 24, 15
lambda_srg, mu_srg = 2, 4  # The SRG parameters

print('=== ADJACENCY MATRIX RECURRENCE RELATION ===')
print()
print(f'For SRG({n},{k},{lambda_srg},{mu_srg}), the adjacency matrix satisfies:')
print(f'  A^3 = (k+r+s)A^2 - (rs+k)A + (r+s)I')
print()

# The recurrence is A^{j+1} = c0*I + c1*A + c2*A^2 for large j
# More precisely, for SRG: the characteristic polynomial is:
# chi(lambda) = (lambda-k)(lambda-r)(lambda-s) = lambda^3 - (k+r+s)*lambda^2 + (kr+ks+rs)*lambda - krs

c2 = k + r + s  # = 12 + 2 - 4 = 10
c1 = k*r + k*s + r*s     # = 24 + (-48) + (-8) = -32
c0 = -k*r*s     # = -12*2*(-4) = 96

print(f'Characteristic polynomial coefficients:')
print(f'  c2 = k+r+s = {k}+{r}+{s} = {c2}')
print(f'  c1 = kr+ks+rs = {k*r}+{k*s}+{r*s} = {c1}')
print(f'  c0 = -krs = {c0}')
print()

# For any eigenvalue lambda: lambda^3 = c2*lambda^2 - c1*lambda - c0
# So: tr(A^{j+3}) = c2*tr(A^{j+2}) - c1*tr(A^{j+1}) - c0*tr(A^j)

print(f'Recurrence: tr(A^{{j+3}}) = {c2}*tr(A^{{j+2}}) - ({c1})*tr(A^{{j+1}}) - ({c0})*tr(A^j)')
print(f'           = {c2}*tr(A^{{j+2}}) + {-c1}*tr(A^{{j+1}}) + {-c0}*tr(A^j)')
print()

# Compute traces using recurrence
# Initial: tr(I) = 40, tr(A) = 0, tr(A^2) = 480, tr(A^3) = 960
traces = {0: 40, 1: 0, 2: 480, 3: 960}

print('Computing tr(A^j) via recurrence:')
for j in range(0, 10):
    if j in traces:
        print(f'  tr(A^{j}) = {traces[j]:12}')
    else:
        # Use recurrence: tr(A^j) = c2*tr(A^{j-1}) + (-c1)*tr(A^{j-2}) + (-c0)*tr(A^{j-3})
        val = c2*traces[j-1] + (-c1)*traces[j-2] + (-c0)*traces[j-3]
        traces[j] = val
        print(f'  tr(A^{j}) = {c2}*{traces[j-1]:12} + {-c1}*{traces[j-2]:12} + {-c0}*{traces[j-3]:12} = {val:12}')

print()
print('Verification against direct computation:')
for j in range(9):
    direct = k**j + fr*r**j + fs*s**j
    recur = traces[j]
    match = '✓' if direct == recur else 'X'
    print(f'  tr(A^{j}): direct={direct:12}, recurrence={recur:12} {match}')

print()
print('Moment ratios to tr(A^2)=480:')
seq = [traces[j] for j in range(9)]
ratios = [s/480 for s in seq]
print(f'  j:      {list(range(9))}')
print(f'  ratio:  {[f"{r:.4f}" for r in ratios]}')

print()
print('Second differences of log ratios (to detect growth patterns):')
import math
log_ratios = [math.log(r) if r > 0 else 0 for r in ratios]
print(f'  log(ratio): {[f"{lr:.4f}" for lr in log_ratios]}')
for j in range(2, 8):
    d1 = log_ratios[j] - log_ratios[j-1]
    d2 = log_ratios[j] - 2*log_ratios[j-1] + log_ratios[j-2] if j >= 2 else None
    print(f'  Δlog_j = {d1:.4f}')
