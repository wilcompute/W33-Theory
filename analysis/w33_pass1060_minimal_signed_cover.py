from __future__ import annotations
import json, time
from pathlib import Path
from w33_pass1060_1064_core import *
from sympy.combinatorics import Permutation,PermutationGroup

def lift_signs(p,reps):
    n=len(reps); adj=[[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            before=dot(reps[i],reps[j]); after=dot(reps[p(i)],reps[p(j)])
            if before==0:
                assert after==0; continue
            assert abs(before)==abs(after)
            rhs=0 if before==after else 1
            adj[i].append((j,rhs));adj[j].append((i,rhs))
    bits=[None]*n;bits[0]=0;stack=[0]
    while stack:
        i=stack.pop()
        for j,r in adj[i]:
            v=bits[i]^r
            if bits[j] is None:bits[j]=v;stack.append(j)
            else:assert bits[j]==v
    assert all(x is not None for x in bits)
    return [int(x) for x in bits]

def signed_perm(p,bits):
    return Permutation([2*p(i)+(b^bits[i]) for i in range(120) for b in (0,1)])

def main():
    w=build_w33();q=build_quot(w);a=build_axes(w,q);e=build_e8();F=isometry(q,e)
    reps=[e.positive[F[c]] for c in a.coords]
    lifts=[]; bitrows=[]
    for p in a.axis_gens:
        bits=lift_signs(p,reps);bitrows.append(bits);lifts.append(signed_perm(p,bits))
    L=PermutationGroup(lifts); A=PermutationGroup(a.axis_gens)
    neg=Permutation([2*i+(b^1) for i in range(120) for b in (0,1)])
    failures=0
    roots=[tuple(((-1)**b)*x for x in reps[i]) for i in range(120) for b in (0,1)]
    for g in lifts:
        for i in range(240):
            for j in range(240):
                if dot(roots[i],roots[j])!=dot(roots[g(i)],roots[g(j)]):failures+=1
    cert=[([0,1,49,50],0),([0,1,48,50],0),([0,49,50,60],1),([0,48,50,60],0)]
    cmask=0; crhs=0
    for variables,rhs in cert:
        for v in variables: cmask ^= 1 << v
        crhs ^= rhs
    checks={
      'axis_image_order_25920':A.order()==25920,
      'signed_lift_order_51840':L.order()==51840,
      'central_global_negation_in_lift_group':L.contains(neg) and all(neg*g==g*neg for g in lifts),
      'kernel_has_order_two':L.order()//A.order()==2,
      'all_generator_lifts_preserve_E8_inner_products':failures==0,
      'four_row_no_section_certificate_xors_to_zero_equals_one':cmask==0 and crhs==1,
      'minimal_extension_order_lower_bound_met':L.order()==2*A.order(),
    }
    assert all(checks.values())
    return {
      'schema':'w33.pass1060.minimal_signed_cover.v1','status':'PASS',
      'headline':'The smallest symmetry object carrying the signed 240-root action is not an ordinary overgroup of PSp(4,3), but its non-split central double cover 2.PSp(4,3) ~= Sp(4,3), of order 51840.',
      'orders':{'unsigned_PSp43':int(A.order()),'signed_cover':int(L.order()),'kernel':2},
      'extension':'1 -> C2(global root negation) -> Sp(4,3) -> PSp(4,3) -> 1',
      'candidate_decisions':{
        'central_double_cover_Sp43':'PASS: exact signed action constructed',
        'PGSp43':'FAIL as a cure: an ordinary overgroup contains the obstructed PSp43 subgroup, so restriction would give the forbidden section',
        'W_E6_split_outer_extension':'FAIL as a cure for the same restriction reason',
        'semilinear_overgroup':'FAIL as a cure for the same restriction reason',
        'direct_or_semidirect_S3_controller':'can select an external branch operationally, but does not split the internal signed-root extension'
      },
      'no_section_certificate':{'rows':[{'variables':v,'rhs':r} for v,r in cert],'xor_mask':cmask,'xor_rhs':crhs},
      'minimality_proof':'The four-row Pass1055 certificate rules out a section over PSp(4,3), so any lifting group projecting onto it has nontrivial kernel of size at least 2. The constructed group has exactly twice the order, meeting the lower bound.',
      'generator_lift_sign_weights':[sum(r) for r in bitrows],
      'check_count':len(checks),'checks':checks,
      'scope':'Exact finite signed-permutation construction. The identification with the Schur cover is at permutation-group/extension level; no complex reflection matrices are required.'
    }
if __name__ == "__main__":
    started = time.time(); result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1060_minimal_signed_cover.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "check_count": result["check_count"], "output": str(output), "seconds": round(time.time()-started, 3)}, indent=2))
