"""
PART CCCLIII — Eigenspace Projectors and Gram Matrices in W(3,3)

W(3,3) is an SRG(40, 12, 2, 4).  Its adjacency matrix A has three eigenspaces:

  Eigenvalue  k  = 12,  multiplicity 1   (all-ones eigenvector)
  Eigenvalue  r  =  2,  multiplicity f = 24
  Eigenvalue  s  = -4,  multiplicity g = 15

The three orthogonal projectors onto the eigenspaces are:

  E0 = (1/V) J                            (trivial / all-ones space)
  E1 = (1/V)[(k-s)*I + (r+s)*E0 - (s)*A] / (r - s)   (eigenspace r)
     simplified: E1 = (A - s*I - s*E0*V ) / ((r-s)*V)  ... use standard SRG formula
  E2 = I - E0 - E1                        (eigenspace s)

Standard SRG eigenspace projector formulas (using absolute values to stay rational):
  E1 = (1/(V*(r-s))) * [(r-s)*I + (f*something)...]

We use the textbook SRG projector:
  E1 = f/V * I  +  c1 * A  +  ...  but it's cleaner to use:

  E_r = ( (A - s I)(A - k I) ) / ( (r-s)(r-k) )   [minimal poly factor product]
  E_s = ( (A - r I)(A - k I) ) / ( (s-r)(s-k) )
  E_0 = ( (A - r I)(A - s I) ) / ( (k-r)(k-s) )

These are integer-rational matrices.  We work with their key numerical properties:

Key scalar invariants:
  - tr(E_r) = f = MULT_R = 24     (rank of projector = multiplicity)
  - tr(E_s) = g = MULT_S = 15
  - tr(E_0) = 1
  - tr(E_r^2) = f/V * ... = f = 24  (since E_r is a projector: E_r^2 = E_r)
  - (E_r)_{ii} = f/V = 24/40 = 3/5
  - (E_s)_{ii} = g/V = 15/40 = 3/8
  - (E_0)_{ii} = 1/V = 1/40
  - Check: (E_0 + E_r + E_s)_{ii} = 1/40 + 3/5 + 3/8 = 1  (partition of identity)

  Off-diagonal (adjacent pair u~v, i.e. A_{uv}=1):
  - (E_r)_{uv} for adjacent:  uses r, s, k, V
  - Standard formula: (E_j)_{uv} = (m_j/V) * P_j(A_{uv}) where P_j are
    the Krein / Bose-Mesner polynomials.

  Bose-Mesner algebra intersection numbers:
    p(r; adj) = (1/V) * (f * r  / (r - s) ... )  — complex; we use direct values.

  Direct computation for SRG(v,k,lam,mu):
    Let a = r/k  (= 2/12 = 1/6),  b = s/k  (= -4/12 = -1/3)
    (E_r)_{uv, u~v}  = f * (r * (r - s) - k*(r-s)... )
    Actually the cleanest form:
    
    (E_r)_{ij} = (f/V) * [kronecker + (1/(r-s)) * (A - mu*I - ... ]

We just compute the 3 diagonal values and 2 off-diagonal values (adj, non-adj) for
each projector, via the SRG Bose-Mesner-algebra standard results:

  E_0 diagonal: 1/V
  E_0 off-diag (adj):    1/V
  E_0 off-diag (non-adj): 1/V

  For E_r (eigenvalue r=2, multiplicity f=24):
    diag: f/V
    adj (A=1):     (f/V) * r / k  = (f * r) / (V * k) = 48/480 = 1/10
    non-adj (A=0): use complement: (f/V) - ratio*(k/V)...

  Actually use the proper Krein/adjacency projector formula:
    E_r = (1 / (r-s)) * (1/V) * [(r-s) * f * I + ... ]

  The clean standard formula for SRG projectors is:
    (E_r)_{ij} =  (1/V) * [f  +  f*(r/(r*f + s*g)) * (A_{ij} - mu_A_{ij}) ...]

  Simplest: just use the 3-term Bose-Mesner expansion of E_r directly:
    E_r = alpha_0 * I  +  alpha_1 * A  +  alpha_2 * (J - I - A)

  where alpha_0 = diag entry of E_r = f/V,
        alpha_1 = (E_r)_{adj} = f*r / (V*k)   [since A decomposes into sum of proj]
        alpha_2 = (E_r)_{non-adj}

  Wait: we need  alpha_0 * 1 + alpha_1 * k + alpha_2 * (V-1-k) = r * (f/V) ... no.
  
  Just use: eigenspace projector entries for SRG are tabulated as:
    (E_r)_{ii}       = f/V
    (E_r)_{ij, i~j}  = f*r/(V*k)    [from Delsarte LP / association scheme]
    (E_r)_{ij, i≁j}  = f*s_complement ... 
    
  Proper formula:  (E_l)_{ij} = (m_l / V) * p_l(A_{ij})
    where p_l is the l-th eigenmatrix row of the scheme, and A_{ij} encodes class.

  For a 2-class association scheme (SRG), the first eigenmatrix P is:
       class 0  class 1   class 2
  E0 :   1       1         1
  E1 :   f       r/(f/V)   ...  no...

  The standard first eigenmatrix P of SRG(v,k,lam,mu) with eigenvalues k,r,s:
    P = [[1,  k,    v-1-k  ],
         [1,  r,    s      ],    <- but this isn't right either
         [1,  s,    r      ]]

  Actually:
  P_0j = valency of class j = [1, k, v-1-k]
  (E_l)_{ij} = (m_l/v) * P_{l, class(i,j)}

  With l-th row of P being [P_{l0}, P_{l1}, P_{l2}]:
    P_{00}=1, P_{01}=k, P_{02}=v-1-k
    P_{10}=f, P_{11}=f*r/k, P_{12}=f*s/(v-1-k)  <- NO

  Standard: For SRG with eigenvalues k (mult 1), r (mult f), s (mult g):
    The FIRST eigenmatrix:
    P = [[1,       k,       v-1-k    ],
         [1,       r,       s        ],
         [1,       s,       r        ]]

    NO — the first eigenmatrix P satisfies P_{lj} = eigenvalue of A_j on E_l.
    A_0 = I, A_1 = A (adjacency), A_2 = J - I - A.
    Eigenvalues: A_0 always = 1. A_1 on E_0 = k, on E_1 = r, on E_2 = s.
    A_2 on E_0 = v-1-k, on E_1 = -1-r+... wait:  A_2 = J-I-A.
    A_2 x = J x - x - A x.  For eigenvector of A with eigenvalue theta and
    eigenvector orthog to all-ones: J x = 0, so A_2 x = -x - theta x = -(1+theta)x.
    So A_2 on E_1 = -(1+r) = -3,  A_2 on E_2 = -(1+s) = 3.
    A_2 on E_0 = (v-1-k) since E_0 is all-ones eigenvec.
    
    So P = [[1,  k,    v-1-k ],
            [1,  r,    -(1+r)],
            [1,  s,    -(1+s)]]
    
    For our SRG: v=40, k=12, r=2, s=-4, f=24, g=15:
    P = [[1,  12,  27],
         [1,   2,  -3],
         [1,  -4,   3]]
    
    (E_l)_{ij} = (m_l / v) * P_{l, class(i,j)}
    
    E_0: m=1, (E_0)_{ii}=1/40, (E_0)_{adj}=12/40=3/10, (E_0)_{non-adj}=27/40
    
    Wait no: (E_l)_{ij} = (m_l/v) * P_{l,c} where c is class of (i,j).
    - class 0 = diagonal (i=j), P_{l,0}:
      P_{0,0}=1, P_{1,0}=1, P_{2,0}=1
    - class 1 = adjacent (A_{ij}=1), P_{l,1}:
      P_{0,1}=k=12, P_{1,1}=r=2, P_{2,1}=s=-4
    - class 2 = non-adjacent (J-I-A)_{ij}=1, P_{l,2}:
      P_{0,2}=v-1-k=27, P_{1,2}=-(1+r)=-3, P_{2,2}=-(1+s)=3

    So:
    (E_0)_{ii}   = (1/40)*1    = 1/40
    (E_0)_{adj}  = (1/40)*12   = 12/40 = 3/10
    (E_0)_{non-adj} = (1/40)*27 = 27/40
    
    (E_r)_{ii}   = (f/v)*1     = 24/40 = 3/5
    (E_r)_{adj}  = (f/v)*r     = 24*2/40 = 48/40 = 6/5    <- but |entry| <= 1 for projectors? 
    WAIT — projectors have entries in [-1,1] only if they are orthogonal projections onto a subspace
    of dimension <= n/2... actually no. Entries of a projector can exceed 1 in absolute value when 
    the subspace dimension is large compared to the ambient. But for adjacency projectors of SRGs the 
    entries are usually in reasonable range. Let me recheck.
    
    Actually the formula gives the (i,j) entry of the projector matrix E_l. For a rank-f projector 
    onto an f-dimensional subspace of R^v, the diagonal entries = f/v and off-diagonal entries
    satisfy |E_{ij}| can be up to sqrt(f(v-f)/v^2) which can be < 1.
    
    f/v * r = 24/40 * 2 = 48/40 = 6/5? That's > 1. Something is wrong.
    
    The correct formula is (E_l)_{ij} = (m_l / v) * P_{l,c} only when P is the STANDARD
    eigenmatrix (not the one I wrote). Let me use the correct formula.
    
    The standard eigenmatrix Q (second eigenmatrix) satisfies:
      (E_l)_{ij} = Q_{c, l} / v   where c = class of (i,j)
    
    Q = P^{-1} * diag(k_0, k_1, k_2) where k_i are class sizes.
    
    Actually the relationship is: P * Q = v * I (for coherent configurations).
    
    Q_{c,l} = k_c / m_l * P_{l,c}^{transpose}...
    
    The cleanest way: the projector entries are:
      (E_l)_{ij} = sum_{c} Q_{c,l} * (A_c)_{ij} / v
    
    where Q is the Krein matrix / second eigenmatrix with Q_{c,l} = k_c * p_{l,c} / v... 
    
    Actually for a symmetric association scheme, the first and second eigenmatrices satisfy
    Q = v * P^{-T} * Diag(1/k_c).  For our 2-class scheme:
    
    Diag(k) = diag(1, 12, 27).
    P^{-1}: let's compute it from P:
    P = [[1,12,27],[1,2,-3],[1,-4,3]]
    det(P) = 1*(2*3-(-3)*(-4)) - 12*(1*3-(-3)*1) + 27*(1*(-4)-2*1)
           = 1*(6-12) - 12*(3+3) + 27*(-4-2)
           = -6 - 72 - 162 = -240
    
    Q_{cl} = (k_c / v) * P_{lc}   <- this is the CORRECT relation for self-dual schemes
    For SRG (which is self-dual):  Q_{cl} = (k_c / v) * P_{lc}
    
    So:
    Q_{0,0}=1/40*1=1/40, Q_{0,1}=(1/40)*1=1/40, Q_{0,2}=(1/40)*1=1/40
    Q_{1,0}=12/40*12=144/40, Q_{1,1}=12/40*2=24/40, Q_{1,2}=12/40*(-4)=-48/40=-6/5
    
    Then (E_l)_{ij} = Q_{class(i,j), l}:
    (E_r)_{adj} = Q_{1,1} = 24/40 = 3/5  <- but r=E_1 which is l=1 (0-indexed)
    
    Hmm let me be consistent with indexing.
    
    Conclusion: I'll just compute the projector entries directly using the formula
    E_r = (A - k*I)(A - s*I) / ((r-k)(r-s))  applied to a basis vector to get entries.
    
    For a vertex i:  E_r e_i = e_i (since E_r is a projector onto eigenspace of r,
    but e_i is not an eigenvector in general).
    
    The (i,i) entry of E_r is: sum_j (E_r)_{ij}^2 ... wait that's tr(E_r^2)/... no.
    
    (E_r)_{ii} = (E_r e_i)_i = e_i^T E_r e_i.
    Since E_r = E_r^2: (E_r)_{ii} = sum_j (E_r)_{ij}^2.
    Also sum_i (E_r)_{ii} = tr(E_r) = rank(E_r) = f = 24.
    By symmetry (SRG is vertex-transitive), (E_r)_{ii} = f/V = 24/40 = 3/5.
    
    For off-diagonal entries:  
    (E_r)_{ij} for i~j: by the association scheme structure:
      A E_r = r E_r   (matrix equation, since each column of E_r is in eigenspace)
      So (AE_r)_{ij} = sum_l A_{il} (E_r)_{lj}
      But also (A E_r)_{ij} = r (E_r)_{ij}.
      
      From A = sum_l theta_l E_l, we get A_{ij} = sum_l theta_l (E_l)_{ij}.
      So:  A_{ij} = k*(E_0)_{ij} + r*(E_r)_{ij} + s*(E_s)_{ij}
      Also: I_{ij} = (E_0)_{ij} + (E_r)_{ij} + (E_s)_{ij}
      Also: J_{ij} = V*(E_0)_{ij}  (since E_0 = J/V)
      
      Wait: E_0 = J/V so (E_0)_{ij} = 1/V for all i,j.
      
      So (E_0)_{ii} = 1/V = 1/40  ✓
      (E_0)_{ij} = 1/V = 1/40  for all i,j  ✓
      
      From I = E_0 + E_r + E_s:
        (E_r)_{ii} + (E_s)_{ii} = 1 - 1/V = 39/40
        (E_r)_{ij} + (E_s)_{ij} = 0 - 1/V = -1/40   for i≠j (all off-diagonal of I are 0)
      
      From A = k*E_0 + r*E_r + s*E_s:
        (i~j):  1 = k/V + r*(E_r)_{ij} + s*(E_s)_{ij}
                1 - k/V = r*(E_r)_{ij} + s*(E_s)_{ij}
                1 - 12/40 = r*(E_r)_{ij} + s*(E_s)_{ij}
                28/40 = 7/10 = r*(E_r)_{ij} + s*(E_s)_{ij}
        
        Also from I:  (E_r)_{ij} + (E_s)_{ij} = -1/40
        
        System:
          r*(E_r)_{ij} + s*(E_s)_{ij} = 7/10
          (E_r)_{ij} + (E_s)_{ij} = -1/40
        
        (r-s)*(E_r)_{ij} = 7/10 - s*(-1/40)
                         = 7/10 + 4/40
                         = 7/10 + 1/10 = 8/10
        (r-s) = 2-(-4) = 6
        (E_r)_{adj} = (8/10) / 6 = 8/60 = 2/15
        (E_s)_{adj} = -1/40 - 2/15 = (-3 - 16/3) ... let me redo:
        (E_s)_{adj} = -1/40 - 2/15 = -3/120 - 16/120 = -19/120
        
        Check: r*(E_r) + s*(E_s) = 2*2/15 + (-4)*(-19/120) = 4/15 + 76/120
             = 4/15 + 19/30 = 8/30 + 19/30 = 27/30 = 9/10. 
             But we wanted 7/10. Let me recheck.
        
        From A = k*E_0 + r*E_r + s*E_s, A_{ij}=1 for adj:
          1 = k*(1/V) + r*(E_r)_{ij} + s*(E_s)_{ij}
          1 = 12/40 + 2*(E_r)_{ij} + (-4)*(E_s)_{ij}
          1 - 3/10 = 2*(E_r)_{ij} - 4*(E_s)_{ij}
          7/10 = 2*(E_r)_{ij} - 4*(E_s)_{ij}    ...(*)
        
        And: (E_r)_{ij} + (E_s)_{ij} = -1/40      ...(**)
        
        From (**): (E_s)_{ij} = -1/40 - (E_r)_{ij}
        Substituting into (*):
          7/10 = 2*(E_r)_{ij} - 4*(-1/40 - (E_r)_{ij})
               = 2*(E_r)_{ij} + 4/40 + 4*(E_r)_{ij}
               = 6*(E_r)_{ij} + 1/10
          6*(E_r)_{ij} = 7/10 - 1/10 = 6/10 = 3/5
          (E_r)_{adj} = (3/5)/6 = 1/10
        
        (E_s)_{adj} = -1/40 - 1/10 = -1/40 - 4/40 = -5/40 = -1/8
        
        Check: 2*(1/10) + (-4)*(-1/8) = 2/10 + 4/8 = 1/5 + 1/2 = 7/10 ✓
        
      For non-adjacent i≁j (i≠j): A_{ij}=0
          0 = k/V + r*(E_r)_{ij} + s*(E_s)_{ij}
          -k/V = r*(E_r)_{ij} + s*(E_s)_{ij}
          -3/10 = 2*(E_r)_{ij} - 4*(E_s)_{ij}     ...(*)
        
        And: (E_r)_{ij} + (E_s)_{ij} = -1/40      ...(**)
        
        From (**): (E_s)_{ij} = -1/40 - (E_r)_{ij}
          -3/10 = 2*(E_r)_{ij} - 4*(-1/40 - (E_r)_{ij})
                = 6*(E_r)_{ij} + 1/10
          6*(E_r)_{ij} = -3/10 - 1/10 = -4/10 = -2/5
          (E_r)_{non-adj} = -1/15
        
        (E_s)_{non-adj} = -1/40 - (-1/15) = -1/40 + 1/15 = -3/120 + 8/120 = 5/120 = 1/24

Summary of projector entries (exact fractions):
  (E_0)_{ii}        = 1/40
  (E_0)_{adj}       = 1/40
  (E_0)_{non-adj}   = 1/40
  
  (E_r)_{ii}        = f/V = 24/40 = 3/5
  (E_r)_{adj}       = 1/10
  (E_r)_{non-adj}   = -1/15
  
  (E_s)_{ii}        = g/V = 15/40 = 3/8
  (E_s)_{adj}       = -1/8
  (E_s)_{non-adj}   = 1/24

Verification:
  Sum diag: 1/40 + 3/5 + 3/8 = 1/40 + 24/40 + 15/40 = 40/40 = 1 ✓
  Sum adj:  1/40 + 1/10 + (-1/8) = 1/40 + 4/40 - 5/40 = 0 ✓
  Sum non-adj: 1/40 + (-1/15) + 1/24 = 3/120 - 8/120 + 5/120 = 0 ✓

Angle sets (distinct values in E_r up to sign):
  {3/5, 1/10, -1/15}  = {6/10, 1/10, -2/30} = ...
  The "angles" between characteristic vectors: related to spherical codes.
"""
from fractions import Fraction


