"""weight-level multisets (m, n, mm, weight) and the subset relation Wilson-line-on <= Wilson-line-off; the complement are the 6D
massless states whose fixed-torus momentum is shifted by the Wilson line."""
import collections, sys
def wl(p):
    c = collections.Counter(); cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            t = l.split(); cur = (int(t[2][2:]), int(t[5][2:]), int(t[4][3:]))
        elif l.startswith('W ') and cur is not None:
            c[cur + (tuple(round(float(x), 6) + 0.0 for x in l[2:].split(',')),)] += 1
    return c
if __name__ == '__main__':
    on, off = wl(sys.argv[1]), wl(sys.argv[2])
    print(sys.argv[1], sum(on.values()), sys.argv[2], sum(off.values()), 'on - off (must be 0):', sum((on - off).values()), 'shifted:', sum((off - on).values()))
