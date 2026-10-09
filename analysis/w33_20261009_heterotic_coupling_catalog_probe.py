"""Cross-check every all-order gauge candidate against existing orbifolder
*.dbd, *.mu, *.ch coupling catalogs, without assuming their completeness.

Catalog semantics must be independently established before any F-flatness
assertion. Save SHA256, raw line counts, and exact multiset matches.
"""
from pathlib import Path
import hashlib,json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
BASE=Path.home()/'orb/scan/cp2/out/Z6II_34__SM_20260917_1558'
def main():
    d=json.loads((ROOT/'data/w33_20261009_all_order_one_outsider_F_gate.json').read_text())
    targets={}
    for m in d['monomials']:
        seq=list(m['exponents'].items())
        fields=tuple(sorted([m['outside']]+[x for x,k in seq for _ in range(k)]))
        targets[m['outside']]=fields
    out={}
    for ext in ('dbd','mu','ch'):
        f=BASE.with_suffix('.'+ext)
        if not f.exists():
            out[ext]=dict(found=False);continue
        contents=f.read_text().splitlines()
        parsed=[]
        for line in contents:
            w=line.split()
            if len(w)>2 and w[0]=='C' and w[1].isdigit() and len(w)==int(w[1])+2:
                parsed.append((tuple(sorted(w[2:])),line))
        matches={k:[text for tup,text in parsed if tup==target] for k,target in targets.items()}
        out[ext]=dict(found=True,source_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
            lines=len(contents),parsed_C_lines=len(parsed),
            matching_count=sum(bool(v) for v in matches.values()),
            matches={k:v for k,v in matches.items() if v})
    coverage={}
    required=set(x for tup in targets.values() for x in tup)
    for ext in ('w','sp'):
        f=(BASE.with_suffix('.'+ext) if ext=='w' else
           Path.home()/'orb/scan/cp2/sp'/(BASE.name+'.sp'))
        present=set()
        if f.is_file():
            for line in f.read_text().splitlines():
                parts=line.split()
                if len(parts)>=2 and parts[0] in ('W','S'):present.add(parts[1])
        coverage[ext]=dict(source_found=f.is_file(),total_distinct_fields=len(present),
            required_field_count=len(required),required_fields_present=sorted(required & present),
            required_fields_missing=sorted(required - present))
    return dict(status='PASS',source_model=str(BASE.name),candidate_count=len(targets),
        field_metadata_coverage=coverage,by_catalog=out,
        scope='Exact whole-field-multiset matching against existing catalog C records. No independent evidence here that any catalog lists every possible string-level superpotential coupling, or that catalog presence means nonzero coefficient.')
if __name__=='__main__':
    d=main()
    (ROOT/'data/w33_20261009_heterotic_coupling_catalog_probe.json').write_text(json.dumps(d,indent=2)+'\n')
    print({x:{k:v for k,v in a.items() if k!='matches'} for x,a in d['by_catalog'].items()})
    for x,a in d['by_catalog'].items():print(x,a.get('matches'))