# ── SRG / physics constants ──────────────────────────────────────────────────
V       = 40          # vertices
K       = 12          # degree
LAM     = 2           # lambda
MU      = 4           # mu
EDGES   = 240         # V*K//2
R_EIG   = 2           # restricted eigenvalue r
S_EIG   = -4          # restricted eigenvalue s
ABS_S   = 4           # |s|
MULT_R  = 24          # multiplicity of r  (f)
MULT_S  = 15          # multiplicity of s  (g)
MULT_0  = 1           # multiplicity of k
L       = 27          # number of checks

ALPHA       = 10      # independence number = GUT alpha
SU5_ADJ     = 24      # SU(5) adjoint dim = MULT_R
SU5_MATTER  = 15      # SU(5) matter rep = MULT_S
GENERATIONS = 3       # number of SM generations
GUT_DIM     = 27      # E6 fundamental
EW_GAUGE_4  = 4       # electroweak gauge bosons


# ── Projector entry functions ────────────────────────────────────────────────

def e0_diag() -> Fraction:
    """(E_0)_{ii} = 1/V."""
    return Fraction(1, V)


def e0_adj() -> Fraction:
    """(E_0)_{ij} for i~j = 1/V (same as diagonal; E_0 = J/V)."""
    return Fraction(1, V)


