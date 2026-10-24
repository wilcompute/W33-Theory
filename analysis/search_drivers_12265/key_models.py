"""12265b: the Ploger status of the models the corpus actually claimed: S002 / T115 (12121-12155 lead models), and every model
named in the certificates of 12111 (three-generation SO(10)), 12116 (SU3xSU2xSU2) and 12121-12155 (k_Y, crossed models)."""
import glob, json, os, re, sys
exec(open('audit_all.py').read().split("files = [l.strip()")[0])
files = [l.strip() for l in open('files_win.txt', encoding='utf-8') if l.strip()]
index = {}
for f in files:
    try:
        t = open(f, encoding='utf-8', errors='ignore').read()
    except OSError:
        continue
    for blk in t.split('begin model')[1:]:
        m = re.search(r'Label:(\S+)', blk)
        if not m or 'Shifts and Wilsonlines:' not in blk:
            continue
        try:
            rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n') if r.strip()]
        except Exception:
            continue
        if not rows or any(len(r) != 16 for r in rows) or len(rows) < 7:
            continue
        index.setdefault(m.group(1), (f, check_block(rows)))
claimed = set()
for cert in glob.glob(r'C:\tmp\toe_wt\data\w33_pass121[0-6]*.json'):
    txt = open(cert, encoding='utf-8', errors='ignore').read()
    for lab in re.findall(r'"(N0\d\d_F1_0\d_[A-Z]\d{3}|N0\d\d_F1_0\d_9|[A-Z]\d{3}_[A-Za-z0-9_]+)"', txt):
        claimed.add(lab)
for lab in list(index):
    if re.search(r'_S002$|_T115$|S002|T115', lab):
        claimed.add(lab)
res = {lab: dict(file=index[lab][0], fails=index[lab][1]) for lab in sorted(claimed) if lab in index}
bad = {k: v for k, v in res.items() if v['fails']}
print('claimed labels found', len(res), 'inconsistent', len(bad))
for k, v in list(bad.items())[:40]:
    print(k, v['fails'], os.path.basename(os.path.dirname(v['file'])))
for k in res:
    if 'S002' in k or 'T115' in k:
        print('KEY', k, res[k]['fails'], os.path.basename(os.path.dirname(res[k]['file'])))
json.dump(dict(found=len(res), inconsistent=bad, all=res), open('key_models.json', 'w'), indent=1)
