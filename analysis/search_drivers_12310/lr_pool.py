"""12310: the left-right hypercharge scan (12294's analyse) over every model pair of the 12281 and 12302 censuses, one task per
model file, 6 workers, 120 s limit per task (timeouts recorded, not dropped), progress logged."""
import json, os, sys, itertools, time, collections
from multiprocessing import Pool, TimeoutError
sys.path.insert(0, '../search_drivers_12294')
def task(args):
    import lr_census as L
    p = args
    if not os.path.exists(p) or not open(p, errors='ignore').read().rstrip().endswith('END'):
        return p, 'missing', []
    r = L.load(p)
    if r is None:
        return p, 'missing', []
    fac, fs = r
    i3 = [i for i, f in enumerate(fac) if f == 'A2']; i2 = [i for i, f in enumerate(fac) if f == 'A1']
    res = []
    for a in i3:
        for iL, iR in itertools.permutations(i2, 2):
            rr = L.analyse(fac, fs, a, iL, iR)
            if rr:
                res.append(dict(SU3=a, SU2L=iL, SU2R=iR, **rr))
    return p, 'ok', res
if __name__ == '__main__':
    jobs = []
    for D in ('../search_drivers_12281', '../search_drivers_12302'):
        for e in json.load(open(D + '/census_index.json')):
            for tag in ('w6odd', 'ctrl'):
                if tag in e['files']:
                    jobs.append(D + '/' + e['files'][tag][:-4] + '.nsoq')
    log = open('lr_pool.log', 'w', buffering=1)
    out = {}
    with Pool(6) as pool:
        asyncs = [(j, pool.apply_async(task, (j,))) for j in jobs]
        for n, (j, a) in enumerate(asyncs):
            try:
                p, status, res = a.get(timeout=120)
            except TimeoutError:
                p, status, res = j, 'timeout', []
            out[os.path.basename(p)] = dict(status=status, results=res)
            if n % 100 == 0:
                log.write(f'{n}/{len(jobs)} {time.strftime("%H:%M:%S")}\n')
        pool.terminate()
    tab = collections.Counter()
    for k, v in out.items():
        tag = 'w6odd' if '__w6odd' in k else 'ctrl'
        hit = any(x.get('sm_values') for x in v['results'])
        tab[(tag, v['status'], 'LR-type' if v['results'] else 'no SU3xSU2xSU2', 'three generations' if hit else '-')] += 1
    json.dump(dict(table={str(k): v for k, v in tab.items()}, results=out), open('lr_pool.json', 'w'), indent=1)
    for k, v in sorted(tab.items()):
        log.write(f'{v} {k}\n')
    log.write('DONE\n')
