from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXV_AG32_RM13_AUTOMORPHISM_results.json'

def add(a,b): return tuple(x^y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b)) % 2

def mat_vec(M,x): return tuple(dot(row,x) for row in M)
def block_perm(p,B): return tuple(sorted(p[i] for i in B))

def main():
    pts=list(product([0,1], repeat=3)); idx={p:i for i,p in enumerate(pts)}
    nz=[p for p in pts if p!=(0,0,0)]
    planes=[]
    for n in nz:
        pair=[]
        for b in (0,1):
            B=tuple(sorted(idx[x] for x in pts if dot(n,x)==b))
            planes.append((n,b,B)); pair.append(B)
        assert set(pair[0]).isdisjoint(pair[1]) and sorted(pair[0]+pair[1])==list(range(8))
    blocks={B for _,_,B in planes}
    triples=Counter(t for B in blocks for t in combinations(B,3))

    rows=list(product([0,1], repeat=3)); GL=[]
    for M in product(rows, repeat=3):
        if len({mat_vec(M,x) for x in pts})==8:
            GL.append(M)
    AGL=[]
    for M in GL:
        for t in pts:
            p=tuple(idx[add(mat_vec(M,x),t)] for x in pts)
            assert all(block_perm(p,B) in blocks for B in blocks)
            AGL.append(p)
    AGL=set(AGL)
    AUT={p for p in permutations(range(8)) if all(block_perm(p,B) in blocks for B in blocks)}

    # Fano plane on the 7 normal directions: {a,b,a+b}.
    norm_idx={n:i+1 for i,n in enumerate(nz)}
    lines={tuple(sorted((norm_idx[a],norm_idx[b],norm_idx[add(a,b)]))) for a,b in combinations(nz,2) if add(a,b)!=(0,0,0)}
    ldeg=Counter(x for L in lines for x in L)
    pairdeg=Counter(tuple(sorted(p)) for L in lines for p in combinations(L,2))

    checks={
      'plane_count_14':len(blocks)==14,
      'parallel_classes_7':len(planes)==14 and len(nz)==7,
      'sqs8':len(triples)==56 and set(triples.values())=={1},
      'gl32_order_168':len(GL)==168,
      'agl32_order_1344':len(AGL)==1344,
      'full_aut_equals_agl32':AUT==AGL and len(AUT)==1344,
      'translation_factor_8':len(pts)==8,
      'fano_normals':len(lines)==7 and set(ldeg.values())=={3} and len(pairdeg)==21 and set(pairdeg.values())=={1},
      'order_identity_8x168':8*168==1344,
      'order_identity_7x192':7*192==1344,
      'order_identity_14x96':14*96==1344,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXV',
      'theorem':'AG(3,2)/RM(1,3) automorphism bridge',
      'objects':{'points':8,'affine_planes':14,'parallel_classes':7,'sqs_triples':56},
      'groups':{'GL(3,2)':len(GL),'AGL(3,2)':len(AGL),'full_SQS8_automorphism_group':len(AUT)},
      'identities':{'AGL=8*168':8*168,'AGL=7*192':7*192,'AGL=14*96':14*96},
      'fano_lines_on_normals':sorted(lines),
      'reading':'The fourteen RM(1,3) weight-4 words are the fourteen affine planes of AG(3,2). Their seven complement pairs are the seven parallel classes/Fano normals. The full permutation automorphism group is exactly AGL(3,2), so the 168 PSL(2,7) factor is the linear stabilizer and the 8 factor is the affine translation/tomotope-cell factor.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__ == '__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['groups'])
