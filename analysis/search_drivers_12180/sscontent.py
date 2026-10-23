"""12180b: chiral content of the Scherk-Schwarz interpolation at large radius, from the non-free model's Witten-untwisted
(m=0) dump.  Even Z6 sectors: left fermions (code 19) = parent multiplets with chi = -1, kept as fermions.  Odd sectors: the
translation pairs fixed points, keeping half of every parent multiplet (codes 19 + 15).  Net count of a rep R = #R - #conj R
(first-factor colour triplet and doublet).  Control: the parent (19 + 15 over all m=0 sectors) must have net 3 (3,2)."""
import re, subprocess, sys, json
from collections import defaultdict


def dump(path):
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          f'timeout 1800 ./nsodump {path}')
    return subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout


def content(o):
    net = defaultdict(lambda: defaultdict(float))
    for mm in re.finditer(r'^F m=(\d+) k=\S+ m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
        code, w, n, dims, k = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), mm.group(4).split(','), int(mm.group(5))
        if w != 0 or code not in (15, 19):
            continue
        rest = 1
        for e in dims[2:]:
            rest *= abs(int(re.match(r'-?\d+', e).group(0)))
        rep = (dims[0], dims[1])
        sign = {('3', '2'): 1, ('-3', '2'): -1}.get(rep)
        tag = 'Q'
        if sign is None:
            sign = {('-3', '1'): 1, ('3', '1'): -1}.get(rep); tag = 'qbar'
        if sign is None:
            sign = {('1', '2'): 1}.get(rep); tag = 'L'
        if sign is None:
            continue
        parity = 'even' if n % 2 == 0 else 'odd'
        net[tag][(code, parity)] += sign * k * rest
    out = {}
    for tag, d in net.items():
        parent = sum(d.values())
        ss = d.get((19, 'even'), 0) + 0.5 * (d.get((19, 'odd'), 0) + d.get((15, 'odd'), 0))
        out[tag] = dict(parent_net=parent, ss_large_R_net_fermions=ss, detail={f'{c}_{p}': v for (c, p), v in d.items()})
    return out


if __name__ == '__main__':
    res = {}
    for v in sys.argv[1:]:
        o = dump(f'~/orb/p1109x/ssz6ii/Z6II_59_SM_20260917_1105_v{v}.txt')
        g = re.search(r'GAUGE (.*)', o).group(1)
        res[v] = dict(gauge=g, content=content(o))
        print(v, g, json.dumps(res[v]['content']))
    json.dump(res, open('sscontent.json', 'w'), indent=1)