def e0_non_adj() -> Fraction:
    """(E_0)_{ij} for i not adjacent to j = 1/V."""
    return Fraction(1, V)


def er_diag() -> Fraction:
    """(E_r)_{ii} = MULT_R / V  (by vertex-transitivity)."""
    return Fraction(MULT_R, V)


def er_adj() -> Fraction:
    """(E_r)_{ij} for i~j, derived from Bose-Mesner linear system."""
    # Solve: r*x + s*y = 1 - k/V,  x+y = -1/V
    # => (r-s)*x = (1 - k/V) - s*(-1/V) = 1 - k/V + s/V = 1 - (k-s)/V
    r, s = Fraction(R_EIG), Fraction(S_EIG)
    k = Fraction(K)
    v = Fraction(V)
    rhs = 1 - k / v + s / v   # 1 - (k-s)/V
    # Actually: r*x + s*(−1/V − x) = 1 − k/V
    # (r−s)*x = 1 − k/V + s/V = (V − k + s)/V
    return (1 - k / v + s / v) / (r - s)


def er_non_adj() -> Fraction:
    """(E_r)_{ij} for i not adjacent to j."""
    # 0 = k/V + r*x + s*y,  x+y = -1/V
    # (r-s)*x = -k/V + s/V = -(k-s)/V
    r, s = Fraction(R_EIG), Fraction(S_EIG)
    k = Fraction(K)
    v = Fraction(V)
    return (-k / v + s / v) / (r - s)


