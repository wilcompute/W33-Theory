#!/usr/bin/env python3
"""
Step 1: S3 Chirality Controller — Complete Jones Matrix Circuit
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
import numpy as np

omega = np.exp(2j * np.pi / 3)

def hwp_jones(theta_deg):
    theta = np.radians(theta_deg)
    return np.array([[np.cos(2*theta), np.sin(2*theta)],
                     [np.sin(2*theta), -np.cos(2*theta)]])

def qwp_jones(theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c**2 + 1j*s**2, (1-1j)*c*s],
                     [(1-1j)*c*s, s**2 + 1j*c**2]])

H = np.array([1, 0])
V = np.array([0, 1])
L = np.array([1, -1j]) / np.sqrt(2)
R = np.array([1,  1j]) / np.sqrt(2)

QWP_45 = qwp_jones(45)

print('S3 Chirality Controller: Jones Matrix Analysis')
print('='*50)
print('Polarisation-chirality mapping:')
print('  |L> = (|H> - i|V>)/sqrt(2)  ->  5_omega  (left chirality)')
print('  |R> = (|H> + i|V>)/sqrt(2)  ->  5_omega^2 (right chirality)')
print('  |H> = rational background   ->  30 channel')
print()

L_V_prob = abs(np.dot(V.conj(), QWP_45 @ L))**2
R_H_prob = abs(np.dot(H.conj(), QWP_45 @ R))**2
assert abs(L_V_prob - 1.0) < 1e-10, f'L->V failed: {L_V_prob}'
assert abs(R_H_prob - 1.0) < 1e-10, f'R->H failed: {R_H_prob}'
print(f'QWP(45) routes |L>->|V> with prob: {L_V_prob:.4f} (VERIFIED)')
print(f'QWP(45) routes |R>->|H> with prob: {R_H_prob:.4f} (VERIFIED)')
print()

S3_elements = {
    'e':    np.eye(2, dtype=complex),
    'C3':   np.diag([omega, omega.conj()]),
    'C3^2': np.diag([omega**2, omega.conj()**2]),
    'tau1': np.array([[0,1],[1,0]], dtype=complex),
}
S3_elements['tau2'] = S3_elements['C3'] @ S3_elements['tau1']
S3_elements['tau3'] = S3_elements['C3^2'] @ S3_elements['tau1']

for name, M in S3_elements.items():
    assert np.allclose(M @ M.conj().T, np.eye(2)), f'{name} not unitary!'
    pL = abs(np.dot(L.conj(), M@L))**2
    pR = abs(np.dot(R.conj(), M@L))**2
    print(f'  {name}: unitary VERIFIED, |L>->{pL:.2f}|L>+{pR:.2f}|R>')

print()
print('Circuit: PBS -> QWP(45deg) -> EOM(2Vpi/3) -> HWP(0deg) -> QWP(-45deg)')
print('Port A: 5_omega (left chirality), Port B: 5_omega^2 (right chirality)')
print('EOM voltage: V_C3 = (2/3)*V_pi')
