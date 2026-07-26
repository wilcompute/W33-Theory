#!/usr/bin/env python3
"""
Pass4 Step 1: CF=1/10 Benchtop Experiment Complete Runbook
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
import numpy as np

q, v, k, lam, mu, Phi4 = 3, 40, 12, 2, 4, 10
omega = np.exp(2j*np.pi/3)
n_lines = v * k // (q+1)
CF_W33 = mu / v

print('CF=1/10 Measurement Runbook')
print('='*50)
print(f'  v={v} points, {n_lines} contexts, target CF={CF_W33}')

T = np.array([[omega**(i*j)/np.sqrt(3) for j in range(3)] for i in range(3)])
assert np.allclose(T @ T.conj().T, np.eye(3))
print('Tritter T_ij = omega^(ij)/sqrt(3): UNITARY VERIFIED')

N_shots = 1000
CF_doily = 0
sigma = np.sqrt(CF_W33*(1-CF_W33)/N_shots)
zscore = (CF_W33 - CF_doily) / sigma
print(f'Separation CF=0.1 vs CF=0: {zscore:.1f} sigma at N={N_shots}/context')
print()
print('Hardware: tritter + 3x EOM + 3x SNSPD (telecom-band)')
print(f'Protocol: {v} states x {n_lines} contexts x {N_shots} shots = {v*n_lines*N_shots:.0e} total')
print(f'Duration: {N_shots*n_lines/1e5:.1f} s at 100 kHz')
print('Decision: CF=0.00+-0.01 => doily/q=2  CF=0.10+-0.01 => W33/q=3')