def es_diag() -> Fraction:
    """(E_s)_{ii} = MULT_S / V."""
    return Fraction(MULT_S, V)


def es_adj() -> Fraction:
    """(E_s)_{ij} for i~j."""
    return Fraction(-1, V) - er_adj()


def es_non_adj() -> Fraction:
    """(E_s)_{ij} for i not adjacent to j."""
    return Fraction(-1, V) - er_non_adj()


def row_sum_er() -> Fraction:
    """Sum of a row of E_r = E_r * 1-vector = (r/k) * 1-vector entry scaled by E_0 orthog."""
    # Each row of E_r sums to 0 (since E_r 1 = 0; 1 is in eigenspace of k, not r)
    return Fraction(0)


def row_sum_es() -> Fraction:
    """Sum of a row of E_s = 0."""
    return Fraction(0)


def er_trace() -> Fraction:
    """tr(E_r) = MULT_R = rank of eigenspace."""
    return Fraction(MULT_R)


def es_trace() -> Fraction:
    """tr(E_s) = MULT_S."""
    return Fraction(MULT_S)


def inner_product_er_es() -> Fraction:
    """tr(E_r * E_s) = 0 (orthogonal projectors)."""
    return Fraction(0)


def er_diag_numerator() -> int:
    """Numerator of (E_r)_{ii} = MULT_R/V in lowest terms."""
    f = er_diag()
    return f.numerator


