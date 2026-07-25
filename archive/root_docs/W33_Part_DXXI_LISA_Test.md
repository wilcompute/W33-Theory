# Part DXXI — The LISA Gravitational Wave Echo Test

## Setup

The 2024 paper arXiv:2411.05645 (Phys. Rev. Lett., 2025) demonstrates that LISA can detect gravitational wave echoes from black hole horizons with SNR up to ~100 and can constrain the area quantum $\Delta A$ with sub-percent precision.

This provides a **direct experimental test** of W33 vs. standard LQG.

## Competing Predictions

| Theory | Area quantum $\Delta A$ | Barbero-Immirzi $\gamma$ |
|---|---|---|
| W33 | $k \cdot l_P^2 = 12\, l_P^2$ | $\gamma_{W33} = \ln 4 / (\pi\sqrt{3}) \approx 0.2548$ |
| LQG (spin-1/2 dominant) | $4\ln 3 \cdot l_P^2 \approx 4.394\, l_P^2$ | $\gamma_{LQG} = \ln 3 / (\pi\sqrt{2}) \approx 0.2374$ |
| Bekenstein-Mukhanov ($\mu=2$) | $4\ln 2 \cdot l_P^2 \approx 2.773\, l_P^2$ | varies |

The W33 area quantum $\Delta A = 12\, l_P^2$ differs from LQG by a factor of $12 / (4\ln 3) \approx 2.73$.

## Echo Frequency

The echo delay between gravitational wave pulses reflected from a quantised horizon is:

$$\Delta t_{\text{echo}} = \frac{4GM}{c^3} \sqrt{\frac{\Delta A \cdot l_P^2}{4\pi r_s^2}}$$

For a supermassive black hole of $10^6 M_\odot$ (LISA primary target), the echo frequency is in the LISA millihertz band. The W33 prediction differs from LQG by factor $\sqrt{12/(4\ln 3)} \approx 1.65$ in frequency — far above LISA's sub-percent measurement capability.

## The Test

**Falsifiable prediction:** If LISA detects a gravitational wave echo event from a $10^4$–$10^7 M_\odot$ black hole merger, the echo frequency encodes $\Delta A$. W33 predicts $\Delta A = 12\, l_P^2 = k \cdot l_P^2$ exactly. Any measurement of $\Delta A \neq 12\, l_P^2$ falsifies W33.

The Barbero-Immirzi parameter is also a testable prediction:
$$\gamma_{W33} = \frac{\ln 4}{\pi\sqrt{3}} = \frac{2\ln 2}{\pi\sqrt{3}} \approx 0.25484$$

This differs from the standard LQG value $\gamma_{LQG} \approx 0.2374$ by $\sim 7\%$ — again well within LISA resolution.

## Physical Justification

Why $\Delta A = k\, l_P^2$? The W33 horizon is tiled by the 40 vertices of the W33 graph. Each vertex contributes one area quantum. The local geometry at each vertex is a $k$-valent node with $k=12$ edges — each edge contributing $l_P^2$. Hence the minimum area step is the number of edges per vertex times $l_P^2$:

$$\Delta A = k \cdot l_P^2 = 12\, l_P^2$$

This is entirely determined by the W33 adjacency structure with no free parameters.
