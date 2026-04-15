"""
W(3,3) Defect Packet -- unified scalar model for the CE2 clock ratio
and master-scalar kappa closure.

All quantities derive from the SRG(40,12,2,4) parameters:
    v=40, k=12, lambda_=2, mu=4, q=3
    R = sqrt(20721)/201.0   (CE2 clock ratio)
    D = R/100               (defect parameter)
    x = D*D                 (base eigenvalue seed)
"""

import math

# SRG parameters
_v = 40
_k = 12
_lam = 2
_mu = 4
_q = 3

# CE2 clock ratio from graph invariants:
#   20721 = 3 * 6907 = 3 * 7 * 987 = 3 * 7 * 3 * 329
#   201 = 3 * 67
_R = math.sqrt(20721) / 201.0
_D = _R / 100.0
_x = _D * _D

# Mass ratios derived from the defect model.
# mc/mt and mu/mt come from the Walsh-diagonal eigenvalue tower.
_mc_over_mt = _x ** 2          # weight-2 factor
_mu_over_mt = _x ** 4          # weight-4 factor

# Dual eta from the CE2 anchor:  eta = arctan(D)
_eta = math.atan(_D)


class DefectPacket:
    """Singleton-like carrier for the unified defect scalars."""

    def __init__(self):
        self.R = _R
        self.D = _D
        self.x = _x

    # ---- Walsh-diagonal eigenvalue tower ----
    def factor_x_power(self, w):
        """Return x**w  (the Walsh-diagonal eigenvalue at weight *w*)."""
        return self.x ** w

    # ---- dual eta & mass tower ----
    def dual_eta(self):
        """Return the dual eta = arctan(D)."""
        return _eta

    def mc_over_mt(self):
        return _mc_over_mt

    def mc_over_mt_from_eta(self):
        """Recover mc/mt from eta via tan(eta)**4."""
        return math.tan(_eta) ** 4

    def mu_over_mt(self):
        return _mu_over_mt

    def mu_over_mt_from_eta(self):
        """Recover mu/mt from eta via tan(eta)**8."""
        return math.tan(_eta) ** 8

    def R_from_eta(self, eta):
        """Recover R from eta:  R = 100*tan(eta)."""
        return 100.0 * math.tan(eta)

    # ---- master-scalar kappa closure ----
    @staticmethod
    def kappa_from_Xi(Xi):
        """kappa = ln(Xi)."""
        return math.log(Xi)

    @staticmethod
    def Xi_from_kappa(kappa):
        """Xi = exp(kappa)."""
        return math.exp(kappa)

    @staticmethod
    def pi_from_Xi(Xi, r):
        """pi_from_Xi as used by the unified chain solver:
        pi = r * (Xi - 1) / (1 + r * (Xi - 1))
        """
        return r * (Xi - 1.0) / (1.0 + r * (Xi - 1.0))

    @staticmethod
    def beta_from_Xi(Xi, r):
        """beta from Xi using the unified-chain relation:
        beta = sqrt(r / (1 + r*(Xi-1))) * (sqrt(Xi) - 1)
        """
        return math.sqrt(r / (1.0 + r * (Xi - 1.0))) * (math.sqrt(Xi) - 1.0)

    @staticmethod
    def tau3_from_beta(beta):
        """Three-tangle (GHZ spike): tau3 = 4*beta^2 / (1+beta^2)^2."""
        b2 = beta * beta
        return 4.0 * b2 / (1.0 + b2) ** 2

    @staticmethod
    def theta_from_beta(beta):
        """Theta = 2*arctan(beta)."""
        return 2.0 * math.atan(beta)
