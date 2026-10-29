"""12372b: 'energy = update rate, mass = internal rotation, c = maximal update propagation' -- checked on the 1D Dirac quantum cellular
automaton of Bisio, D'Ariano, Tosini (arXiv:1212.2839; D'Ariano-Perinotti arXiv:1306.1934), cited in-corpus (toe54).  One step:
psi_L(x) <- n psi_L(x+1) - i m psi_R(x),  psi_R(x) <- n psi_R(x-1) - i m psi_L(x),  n^2 + m^2 = 1.  Checks (numerical, exact cone):
(1) strict light cone: from a point source, amplitude is exactly 0 outside |x| <= t;  (2) dispersion cos w = n cos k;
(3) rest frequency w(0) = arcsin m (mass = chirality-mixing angle per step);  (4) group velocity <= n < 1 for m > 0, = 1 for m = 0;
(5) small k: w^2 = m^2 + n^2 k^2 + O(k^4, m^4)  (E^2 = (mc^2)^2 + (pc)^2 with c_eff = n)."""
import json
import numpy as np
N = 401; out = {}
def step(L, R, n, m):
    return n * np.roll(L, -1) - 1j * m * R, n * np.roll(R, 1) - 1j * m * L
for m in (0.0, 0.1, 0.3, 0.6):
    n = np.sqrt(1 - m * m)
    L = np.zeros(N, complex); R = np.zeros(N, complex); L[N // 2] = 1
    T = 150
    for _ in range(T): L, R = step(L, R, n, m)
    x = np.arange(N) - N // 2
    outside = np.abs(L[np.abs(x) > T]).max() + np.abs(R[np.abs(x) > T]).max()
    # dispersion from the 2x2 symbol U(k) = [[n e^{ik}, -im], [-im, n e^{-ik}]]
    ks = np.linspace(-np.pi, np.pi, 2001); ws = []
    for k in ks:
        U = np.array([[n * np.exp(1j * k), -1j * m], [-1j * m, n * np.exp(-1j * k)]])
        ws.append(np.abs(np.angle(np.linalg.eigvals(U))).min())
    ws = np.array(ws)
    disp_err = np.abs(np.cos(ws) - n * np.cos(ks)).max()
    vg = np.abs(np.gradient(ws, ks)); vmax = vg[np.isfinite(vg)].max()
    small = np.abs(ks) < 0.05; rel = np.abs(ws[small] ** 2 - (m * m + n * n * ks[small] ** 2)).max()
    out[str(m)] = dict(outside_cone=float(outside), dispersion_err=float(disp_err), w0=float(ws[np.argmin(np.abs(ks))]), arcsin_m=float(np.arcsin(m)),
                       vmax=float(vmax), n=float(n), small_k_rel_err=float(rel))
    print(m, out[str(m)])
json.dump(out, open('qca.json', 'w'), indent=1)
