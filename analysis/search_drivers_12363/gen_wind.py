"""12363: winding sectors along e5 of the theta^2-fixed torus.  A winding-w string of the sub-orbifold Witten x theta^2 is the space-group
element (g, l + w e5); its local shift gains w W5 and its centralizer phases gain the matching terms, so feeding the engine constructing
elements shifted by w e5 yields the states that are light as R5 -> 0 (zero effective momentum, internal levels matched).  Tachyons in
that run = small-R5 tachyons, alpha' m^2/4 = l + w^2 R5^2/4.  Control: with W5 = 0 winding must change nothing."""
import sys, numpy as np
sys.path.insert(0, '../search_drivers_12359')
import gen_geom as G
def build_off(s, head, off):
    N = 6 // s; off = np.array(off)
    sectors, cent = [], []
    import itertools
    for a in (0, 1):
        for j in range(N):
            k = (s * j) % 6
            per = [G.plane_reps(p, k)[0] for p in range(3)]
            reps = []
            for combo in itertools.product(*per):
                l = np.array([x for v in combo for x in v])
                if not any(G.equiv(G.rot(l, s * i), r, k) for r in reps for i in range(N)):
                    reps.append(l)
            reps = [l + off for l in reps]
            sectors.append([G.row(a, j, l) for l in reps])
            for l in reps:
                gens = []
                if k == 0:
                    gens += [G.row(0, 0, np.eye(6, dtype=int)[t]) for t in range(6)]
                    for i in range(1, N):
                        m = G.solve_m(l, 0, s * i) if False else ([0] * 6 if not (l - G.rot(l, s * i)).any() else None)
                        if m is not None: gens.append(G.row(0, i, m))
                else:
                    for p in range(3):
                        if not (np.eye(2, dtype=int) - G.mp(G.P[p], k)).any():
                            for t in (0, 1):
                                e = np.zeros(6, dtype=int); e[2 * p + t] = 1; gens.append(G.row(0, 0, e))
                    for i in range(1, N):
                        m = G.solve_m(l, k, s * i)
                        if m is not None: gens.append(G.row(0, i, m))
                gens.append(G.row(1, 0, np.zeros(6)))
                cent.append((G.row(a, j, l), gens))
    from fractions import Fraction as F
    tw = ' '.join(str(F(s, 6) * c) if F(s, 6) * c != 0 else '0' for c in (1, 2, -3))
    out = head.replace('@N@', str(N)).replace('@TWIST@', '0/1 ' + tw)
    out += 'begin constructing elements\n' + ''.join('new sector\n' + ''.join(r + '\n' for r in sec) for sec in sectors) + 'end constructing elements\n\n'
    out += 'begin centralizer elements\n' + ''.join(f'// Const elem: {c} \nbegin data\n' + ''.join(g + '\n' for g in gs) + 'end data\n\n' for c, gs in cent)
    return out + 'end centralizer elements\n'
if __name__ == '__main__':
    src = open('../search_drivers_12359/parent_geom.txt').read()
    head = src.split('begin constructing elements')[0]
    head = head.replace('point group\n2\n6\n1', 'point group\n2\n@N@\n1').replace(' 0/1 1/6 1/3 -1/2', ' @TWIST@')
    head = head.replace('allowed order of Wilson lines\n1\n1\n3\n3\n2\n2', 'allowed order of Wilson lines\n3\n3\n3\n3\n2\n2').replace('begin identical WLs\n 3 4', 'begin identical WLs\n 1 2\n 3 4')
    for w in (0, 1, 2, 3):
        open(f'Geometry_Z6-II_sub2w{w}.txt', 'w', newline='\n').write(build_off(2, head, [0, 0, 0, 0, w, 0]))
    print('ok')