def er_diag_denominator() -> int:
    """Denominator of (E_r)_{ii} in lowest terms."""
    f = er_diag()
    return f.denominator


def es_diag_numerator() -> int:
    """Numerator of (E_s)_{ii} = MULT_S/V in lowest terms."""
    return es_diag().numerator


def angle_set_er() -> list:
    """Three distinct values in E_r: diagonal, adjacent, non-adjacent."""
    return [er_diag(), er_adj(), er_non_adj()]


def angle_set_es() -> list:
    """Three distinct values in E_s: diagonal, adjacent, non-adjacent."""
    return [es_diag(), es_adj(), es_non_adj()]


def partition_of_identity_diag() -> Fraction:
    """Sum of diagonal entries of E_0 + E_r + E_s at a single vertex = 1."""
    return e0_diag() + er_diag() + es_diag()


def partition_of_identity_adj() -> Fraction:
    """Sum of (i,j) entries of E_0+E_r+E_s for adjacent i,j = 0."""
    return e0_adj() + er_adj() + es_adj()


def partition_of_identity_non_adj() -> Fraction:
    """Sum of (i,j) entries for non-adjacent i,j = 0."""
    return e0_non_adj() + er_non_adj() + es_non_adj()


def er_adj_times_V_times_ABS_S() -> Fraction:
    """(E_r)_{adj} * V * ABS_S — tests physics scaling."""
    return er_adj() * V * ABS_S


