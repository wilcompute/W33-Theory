#!/usr/bin/env python3
"""Independent GF(2) integer-bitset verifier of five-qubit partial
Pauli MUB rank-code data:
- rebuild 32,768 symmetric matrices and their invertibility from
  scratch, with no imports of the original rank-code solver;
- independently enumerate all O(5,2) matrices and 8 congruence
  orbits of normalized second matrices;
- verify two S3 equivalence classes via S^-1 and S+I;
- verify every saved size-nine witness from two independent search
  traversal orders, including all 13,888 possible extenders;
- audit both exhaustive completed size-eight search certificates,
  but explicitly distinguish checking logs from recomputing
  their 433-million/108-million-node negative search.
"""
from pathlib import Path
from itertools import combinations
import json,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261114_independent_MUB_rankcode_orbit_witness_audit.json"
def positions(n):return [(i,j) for i in range(n) for j in range(i,n)]
def code(rows,pos):
    return sum(((rows[i]>>j)&1)<<b for b,(i,j) in enumerate(pos))
def rows(n,c,pos):
    M=[0]*n
    for b,(i,j) in enumerate(pos):
        if c>>b&1:
            M[i]|=1<<j;M[j]|=1<<i
    return M
def rank(M,n):
    M=list(M)
    k=0
    for col in range(n):
        pivot=next((t for t in range(k,n) if M[t]>>col&1),None)
        if pivot is None:continue
        M[k],M[pivot]=M[pivot],M[k]
        for r in range(n):
            if r!=k and (M[r]>>col)&1:M[r]^=M[k]
        k+=1
        if k==n:break
    return k
def inverse(M,n):
    A=[M[i]|(1<<(n+i)) for i in range(n)]
    for col in range(n):
        k=next(i for i in range(col,n) if A[i]>>col&1)
        A[col],A[k]=A[k],A[col]
        for i in range(n):
            if i!=col and A[i]>>col&1:A[i]^=A[col]
    assert all((A[i]&((1<<n)-1))==1<<i for i in range(n))
    return [A[i]>>n for i in range(n)]
def ortho(n):
    odd=[z for z in range(1,1<<n) if z.bit_count()&1]
    ans=[]
    def rec(A):
        if len(A)==n:
            ans.append(tuple(A));return
        for v in odd:
            if all((v&w).bit_count()%2==0 for w in A):
                rec(A+[v])
    rec([])
    return ans
def congr(A,S,pos,n):
    AS=[0]*n
    for i in range(n):
        for k in range(n):
            if (A[i]>>k)&1:AS[i]^=S[k]
    output=[0]*n
    for i in range(n):
        for j in range(n):
            if (AS[i]&A[j]).bit_count()&1:output[i]|=1<<j
    return code(output,pos)
def test_nine(witness,sing,ns,n=5):
    assert len(witness)==7 and len(set(witness))==7
    for a in witness:
        assert not sing[a]
    for a,b in combinations(witness,2):
        assert not sing[a^b],(a,b)
    # The fixed L0,L_infinity have no other extenders than nonsingular
    # graph(S). Every such graph either equals a chosen S or
    # intersects one of the seven chosen graph Lagrangians.
    for t in ns:
        if t in witness:continue
        assert any(sing[t^s] for s in witness),t
    return True

def main():
    n=5;pos=positions(n)
    size=1<<(n*(n+1)//2)
    sing=bytearray(size);ns=[]
    for c in range(size):
        if rank(rows(n,c,pos),n)==n:ns.append(c)
        else:sing[c]=1
    assert len(ns)==13888
    I=code([1<<i for i in range(n)],pos)
    assert I==21025
    cand=[c for c in ns if not sing[c^I]]
    assert len(cand)==5760
    orth=ortho(n)
    assert len(orth)==720,len(orth)
    reps=[692,693,694,695,700,701,702,703]
    all_seen=set();orbits=[]
    lookup={}
    for r,rep in enumerate(reps):
        orbit={congr(A,rows(n,rep,pos),pos,n) for A in orth}
        assert orbit <= set(cand)
        assert not orbit&all_seen
        for z in orbit:lookup[z]=r
        all_seen |= orbit
        orbits.append(len(orbit))
    assert all_seen==set(cand)
    images_inv=[];images_shift=[]
    for rep in reps:
        im=code(inverse(rows(n,rep,pos),n),pos)
        images_inv.append(lookup[im])
        images_shift.append(lookup[rep^I])
    def components(actions):
        par=list(range(len(reps)))
        def f(i):
            while par[i]!=i:i=par[i]
            return i
        for a in actions:
            for i,j in enumerate(a):par[f(i)]=f(j)
        return sorted(sorted(k for k in range(len(reps)) if f(k)==p)
                      for p in {f(k) for k in range(len(reps))})
    classes=components((images_inv,images_shift))
    assert classes==[[0,1],[2,3,4,5,6,7]],classes
    full=json.loads((ROOT/"data/w33_five_qubit_size8_dlx_full.json").read_text())["n5_size8"]
    back=json.loads((ROOT/"data/w33_five_qubit_size8_dlx_reverse.json").read_text())["n5_size8"]
    assert full["status"]==back["status"]=="none"
    assert full["nodes"]==433517130 and back["nodes"]==107943913
    assert not any(x["found"] is not None or x["timeout"] for x in full["per_rep"]+back["per_rep"])
    assert [x["s2"] for x in full["per_rep"]]==reps
    assert [x["s2"] for x in back["per_rep"]]==[692,694]
    verified={}
    for f in ("data/w33_five_qubit_size9_dlx.json",
              "data/w33_five_qubit_size9_dlx_reverse.json"):
        g=json.loads((ROOT/f).read_text())["control_n5_size9"]
        assert g["status"]=="exists"
        witnesses=[z["found"] for z in g["per_rep"] if z["found"]]
        assert all(test_nine(z,sing,ns) for z in witnesses)
        verified[f]={"witnesses_independently_verified":len(witnesses),
                     "representatives":[int(z["s2"]) for z in g["per_rep"]]}
    result={
      "status":"PASS_INDEPENDENT_GF2_8_ORBITS_2_S3_CLASSES_AND_ALL_SIZE9_WITNESSES",
      "all_symmetric_5x5":size,"all_nonsingular":len(ns),
      "nonsingular_second_candidates":len(cand),"orthogonal_group_O5_order":len(orth),
      "eight_O5_representatives":reps,"eight_orbit_sizes":orbits,
      "full_5760_candidate_orbit_partition_verified":True,
      "inverse_S3_orbit_permutation":images_inv,
      "shift_S3_orbit_permutation":images_shift,
      "two_S3_classes":classes,
      "forward_search_reported_nodes":int(full["nodes"]),
      "reversed_search_reported_nodes":int(back["nodes"]),
      "both_reported_complete_no_timeout":True,
      "all_forward_reverse_size9_witnesses_independently_checked":verified,
      "proof_scope":"Independent GF2 core and exact positive-witness/canonical orbit checks. Read-only audit of negative-search logs, NOT an independent complete negative-search proof; reverse traversal is the same algorithm family and its claimed 107,943,913 nodes were not replayed.",
      "theoretical_translation":"Two fixed graph Lagrangians plus seven nonsingular symmetric graph matrices: pairwise differences nonsingular and all 13,888 candidate extenders intersect one of the chosen."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ["status","all_nonsingular","orthogonal_group_O5_order","eight_orbit_sizes","two_S3_classes","all_forward_reverse_size9_witnesses_independently_checked"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
