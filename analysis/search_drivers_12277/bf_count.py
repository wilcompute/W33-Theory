"""12280: massless Bose-Fermi counting for SM_2496 and its torsion brother (component count = product of representation dimensions per
field; same convention for both, so differences are meaningful).  The leading one-loop vacuum energy of a Scherk-Schwarz-type vacuum at
large radius is proportional to n_F - n_B (massless level); this is a proxy, not the potential."""
import re, collections, json
KIND = {13: 'gauge', 14: 'gauge', 15: 'scalar', 16: 'scalar', 17: 'moduli', 18: 'moduli', 19: 'fermion', 20: 'fermion',
        21: 'tachyon', 22: 'tachyon', 23: 'excited tachyon', 24: 'excited tachyon', 8: 'gravity', 9: 'gravity'}
def count(p):
    c = collections.Counter()
    for l in open(p):
        m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) ', l)
        if m:
            d = 1
            for x in m.group(2).split(','):
                if x:
                    d *= abs(int(re.match(r'-?\d+', x).group(0)))
            c[KIND.get(int(m.group(1)), m.group(1))] += d
    return c
if __name__ == '__main__':
    out = {}
    for tag, f in (('original', 'b2496/c000.nsoq'), ('brother', 'b2496/c576.nsoq')):
        c = count(f)
        bos = c['gauge'] + c['scalar'] + c['moduli'] + c['gravity']
        out[tag] = dict(components=dict(c), n_B=bos, n_F=c['fermion'], nF_minus_nB=c['fermion'] - bos)
        print(tag, dict(c), 'n_F - n_B =', c['fermion'] - bos)
    json.dump(out, open('bf_count.json', 'w'), indent=1)
