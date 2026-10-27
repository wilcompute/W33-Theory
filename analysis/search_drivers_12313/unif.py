"""12313: one-loop SM running from M_Z (alpha_em^-1 = 127.95, sin^2 theta_W = 0.2312, alpha_s = 0.1180; b_Y = 41/6, b_2 = -19/6,
b_3 = -7 for unnormalised Y).  The scale where alpha_2 = alpha_3, the k_Y that k_Y alpha_Y = alpha_2 requires there, and the same at the
weakly coupled heterotic string scale M_s ~ 5e17 GeV (Kaplunovsky; alpha_2 vs alpha_3 mismatch also reported).  SM running only: the
candidate's extra light states are not included (they would change b_i)."""
import math, json
MZ = 91.1876
ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
aY = 1 / ainv_em / (1 - s2); a2 = 1 / ainv_em / s2; a3 = as_
b = dict(Y=41 / 6, two=-19 / 6, three=-7)
inv = lambda a0, bb, mu: 1 / a0 - bb / (2 * math.pi) * math.log(mu / MZ)
# alpha_2 = alpha_3 crossing
t = (1 / a2 - 1 / a3) / ((b['two'] - b['three']) / (2 * math.pi))
M23 = MZ * math.exp(t)
k_needed = inv(aY, b['Y'], M23) / inv(a2, b['two'], M23)          # k alpha_Y = alpha_2  <=>  k = (1/alpha_Y)/(1/alpha_2)
Ms = 5e17
k_at_Ms = inv(aY, b['Y'], Ms) / inv(a2, b['two'], Ms)
mismatch_23_Ms = inv(a2, b['two'], Ms) - inv(a3, b['three'], Ms)
sin2_string = lambda k: 1 / (1 + k)
out = dict(M23=M23, k_needed_at_M23=k_needed, k_needed_at_Ms=k_at_Ms, alpha2inv_minus_alpha3inv_at_Ms=mismatch_23_Ms,
           sin2_string_kY_8_3=sin2_string(8 / 3), sin2_string_kY_5_3=sin2_string(5 / 3))
print(json.dumps(out, indent=1)); json.dump(out, open('unif.json', 'w'), indent=1)
