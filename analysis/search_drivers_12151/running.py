"""12154: one-loop SM gauge running with string boundary conditions k_3 = k_2 = 1, k_Y (unnormalised U(1)_Y) at M_s.
(a) solve alpha_U, M_s from alpha_em(M_Z), alpha_s(M_Z) -> predict sin^2 theta_W(M_Z); (b) fix M_s = g_U * 5.27e17 GeV
(Kaplunovsky) with alpha_U from alpha_s -> predict sin^2; (c) the k_Y that would reproduce the measured sin^2 in (a)."""
import json, math
MZ, aem, a3, s2_exp = 91.1876, 1 / 127.951, 0.1180, 0.23122
bY, b2, b3 = 41 / 6, -19 / 6, -7.0
out = {}
for kY in (5 / 3, 17 / 3, 29 / 3):
    # 1/aem = (1+kY)/aU + (b2+bY) L/2pi ; 1/a3 = 1/aU + b3 L/2pi
    A = [[1 + kY, (b2 + bY) / (2 * math.pi)], [1.0, b3 / (2 * math.pi)]]
    rhs = [1 / aem, 1 / a3]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    iaU = (rhs[0] * A[1][1] - A[0][1] * rhs[1]) / det
    L = (A[0][0] * rhs[1] - A[1][0] * rhs[0]) / det
    ia2 = iaU + b2 * L / (2 * math.pi)
    sa = aem * ia2
    Ms = MZ * math.exp(L)
    # (b) Kaplunovsky
    def fixed(kY):
        # iterate: aU from alpha_s with L(Ms), Ms = sqrt(4 pi aU) * 5.27e17
        Msb = 5e17
        for _ in range(100):
            Lb = math.log(Msb / MZ)
            iaUb = 1 / a3 - b3 * Lb / (2 * math.pi)
            Msb = math.sqrt(4 * math.pi / iaUb) * 5.27e17
        ia2b = iaUb + b2 * Lb / (2 * math.pi)
        iaYb = kY * iaUb + bY * Lb / (2 * math.pi)
        return dict(Ms=Msb, alphaU=1 / iaUb, sin2=(1 / ia2b) / (1 / ia2b + 1 / iaYb) if False else iaYb ** -1 / (ia2b ** -1 + iaYb ** -1),
                    alpha_em_inv=ia2b + iaYb)
    out['%.4f' % kY] = dict(kY=kY, sin2_at_Ms=1 / (1 + kY), a_solve_from_aem_as=dict(Ms_GeV=Ms, alphaU=1 / iaU, sin2_MZ=sa),
                           b_kaplunovsky=fixed(kY))
    print(out['%.4f' % kY])
# (c) kY reproducing measured sin2 and alpha_em with alpha_s: from (a) system with three equations -> kY
ia2m = s2_exp / aem; iaYm = (1 - s2_exp) / aem
L = (ia2m - 1 / a3) * 2 * math.pi / (b2 - b3); iaU = 1 / a3 - b3 * L / (2 * math.pi)
kY_needed = (iaYm - bY * L / (2 * math.pi)) / iaU
out['kY_needed_for_measured'] = dict(kY=kY_needed, Ms_GeV=MZ * math.exp(L), alphaU=1 / iaU)
print(out['kY_needed_for_measured'])
json.dump(out, open('running.json', 'w'), indent=1)
