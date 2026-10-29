"""compare two nsoq spectra as multisets of (m, sector n, Witten mm, dims, sorted weight set) -- fixed-point labels may differ."""
import re, sys, collections
def states(p):
    out, cur = [], None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=\S+ dim=(\S*)', l)
            cur = [m.group(1), m.group(2), m.group(3), m.group(4), []]; out.append(cur)
        elif l.startswith('W ') and cur is not None:
            cur[4].append(tuple(round(float(x), 6) for x in l[2:].split(',')))
    return collections.Counter((a, b, c, d, tuple(sorted(w))) for a, b, c, d, w in out)
if __name__ == '__main__':
    A, B = states(sys.argv[1]), states(sys.argv[2])
    print('states', sum(A.values()), sum(B.values()), 'identical multiset:', A == B, 'diff', sum((A - B).values()), sum((B - A).values()))
