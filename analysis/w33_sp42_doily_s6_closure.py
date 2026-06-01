from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXV_SP42_DOILY_S6_CLOSURE_results.json'

from analysis.w33_s6_outer_automorphism_class_swap import main as outer_main
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


def bxor(a,b): return tuple(x^y for x,y in zip(a,b))
def mat_vec(M,x): return tuple(sum(M[i][j]*x[j] for j in range(4))%2 for i in range(4))
def mat_mul(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4))%2 for j in range(4)) for i in range(4))
def transpose(A): return tuple(tuple(A[j][i] for j in range(4)) for i in range(4))
def bform(B,x,y): return sum(x[i]*B[i][j]*y[j] for i in range(4) for j in range(4))%2

def mat_from_cols(cols): return tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))

def rank_gf2(rows):
    rows=[sum((b&1)<<i for i,b in enumerate(row)) for row in rows]
    r=0
    for col in range(4):
        pivot=next((i for i in range(r,len(rows)) if (rows[i]>>col)&1), None)
        if pivot is None: continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>col)&1): rows[i]^=rows[r]
        r+=1
    return r

def main():
    outer=outer_main()
    u=[(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,1,1)]
    duads=list(combinations(range(6),2))
    labels={e:bxor(u[e[0]],u[e[1]]) for e in duads}
    label_set=set(labels.values())
    basis_duads=[(0,1),(0,2),(0,3),(0,4)]
    B=((0,1,1,1),(1,0,1,1),(1,1,0,1),(1,1,1,0))
    I=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))

    s6_mats=set()
    for p in permutations(range(6)):
        cols=[labels[tuple(sorted((p[a],p[b])))] for a,b in basis_duads]
        M=mat_from_cols(cols)
        assert all(mat_vec(M, labels[e]) == labels[tuple(sorted((p[e[0]],p[e[1]])))] for e in duads)
        s6_mats.add(M)

    rows=list(product([0,1], repeat=4)); pts=list(product([0,1], repeat=4)); nz=[v for v in pts if any(v)]
    gl4=[]; sp=[]
    for M in product(rows, repeat=4):
        if len({mat_vec(M,x) for x in pts})==16:
            gl4.append(M)
            if mat_mul(mat_mul(transpose(M),B),M)==B:
                sp.append(M)
    sp=set(sp)

    # PG(3,2) line split by symplectic polarity: isotropic iff pairwise B=0.
    iso_lines=set(); noniso_lines=set()
    for a,b in combinations(sorted(label_set),2):
        c=bxor(a,b)
        line=tuple(sorted((a,b,c)))
        if bform(B,a,b)==0: iso_lines.add(line)
        else: noniso_lines.add(line)

    onefactors=perfect_matchings(range(6))
    triangles=[tuple(sorted(combinations(T,2))) for T in combinations(range(6),3)]
    onefactor_lines={tuple(sorted(labels[e] for e in F)) for F in onefactors}
    triangle_lines={tuple(sorted(labels[e] for e in T)) for T in triangles}

    point_line_inc=Counter(x for L in iso_lines for x in L)
    pair_line_inc=Counter(tuple(sorted(p)) for L in iso_lines for p in combinations(L,2))
    # Generalized quadrangle property for W(3,2): for point p not on line L, unique isotropic line through p meeting L.
    gq_ok=True
    for p in label_set:
        for L in iso_lines:
            if p in L: continue
            candidates=[]
            for M in iso_lines:
                if p in M and set(M)&set(L): candidates.append(M)
            if len(candidates)!=1:
                gq_ok=False; break
        if not gq_ok: break

    checks={
      'inherits_outer_automorphism':outer['n_verified']==outer['n_checks']==15,
      'b_alternating_zero_diagonal':all(B[i][i]==0 for i in range(4)),
      'b_nondegenerate_rank_4':rank_gf2(B)==4,
      'duad_labels_all_15_nonzero':len(label_set)==15 and (0,0,0,0) not in label_set,
      's6_duad_action_linear_720':len(s6_mats)==720,
      'gl4_order_20160':len(gl4)==20160,
      'sp42_order_720':len(sp)==720,
      's6_equals_sp42':s6_mats==sp,
      'all_s6_preserve_b':all(mat_mul(mat_mul(transpose(M),B),M)==B for M in s6_mats),
      'pg32_lines_split_15_20':len(iso_lines)==15 and len(noniso_lines)==20,
      'onefactors_are_isotropic_lines':onefactor_lines==iso_lines,
      'triangles_are_nonisotropic_lines':triangle_lines==noniso_lines,
      'doily_points_15_lines_15':len(label_set)==15 and len(iso_lines)==15,
      'doily_line_size_3':all(len(L)==3 for L in iso_lines),
      'doily_each_point_on_3_lines':Counter(point_line_inc.values())==Counter({3:15}),
      'doily_collinear_pairs_45':len(pair_line_inc)==45 and set(pair_line_inc.values())=={1},
      'doily_gq_2_2_property':gq_ok,
      'sp42_s6_order_identity':720==6*120==15*48,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXV',
      'theorem':'Sp(4,2)/doily S6 closure',
      'symplectic_form':B,
      'orders':{'S6_duad_action':len(s6_mats),'Sp(4,2)':len(sp),'GL(4,2)':len(gl4)},
      'line_split':{'PG(3,2)_lines':35,'symplectic_doily_lines_onefactors':15,'nonisotropic_triangle_lines':20},
      'doily':{'points':15,'lines':15,'line_size':3,'lines_per_point':3,'collinear_pairs':45,'GQ_order':'(2,2)'},
      'reading':'The K6-duad labeling is not merely combinatorial: the induced 720 S6 actions on the 15 duads are exactly the 720 linear maps preserving the nondegenerate alternating form B on F2^4. Thus S6 closes as Sp(4,2). The symplectic polarity selects exactly the 15 K6 one-factors as isotropic PG(3,2) lines, while the 20 K6 triangles are the nonisotropic PG(3,2) lines. This upgrades the previous PG(3,2) operation weld to the doily W(3,2) geometry.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['orders'], r['line_split'])
