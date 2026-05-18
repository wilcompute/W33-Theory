"""
Core W(3,3) substrate parameters and geometric constants.
No fitted parameters or free variables are permitted here.
"""

import math

# Fundamental graph primitives
q = 3
lambda_ = 2
mu = 4
q_bang = 6
Phi6 = 7
Phi4 = 10
k = 12
Phi3 = 13
g = 15          # Multiplicity of the negative Laplacian eigenvalue
f = 24          # Fine structure coupling dimension
q_pow_q = 27
T7 = 28         # Affine triality frame constraint
v = 40          # Vertices / Witting rays
H1 = 81         # Protected matters sector dimension
alpha_inv = 137 # Zero-momentum UV Fine-Structure anchor
E = 240         # Graph Edges
E8_dim = 248    # E8 algebra dimension
tau_O = 384     # Octahedron spanning trees

# Transcendental fixed points
phi = (1 + math.sqrt(5)) / 2
pi = math.pi
e = math.e

# Monument limits
Leech_kissing = 196560
Monster_rep = 196883
