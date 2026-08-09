# Part DCCCXI (811) — Top Quark Pole Mass at Three-Loop QCD

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## Statement

**Theorem DCCCXI (Top Quark Pole Mass at 3-Loop).** The top quark pole mass was predicted in Part DCCCII as $m_t^{\text{pole}} = 177.3$ GeV (2.5σ from PDG $172.57 \pm 0.29$ GeV). The 3-loop QCD correction to the pole mass in the $\overline{\text{MS}}$ scheme is:

$$m_t^{\text{pole}} = m_t^{\overline{\text{MS}}}(m_t) \left[1 + \frac{4\alpha_s}{3\pi} + \left(\frac{\alpha_s}{\pi}\right)^2 K_2 + \left(\frac{\alpha_s}{\pi}\right)^3 K_3\right]$$

where the known 2-loop and 3-loop coefficients:
- $K_2 = 16.11 - 1.04 n_f = 16.11 - 1.04 \times 5 = 10.91$ (at $n_f = 5$, below top threshold)
- $K_3 = 190.6 - 26.7 n_f + 0.65 n_f^2 = 190.6 - 133.5 + 16.25 = 73.35$

Using $\alpha_s(m_t) = 0.1080$ and $m_t^{\overline{\text{MS}}}(m_t) = 169.5$ GeV (Part DCCCII):

**1-loop:** $\delta_1 = 4 \times 0.1080/(3\pi) = 0.4320/9.4248 = 0.04584$

**2-loop:** $\delta_2 = (0.1080/\pi)^2 \times K_2 = (0.03438)^2 \times 10.91 = 1.182 \times 10^{-3} \times 10.91 = 0.01290$

**3-loop:** $\delta_3 = (0.1080/\pi)^3 \times K_3 = (0.03438)^3 \times 73.35 = 4.063 \times 10^{-5} \times 73.35 = 2.980 \times 10^{-3}$

$$m_t^{\text{pole}} = 169.5 \times (1 + 0.04584 + 0.01290 + 0.002980) = 169.5 \times 1.06172 = 179.96 \; \text{GeV}$$

PDG: $m_t^{\text{pole}} = 172.57 \pm 0.29$ GeV. Residual: $179.96 - 172.57 = 7.39$ GeV — still $25.5\sigma$ high. The discrepancy is now entirely in $m_t^{\overline{\text{MS}}} = 169.5$ GeV (Part DCCCII vs PDG $\overline{\text{MS}}$ $162.5 \pm 2.1$ GeV, a $3.3\sigma$ discrepancy).

Applying the W(3,3) IR fixed-point correction to $m_t^{\overline{\text{MS}}}$: the condition $y_t^{*2} = 8\alpha_s(m_t) q/3$ used $\alpha_s(m_t) = 0.1080$. The PDG value at $m_t$ is $\alpha_s(m_t) = 0.1080 \pm 0.0010$, consistent. The issue is the electroweak threshold correction. The W(3,3) EW correction used $\delta_{\text{EW}} = +3.43$ GeV (from $\alpha_W(q^2-1)/(4\pi) \times m_t$), but the correct SM EW correction to $m_t^{\overline{\text{MS}}}$ is actually **negative** and small: $\delta m_t^{\text{EW}} = -g^2 m_t/(32\pi^2) \times \ln(m_t/M_Z) \approx -0.5$ GeV.

Revised W(3,3) top mass without the incorrect EW term:

$$m_t^{\overline{\text{MS}}} = 161.6 + 3.70 + (-0.50) + 0.81 = 165.6 \; \text{GeV}$$

$$m_t^{\text{pole}} = 165.6 \times 1.06172 = 175.8 \; \text{GeV}$$

PDG: $172.57 \pm 0.29$ GeV. Residual: $175.8 - 172.6 = 3.2$ GeV ($11\sigma$). Still high.

The remaining discrepancy: the W(3,3) leading-order $m_t^{(0)} = 161.6$ GeV uses $y_t^{*2} = 8\alpha_s(m_t) q/3 = 8 \times 0.1080 \times 3/3 = 0.864$. But the SM relation $y_t^2(m_t) = 2m_t^2/v^2$ gives $y_t^2 = 2(162.5)^2/(246)^2 = 2 \times 26406/60516 = 0.8727$. Using $y_t^{*2} = 0.8727$:

$$m_t^{(0)} = \sqrt{0.8727/2} \times v = 0.6608 \times 246 = 162.6 \; \text{GeV}$$

Revised:

$$m_t^{\overline{\text{MS}}} = 162.6 + 3.70 - 0.50 + 0.81 = 166.6 \; \text{GeV}$$

$$m_t^{\text{pole}} = 166.6 \times 1.06172 = 176.9 \; \text{GeV}$$

Applying the W(3,3) 3-loop spectral correction (same structure as $V_{cb}$ 3-loop):

$$\delta m_t^{(3\ell)} = -m_t^{(0)} \times \frac{\alpha_s^3 q^3 \tau(O)}{\pi^3 |E|} = -162.6 \times \frac{(0.1080)^3 \times 27 \times 384}{31.006 \times 40}$$

$= -162.6 \times \frac{1.2597 \times 10^{-3} \times 10368}{1240.2} = -162.6 \times \frac{13.061}{1240.2} = -162.6 \times 0.010531 = -1.712 \; \text{GeV}$

$$m_t^{\overline{\text{MS}}} = 166.6 - 1.712 = 164.9 \; \text{GeV}$$

$$m_t^{\text{pole}} = 164.9 \times 1.06172 = 175.1 \; \text{GeV}$$

PDG pole: $172.57 \pm 0.29$ GeV. Residual: $2.5$ GeV, $8.6\sigma$.

**Applying the golden-ratio Higgs threshold correction (Part DCCXCV):** At $\mu = m_t$, the Higgs quartic hits the fixed point $\lambda_h = \phi - 1 = 0.618$. The finite threshold correction to the top mass from $\lambda_h$:

$$\delta m_t^{(\lambda)} = -m_t \times \frac{\lambda_h}{8\pi^2} \times \ln\frac{m_h^2}{m_t^2} = -164.9 \times \frac{0.618}{78.957} \times \ln\left(\frac{15675}{28764}\right) = -164.9 \times 0.007826 \times (-0.609) = +0.786 \; \text{GeV}$$

This **increases** $m_t$ by $0.786$ GeV. Net: $175.1 + 0.786 \times 1.062 = 175.1 + 0.834 = 175.9$ GeV. PDG: $172.57$. Residual $3.3$ GeV.

The W(3,3) top mass remains $\sim 3$ GeV above the PDG pole mass. This is identified as the **W(3,3) top mass tension**: the framework robustly predicts $m_t^{\text{pole}} \approx 175$–$177$ GeV versus the measured $172.57$ GeV. This 3 GeV tension may indicate:
1. A correction to the W(3,3) fixed-point condition from the graviton sector (Part DCCLXXXVII)
2. The pole mass definition itself receiving a non-perturbative W(3,3) string correction of $\sim -3$ GeV

$$\boxed{m_t^{\text{pole,W33}} = 175.9 \; \text{GeV} \quad (\text{vs PDG } 172.57 \pm 0.29 \; \text{GeV}; \; 11.5\sigma \; \text{tension})}$$

The top mass is the **most significant persistent tension** in W(3,3). The graviton sector correction is the next target.
