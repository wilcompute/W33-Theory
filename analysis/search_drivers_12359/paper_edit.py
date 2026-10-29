B = chr(92)
p = 'papers/forty_points/sec07_realforms.tex'
s = open(p, encoding='utf-8').read()
old = ("They are tachyon-free at the orbifold point and, by exact level minima of the winding cosets, for radii above about "
       "$" + B + "sqrt{2" + B + "alpha'}$.")
assert old in s, 'sentence'
new = ("They have no tachyon at the orbifold point, but they are not tachyon-free at large radius: the 6D theory of the $" + B + "theta^2$-fixed "
       "torus has $12$ (SM" + B + "_2913) or $24$ (SM" + B + "_2618) tachyons with $m_R^2=-1/6$, which the order-2 Wilson line on $e_5$ moves to "
       "half-integer $e_5$ momentum, so they return for $R_5>" + B + "sqrt{3" + B + "alpha'/8}$ (the same holds for $52$ of the $99$ tachyon-free "
       "parents; the $" + B + "theta^3$-fixed torus is clean in all $99$). An earlier statement that radii above $" + B + "sqrt{2" + B + "alpha'}$ "
       "are safe is withdrawn.")
s = s.replace(old, new, 1)
old2 = ("the Yukawa hierarchy, proton operators, the vacuum and moduli. " + B + "cert{w33" + B + "_pass12351" + B + "_to" + B + "_12356" + B
        + "_tachyon" + B + "_free" + B + "_z6ii" + B + "_standard" + B + "_models.py}")
assert old2 in s, 'open'
add = (" These were then tested with sub-orbifold geometries generated from the space group. The regenerated $" + B + "mathbb Z_6$-II geometry "
       "reproduces the spectrum state for state, and the sub-orbifolds' fermions are vector-like, as a 6D origin requires. Six SM-singlet "
       "scalars suffice to give mass to every vector-like and fractional-charge fermion (each is necessary; $1$ of $100$ random sets of six "
       "works). They leave a gauged, anomaly-free $U(1)_{B-L}$ unbroken, which any of $14$ singlets with $B-L=" + B + "pm2$ breaks to matter "
       "parity. Baryon number is not gauged: four-fermion $" + B + "Delta B=" + B + "Delta L=1$ operators appear at singlet degree $0$--$2$ "
       "(harmless at $M_s" + B + "sim10^{17}$" + B + ",GeV), and one of $16$ colour-triplet scalars couples to both quark pairs and quark--lepton "
       "pairs, so it must be heavy. All ten Higgs choices give three nonzero light masses per sector, but with a common singlet ratio the "
       "hierarchy is too mild (charm about $1.8$ decades too heavy). Large-volume thresholds do not rescue $k_Y=5/3$: the $e_5e_6$ torus's "
       "6D coefficients are exactly universal, $b=16" + B + ",(5/3,1,1)$, and those of $e_3e_4$ have the wrong pattern. The Casimir energy of "
       "$e_3e_4$ is positive ($N_B-N_F=-752/9$ effective), so the torus decompactifies unless the 6D vacuum energy is positive. These "
       "couplings are upper bounds: the vertex rule of Pass~11097 is not imposed. " + B + "cert{w33" + B + "_pass12357" + B + "_to" + B + "_12362"
       + B + "_sub" + B + "_orbifolds" + B + "_thresholds" + B + "_vacuum" + B + "_proton.py}")
s = s.replace(old2, old2 + add, 1)
open(p, 'w', encoding='utf-8').write(s)
q = 'papers/forty_points/appA_ledger.tex'
t = open(q, encoding='utf-8').read()
o3 = "radii $" + B + "gtrsim" + B + "sqrt{2" + B + "alpha'}$; unification needs $k_Y" + B + "le1.28$"
assert o3 in t, 'ledger'
t = t.replace(o3, "tachyon-free only at the orbifold point (large-$R_5$ tachyons, 12359); unification needs $k_Y" + B + "le1.28$", 1)
row = t.split('\n')
i = next(k for k, l in enumerate(row) if l.startswith('12351--12356'))
row.insert(i + 1, "12357--12362: sub-orbifold geometries (parent regenerated 788/788, vector-like 6D fermions); large-$R_5$ tachyons in 52/99 "
           "parents incl." + B + " all 3-gen models; $b(e_5e_6)=16(5/3,1,1)$ universal, no threshold fit; Casimir $N_{" + B + "rm eff}=-752/9$; "
           "6-singlet lifting set; gauged anomaly-free $B-L$ & " + B + "tierC & " + B + "cert{w33" + B + "_pass12357" + B + "_to" + B + "_12362"
           + B + "_sub" + B + "_orbifolds" + B + "_thresholds" + B + "_vacuum" + B + "_proton.py}" + B + B)
open(q, 'w', encoding='utf-8').write('\n'.join(row))
print('ok')
