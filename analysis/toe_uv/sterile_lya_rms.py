"""Item 4: does the shape of the decay-production momentum distribution move the Lyman-alpha edge?
Freeze-in from decays of a heavy scalar in equilibrium: f(q) ~ q^(-1/2) e^(-q) (non-relativistic-decay freeze-in shape, from memory; q = p/T), so <q> = Gamma(3.5)/Gamma(2.5) = 2.5, <q^2> = Gamma(4.5)/Gamma(2.5) = 8.75.
Thermal Fermi-Dirac: <q> = 3.151, <q^2> = 15 zeta(5)/zeta(3) = 12.94.
Match either the mean momentum (as in sterile_lya.py) or the rms velocity (closer to the free-streaming length); compare M_min.
usage: py -3 sterile_lya_rms.py"""
import json
import math
from scipy.special import zeta

dil = (3.91 / 106.75) ** (1 / 3) * (11 / 4) ** (1 / 3)
dec_mean, dec_rms = 2.5, math.sqrt(8.75)
fd_mean, fd_rms = 7 * math.pi ** 4 / (180 * zeta(3)), math.sqrt(15 * zeta(5) / zeta(3))
out = {}
for mth in (5.3, 5.7):
    tx = (94.0 * 0.12 / (mth * 1e3)) ** (1 / 3)
    m_mean = mth * dec_mean * dil / (fd_mean * tx)
    m_rms = mth * dec_rms * dil / (fd_rms * tx)
    out[str(mth)] = dict(M_min_mean=m_mean, M_min_rms=m_rms, shift_percent=(m_rms / m_mean - 1) * 100)
    print("m_th %.1f keV: M_min mean-match %.2f keV, rms-match %.2f keV (%+.1f%%)" % (mth, m_mean, m_rms, (m_rms / m_mean - 1) * 100))
json.dump(out, open("sterile_lya_rms.json", "w"), indent=1)
