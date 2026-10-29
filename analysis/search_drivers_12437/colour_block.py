"""12437: where does the colour charge-lattice obstruction (12432) sit?  For each of the 23 radius-safe, exotic-free new-parent candidates
and its SU(3) x SU(2) pairing: hypercharge feasibility (12364 MILP, loose values) with ONLY the chirality constraints of
  (Q)  quark doublets;  (Q+U)  doublets + |Y| = 2/3 triplets;  (Q+D)  doublets + |Y| = 1/3 triplets;  (Q+U+D) all colour.
Reports the counts; a type whose addition kills feasibility is the obstruction's location."""
import json, os, subprocess, sys, collections
vp = json.load(open('../search_drivers_12373/vet_pairs2.json'))
COND = {
    'Q': "abs(key[0][I3])==3 and abs(key[0][I2])==2",
    'Q+U': "abs(key[0][I3])==3 and (abs(key[0][I2])==2 or abs(key[1])==sp.Rational(2,3))",
    'Q+D': "abs(key[0][I3])==3 and (abs(key[0][I2])==2 or abs(key[1])==sp.Rational(1,3))",
    'Q+U+D': "abs(key[0][I3])==3",
}
out = {}; tab = collections.Counter()
for b, prs in vp.items():
    for x in prs:
        rec = {}
        for name, cond in COND.items():
            env = dict(os.environ, YS_NSOQ=f'../search_drivers_12373/spec/{b}.nsoq', ONLY=cond, LOOSE='1', NO_ANOM='1')
            subprocess.run([sys.executable, 'ysearch.py', b, str(x['su3']), str(x['su2']), '1'], cwd='../search_drivers_12364', env=env,
                           capture_output=True, text=True, timeout=3000)
            rec[name] = len(json.load(open(f'../search_drivers_12364/ysearch_{b}_noanom_loose_only.json'))['solutions']) > 0
        out[b] = rec; tab[tuple(rec[k] for k in COND)] += 1
        print(b, rec, flush=True)
json.dump(dict(per_model=out, table={str(k): v for k, v in tab.items()}, order=list(COND)), open('colour_block.json', 'w'), indent=1)
print('(Q, Q+U, Q+D, Q+U+D) feasible:', dict(tab))