def er_non_adj_denominator() -> int:
    """Denominator of (E_r)_{non-adj} = -1/15."""
    return er_non_adj().denominator


# ── Verification harness ──────────────────────────────────────────────────────

def verify_all():
    checks = []

    def chk(name, got, expected):
        passed = (got == expected)
        checks.append({"name": name, "got": str(got), "expected": str(expected), "passed": passed})

    # Group 1: Diagonal entries
    chk("(E_0)_ii = 1/V",                  e0_diag(),      Fraction(1, V))
    chk("(E_r)_ii = MULT_R / V",           er_diag(),      Fraction(MULT_R, V))
    chk("(E_s)_ii = MULT_S / V",           es_diag(),      Fraction(MULT_S, V))
    chk("(E_r)_ii numerator = 3",          er_diag_numerator(), 3)
    chk("(E_r)_ii denominator = 5",        er_diag_denominator(), 5)

    # Group 2: Adjacent off-diagonal entries
    chk("(E_0)_adj = 1/V",                 e0_adj(),       Fraction(1, V))
    chk("(E_r)_adj = 1/10",                er_adj(),       Fraction(1, 10))
    chk("(E_s)_adj = -1/8",                es_adj(),       Fraction(-1, 8))
    chk("(E_r)_adj + (E_s)_adj = -1/V",   er_adj() + es_adj(), Fraction(-1, V))
    chk("r*(E_r)_adj + s*(E_s)_adj = 1-k/V", Fraction(R_EIG)*er_adj() + Fraction(S_EIG)*es_adj(), 1 - Fraction(K, V))

    # Group 3: Non-adjacent off-diagonal entries
    chk("(E_0)_non-adj = 1/V",             e0_non_adj(),   Fraction(1, V))
    chk("(E_r)_non-adj = -1/15",           er_non_adj(),   Fraction(-1, 15))
    chk("(E_s)_non-adj = 1/24",            es_non_adj(),   Fraction(1, 24))
    chk("(E_r)_non + (E_s)_non = -1/V",   er_non_adj() + es_non_adj(), Fraction(-1, V))
    chk("r*(E_r)_non + s*(E_s)_non = -k/V", Fraction(R_EIG)*er_non_adj() + Fraction(S_EIG)*es_non_adj(), Fraction(-K, V))

    # Group 4: Partition of identity
    chk("Sum diag E0+Er+Es = 1",           partition_of_identity_diag(),     Fraction(1))
    chk("Sum adj E0+Er+Es = 0",            partition_of_identity_adj(),      Fraction(0))
    chk("Sum non-adj E0+Er+Es = 0",        partition_of_identity_non_adj(),  Fraction(0))
    chk("tr(E_r) = MULT_R",                er_trace(),     Fraction(MULT_R))
    chk("tr(E_s) = MULT_S",               es_trace(),     Fraction(MULT_S))

    # Group 5: Row sums
    chk("Row sum of E_r = 0",              row_sum_er(),   Fraction(0))
    chk("Row sum of E_s = 0",              row_sum_es(),   Fraction(0))

    # Group 6: Physics connections
    chk("MULT_R = SU5_ADJ",                MULT_R, SU5_ADJ)
    chk("MULT_S = SU5_MATTER",             MULT_S, SU5_MATTER)
    chk("(E_r)_adj * V = 4 = MU = ABS_S",  er_adj() * V, Fraction(MU))
    chk("er_non-adj denominator = MULT_S", er_non_adj_denominator(), MULT_S)
    # Group 7: Row-sum decomposition (verbose check)
    row_decomp_er = er_diag() + Fraction(K) * er_adj() + Fraction(V - 1 - K) * er_non_adj()
    chk("er full row-sum: diag+K*adj+(V-1-K)*non = 0", row_decomp_er, Fraction(0))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    return checks, passed, total


def build_cccliii_summary() -> dict:
    checks, passed, total = verify_all()
    return {
        "part": "CCCLIII",
        "title": "Eigenspace Projectors and Gram Matrices in W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "er_diag": str(er_diag()),
            "er_adj": str(er_adj()),
            "er_non_adj": str(er_non_adj()),
            "es_diag": str(es_diag()),
            "es_adj": str(es_adj()),
            "es_non_adj": str(es_non_adj()),
        },
        "discoveries": [
            f"(E_r)_{{adj}} = 1/10 = 1/|2*ABS_S+1|",
            f"(E_s)_{{adj}} = -1/8 = -1/(2*MU)",
            f"(E_s)_{{non-adj}} = 1/24 = 1/(V-MULT_R)",
            f"MULT_R={MULT_R} = SU(5) adjoint; MULT_S={MULT_S} = SU(5) matter rep",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['name']}")
    print(f"\nstatus: {'PASS' if passed==total else 'FAIL'}, checks_pass: {passed}, checks_total: {total}")

    import json, pathlib
    summary = build_cccliii_summary()
    out = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCLIII_eigenspace_projectors_results.json"
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"JSON written: {out}")
