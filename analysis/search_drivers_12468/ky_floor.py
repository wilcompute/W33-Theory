"""12468: a spectrum-only lower bound on k_Y.  Y = t . P with t in the U(1) subspace U (orthogonal to every non-abelian root) and
k_Y = 2 |t|^2 (normalisation of 12364: Q_L has Y = 1/6).  Three generations need a massless left-handed fermion that is an SU(3) x SU(2)
singlet with |Y| = 1 (e^c or its conjugate).  For that weight P, 1 = |t . P| = |t . P_U| <= |t| |P_U|, so
        k_Y >= 2 / |P_U|^2          and, minimised over the candidate e^c fields,   k_Y >= 2 / max_f |P_U(f)|^2.
Hidden-sector charged singlets of SU(3) x SU(2) are allowed as e^c only if the hidden rep is trivial (the SM e^c is a full singlet).
Controls: the bound must not exceed any k_Y that a model actually realises (c22: 11/3; SM_2913: 5/3)."""
import sys, os, re, json, glob
import sympy as sp

D = os.path.dirname(os.path.abspath(__file__))


def floor_for(path, I3, I2):
    roots = []; fields = []; cur = None
    for l in open(path, errors='ignore'):
        if l.startswith('FACTOR'):
            roots += [[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
        elif l.startswith('FIELD'):
            mm = re.match(r'FIELD (\d+) m=(\S+) .*?dim=(\S*)', l)
            cur = dict(m=int(mm.group(2)), d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(3).split(',')) if mm.group(3) else (), P=None)
            fields.append(cur)
        elif l.startswith('W ') and cur is not None and cur['P'] is None:
            cur['P'] = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
    R = sp.Matrix(roots)                                  # rows = roots
    Pr = R.T * (R * R.T).pinv() * R                       # projector onto the root span
    best = sp.Integer(0)
    for f in fields:
        if f['m'] != 19 or f['P'] is None or not f['d'] or any(abs(x) != 1 for x in f['d']):
            continue                                      # full singlets only (SM and hidden)
        PU = f['P'] - Pr * f['P']
        best = max(best, (PU.T * PU)[0])
    return (2 / best) if best else None


if __name__ == '__main__':
    out = {}
    F3 = {json.loads(l)['base']: json.loads(l) for f in glob.glob(os.path.join(D, '..', 'search_drivers_12373', 'filt3_*.jsonl')) for l in open(f)}
    vm = json.load(open(os.path.join(D, '..', 'search_drivers_12373', 'vet_maj.json')))
    for b in sorted(vm):
        su3, su2 = F3[b]['su3su2']
        fl = floor_for(os.path.join(D, '..', 'search_drivers_12373', 'spec', f'{b}.nsoq'), su3, su2)
        out[b] = dict(kY_floor=str(fl), kY_floor_float=float(fl), kY_realised=vm[b]['kY'])
        print(b, out[b], flush=True)
    for ctrl, path in (('SM_2913_v6', os.path.join(D, '..', 'search_drivers_12359', 'm2913v6_parent.nsoq')),):
        if os.path.exists(path):
            fl = floor_for(path, None, None); out['control_' + ctrl] = dict(kY_floor=str(fl), kY_floor_float=float(fl), kY_realised='5/3')
            print('control', ctrl, out['control_' + ctrl])
    json.dump(out, open(os.path.join(D, 'ky_floor.json'), 'w'), indent=1)
    fam = [v['kY_floor_float'] for k, v in out.items() if not k.startswith('control')]
    print('SM_2541 family k_Y floor range:', min(fam), max(fam))
