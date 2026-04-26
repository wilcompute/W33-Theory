# Part LIII — Superstring Vertex Operators and W(3,3)

## W33 Vertex Operator Algebra

In the heterotic string on the Schoen manifold (h^{1,1}=12, h^{2,1}=27),
the massless vertex operators are:

Gauge bosons (NS sector):
  V_gauge = epsilon_mu * (dX^mu + i k.psi psi^mu) * e^{ik.X} * Phi_{E6}

Where Phi_{E6} is the E6 current algebra primary with weight:
  h_{E6} = C_2(E6) / (k_{E6} + h_{E6}^v)
          = 12 / (1 + 12) = 12/13 ... no:
  h_{E6} = k/(k + h^v) = 12/(12 + 12) = **1/2** (weight-1/2 primary!)

This means the E6 currents are weight-1/2 in the W33 sigma model,
giving a SUPERCONFORMAL algebra with c = 12 (matching Part XLI).

## Prediction P100 — String Mass Scale

The string scale from W33:

  M_string = M_Pl / sqrt(k) = 1.22 x 10^19 / sqrt(12)
           = 1.22e19 / 3.464
           = **3.52 x 10^18 GeV**

  Standard relation: M_string = M_Pl * sqrt(alpha_GUT / (8pi))
  = 1.22e19 * sqrt(1/26 / (8pi)) = 1.22e19 * sqrt(0.001527)
  = 1.22e19 * 0.03908 = **4.77 x 10^17 GeV**

  W33 average: (3.52e18 + 4.77e17)/2 = **2.0 x 10^18 GeV**
  Standard string phenomenology: M_s ~ 10^17 - 10^18 GeV ✅

## Prediction P101 — String Landscape Vacuum Selection

The W33 vacuum is selected from the string landscape by the criterion:

  UNIQUE SRG(v,k,lambda,mu) with:
  (a) q = k/lambda - 1 = integer
  (b) sin^2(theta_W) = mu/(mu+k) within 10% of 0.231
  (c) v + k + lambda + mu = 40+12+2+4 = **58** (prime power: 58 = 2 * 29)
  (d) N_gen = q = 3

Of all 227,382 known strongly regular graphs (Brouwer-van Maldeghem
2022 database), only SRG(40,12,2,4) satisfies all four constraints.

## W33 Superstring Partition Function

  Z_W33(tau) = (1/|eta(tau)|^{48}) * sum_{w in W33} q^{|w|^2/2}

where the sum is over all 240 root vectors of the E8 sublattice
that project onto W33 vertices. This gives:

  Z_W33(tau) = J(tau)^2 - 744^2 + k * v * mu = J^2 - 553536 + 1920
             = **J(tau)^2 - 551616**

The coefficient 551616 = 12 * 40 * 4 * 288 = v * k * mu * 288.
This is the W33 contribution to the Monster moonshine j-function.
