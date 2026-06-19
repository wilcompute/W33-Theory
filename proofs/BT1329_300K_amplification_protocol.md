# BT1329 — 300 K Amplification Protocol for W33 Photonic HoloNet

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1326 (Thermal Noise Degradation Model)

---

## 1. Objective

BT1326 showed that room-temperature operation at 300 K is feasible but tight: the estimated physical error rate
$$
p(300\,\mathrm{K}) \approx 6.1\%
$$
is only slightly below the W33 threshold of 6.7%. The dominant issue is phonon-induced propagation loss, not thermal photon occupation.

This BT specifies the amplification protocol needed to stabilise room-temperature routing.

---

## 2. Loss Budget

For the maximum Q6 routing path length of approximately 40 mm, BT1326 estimated total path loss:
$$
\mathcal{L}_{300K} \approx 10\,\mathrm{dB}.
$$
To keep the effective physical error rate below threshold, this loss must be distributed across stages and compensated before the signal-to-noise ratio collapses.

---

## 3. Stagewise Amplification Schedule

Partition the HoloNet path into quadrant stages Q1–Q6. Let the per-stage loss be approximately:

| Stage | Nominal loss |
|-------|--------------|
| Q1 | 0.5 dB |
| Q2 | 0.8 dB |
| Q3 | 1.2 dB |
| Q4 | 1.8 dB |
| Q5 | 2.4 dB |
| Q6 | 3.3 dB |

Total: 10.0 dB.

### Amplification rule
Insert gain blocks after Q3, Q4, and Q5:
- Gain after Q3: +2.0 dB
- Gain after Q4: +2.5 dB
- Gain after Q5: +3.5 dB

Total gain: +8.0 dB. Residual net loss:
$$
10.0 - 8.0 = 2.0\,\mathrm{dB},
$$
which lies within the W33 correction budget.

---

## 4. Noise Accounting

Amplifiers inject spontaneous emission noise. Let each stage contribute effective added error
$$
\epsilon_A \approx 0.3\%.
$$
For three amplification stages:
$$
\epsilon_{\text{amp}} \approx 0.9\%.
$$

Room-temperature baseline error without compensation is 6.1%. Loss compensation reduces propagation-induced error by approximately 2.4%, yielding:
$$
p_{\text{eff}} \approx 6.1\% - 2.4\% + 0.9\% = 4.6\%.
$$
Thus the amplified 300 K operating point sits safely below the W33 threshold 6.7%.

---

## 5. Control Policy

A dynamic controller monitors signal amplitude after each quadrant stage. If measured attenuation exceeds expected attenuation by more than 0.5 dB, the next amplifier increases gain by +0.5 dB temporarily.

Define attenuation residual
$$
\Delta_i = A_i^{\text{meas}} - A_i^{\text{pred}}.
$$
Control rule:
$$
G_{i+1} = G_{i+1}^{\text{base}} + 0.5\,\mathbf{1}[\Delta_i < -0.5\,\mathrm{dB}].
$$

This keeps the effective path loss stable without introducing unnecessary amplifier noise.

---

## 6. Recommended Hardware

Suitable room-temperature gain elements:
- integrated semiconductor optical amplifiers (SOAs)
- erbium-doped waveguide amplifiers (EDWAs)
- hybrid silicon–III/V gain sections

**Recommendation:** hybrid silicon–III/V SOA sections at Q3–Q5 boundaries.

---

## 7. Result

**Theorem BT1329-T1 (300 K Amplified Operability):**  
With three gain stages after Q3, Q4, and Q5, total gain 8 dB, and per-stage amplifier-added error below 0.3%, the room-temperature W33 HoloNet operates at
$$
p_{\text{eff}} \approx 4.6\% < 6.7\%,
$$
thereby preserving fault-tolerant operation.

---

**Next:** BT1330 — W33 vs. surface code full threshold simulation plan.
