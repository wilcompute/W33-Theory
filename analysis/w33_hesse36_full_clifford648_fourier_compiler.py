#!/usr/bin/env python3
"""Extend the 36-state Fourier compiler from SL(2,3) to full Clifford648.

Let G = H27_address : SL(2,3), |G|=648. On the ordinary 36 Hesse lines the
physical affine Clifford action is transitive with stabilizer H18. On the 36
maximal compiler-safe planes the natural action (automorphism plus inner H27
conjugation) splits into three 12-orbits. Choosing one aligned point from each
orbit gives a common stabilizer H54 containing H18 as a normal subgroup with

    H54/H18 ~= C3.

The quotient generator is exactly the address-center element z. Therefore

    Ind_H18^G(1)
      ~= direct_sum_{chi in dual(C3)} Ind_H54^G(chi),

and the full 36x36 intertwiner is twelve independent 3-point Fourier
transforms along the central fibers. This is the full-Clifford analogue of the
September-22 complement-level compiler.

The matrix is exact over Q(omega), rank 36, has 108 nonzero entries and
T^*T=3I. After 1/sqrt(3) normalization it is unitary over C.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for candidate in (ROOT,ROOT/"analysis"):
    if str(candidate) not in sys.path: sys.path.insert(0,str(candidate))
OUT=ROOT/"data/w33_hesse36_full_clifford648_fourier_compiler.json"

from w33_exact_eisenstein import ONE,ZERO,matrix_rank,omega_power,zero_matrix

def load_parent():
    path=ROOT/"analysis/w33_maximal_compiler_symmetry_pappus.py"
    s=importlib.util.spec_from_file_location("full648_parent",path); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))

def orbit_sets(perms,n):
    unseen=set(range(n)); out=[]
    while unseen:
        seed=min(unseen); orb={p[seed] for p in perms}
        out.append(tuple(sorted(orb))); unseen-=orb
    return sorted(out,key=lambda x:(len(x),x))

def set_key(S): return tuple(sorted(S))

def main(write=True):
    p=load_parent()
    directions=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    noncentral=directions[1:]
    def cyc(d): return frozenset((p.ID,d,p.hmul(d,d)))
    selected={cyc(d) for d in directions}

    aut216=[(u,v) for u in p.H for v in p.H
            if p.hcomm(u,v)==p.ZC and len(p.gen_h(u,v))==27]
    assert len(aut216)==216
    common24=[]
    for uv in aut216:
        images={frozenset(p.phi(uv,g) for g in S) for S in selected}
        if images==selected: common24.append(uv)
    assert len(common24)==24

    h_index={g:i for i,g in enumerate(p.H)}
    aut_perms=[tuple(h_index[p.phi(uv,g)] for g in p.H) for uv in common24]
    aut_index={q:i for i,q in enumerate(aut_perms)}
    aut_mul=[[aut_index[compose(aut_perms[i],aut_perms[j])] for j in range(24)]
             for i in range(24)]
    idaut=aut_index[tuple(range(27))]
    aut_inv=[next(j for j in range(24)
                  if aut_mul[i][j]==idaut and aut_mul[j][i]==idaut)
             for i in range(24)]

    H=list(p.H); Hidx={g:i for i,g in enumerate(H)}
    def gidx(n,a): return Hidx[n]*24+a
    def gunpack(i): return H[i//24],i%24
    gid=gidx(p.ID,idaut)
    def gmul(i,j):
        n,a=gunpack(i); m,b=gunpack(j)
        am=H[aut_perms[a][Hidx[m]]]
        return gidx(p.hmul(n,am),aut_mul[a][b])
    def ginv(i):
        n,a=gunpack(i); ai=aut_inv[a]
        m=H[aut_perms[ai][Hidx[p.hinv(n)]]]
        out=gidx(m,ai)
        assert gmul(i,out)==gid==gmul(out,i)
        return out
    G=range(648); inverses=[ginv(i) for i in G]
    def gpow(i,n):
        r=gid
        for _ in range(n): r=gmul(r,i)
        return r

    ordinary=set()
    for d in noncentral:
        S=cyc(d)
        ordinary|={frozenset(p.hmul(g,h) for h in S) for g in H}
    ordinary=sorted(ordinary,key=set_key); assert len(ordinary)==36
    oindex={S:i for i,S in enumerate(ordinary)}

    order9=set()
    for x in p.K:
        for y in p.K:
            S=p.subgroup_generated((x,y))
            if len(S)==9: order9.add(S)
    safe=sorted((S for S in order9 if S&p.D=={p.KID}),key=set_key)
    assert len(safe)==36
    sindex={S:i for i,S in enumerate(safe)}

    def conj(n,g): return p.hmul(p.hmul(n,g),p.hinv(n))
    source=[]; target=[]
    for n in H:
        for uv in common24:
            source.append(tuple(
                oindex[frozenset(p.hmul(n,p.phi(uv,g)) for g in L)]
                for L in ordinary))
            target.append(tuple(
                sindex[frozenset((conj(n,p.phi(uv,g)),ext) for g,ext in S)]
                for S in safe))
    assert len(set(source))==648
    assert len(set(target))==216

    source_orbits=orbit_sets(source,36)
    target_orbits=orbit_sets(target,36)
    assert list(map(len,source_orbits))==[36]
    assert list(map(len,target_orbits))==[12,12,12]

    source_seed=0
    H18={g for g in G if source[g][source_seed]==source_seed}
    assert len(H18)==18

    aligned=[]
    for orb in target_orbits:
        choices=[t for t in orb if H18 <= {g for g in G if target[g][t]==t}]
        assert choices
        aligned.append(min(choices))
    H54={g for g in G if target[g][aligned[0]]==aligned[0]}
    assert len(H54)==54
    assert all({g for g in G if target[g][t]==t}==H54 for t in aligned)
    assert H18<=H54
    assert all(gmul(gmul(h,k),inverses[h]) in H18 for h in H54 for k in H18)

    quotient_generator=min(H54-H18)
    assert gunpack(quotient_generator)[0]==(0,0,1)
    assert gunpack(quotient_generator)[1]==idaut
    assert gpow(quotient_generator,3) in H18
    qexp={}
    for e in range(3):
        qe=gpow(quotient_generator,e)
        for h in H18: qexp[gmul(h,qe)]=e
    assert len(qexp)==54

    base_seed=aligned[0]
    reps={}
    for t in target_orbits[0]:
        reps[t]=next(g for g in G if target[g][base_seed]==t)
    assert len(reps)==12

    target_data={}
    for j,seed in enumerate(aligned):
        moved={}
        for _,r in sorted(reps.items()):
            t=target[r][seed]
            moved[t]=r
            target_data[t]=(j,r)
        assert set(moved)==set(target_orbits[j])
    assert len(target_data)==36

    columns=[{} for _ in range(36)]
    for t,(j,r) in target_data.items():
        for e in range(3):
            ge=gmul(r,gpow(quotient_generator,e))
            s=source[ge][source_seed]
            columns[t][s]=(-j*e)%3
    assert Counter(map(len,columns))==Counter({3:36})

    M=zero_matrix(36,36)
    for t,col in enumerate(columns):
        for s,e in col.items(): M[s][t]=omega_power(e)
    assert matrix_rank(M)==36

    # Exact Gram = 3I.
    for a in range(36):
        for b in range(36):
            val=ZERO
            for row in set(columns[a])&set(columns[b]):
                val=val+omega_power(columns[a][row]).conjugate()*omega_power(columns[b][row])
            assert val==(3*ONE if a==b else ZERO)

    phases=[]
    for g in G:
        row=[0]*36
        for t,(j,r) in target_data.items():
            moved=target[g][t]; j2,r2=target_data[moved]; assert j2==j
            h=gmul(inverses[r2],gmul(g,r)); assert h in qexp
            row[t]=(j*qexp[h])%3
        phases.append(tuple(row))

    # Full group law and intertwining.
    for a in G:
        for b in G:
            prod=gmul(a,b)
            for t in range(36):
                assert target[a][target[b][t]]==target[prod][t]
                assert (phases[b][t]+phases[a][target[b][t]])%3==phases[prod][t]
    for g in G:
        for t in range(36):
            left={source[g][s]:e for s,e in columns[t].items()}
            tt=target[g][t]
            right={s:(e+phases[g][t])%3 for s,e in columns[tt].items()}
            assert {k:v%3 for k,v in left.items()}=={k:v%3 for k,v in right.items()}

    serial=[[[s,e] for s,e in sorted(col.items())] for col in columns]
    digest="sha256:"+hashlib.sha256(json.dumps(serial,separators=(",",":")).encode()).hexdigest()
    assert digest=="sha256:e47a3a823d1c0840ec492954c40821ba0ea982e81f6769a041e6aac58fd4ba79"

    out={
      "schema":"w33.hesse36_full_clifford648_fourier_compiler.v1",
      "status":"PASS_FULL_CLIFFORD648_36D_COMPILER_IS_TWELVE_CENTRAL_F3_FOURIER_FIBERS",
      "headline":"The complement-level Hesse36 Fourier compiler extends exactly to all 648 physical one-qutrit Clifford elements. The ordinary 36 is G/H18; each of the three safe 12-sheets is G/H54 with H18 normal in H54 and quotient C3. The quotient generator is literally the address-center element z. Hence Ind_H18^G(1) is the direct sum of the three character-twisted Ind_H54^G modules, and the full compiler is twelve independent three-point Fourier transforms along central fibers.",
      "group":{"G":"H27_address : SL(2,3)","order":648,"source_stabilizer_order":18,
               "target_sheet_stabilizer_order":54,"quotient":"H54/H18 = C3",
               "quotient_generator":"address center z=(0,0,1)","target_permutation_image_order":216},
      "orbits":{"ordinary36":[36],"safe36":[12,12,12],"aligned_safe_seeds":aligned},
      "compiler":{"dimension":36,"field":"Q(omega)","rank":36,"nonzero_entries":108,
                  "column_support_profile":{"3":36},"gram":"T^*T=3I36",
                  "normalized_unitary":"T/sqrt(3)","fiber_count":12,"fiber_size":3,
                  "matrix_digest":digest},
      "checks":{"full_648_source_action":True,"safe_action_image216":True,
                "H18_normal_in_H54":True,"quotient_is_C3":True,
                "quotient_generator_is_address_center":True,"rank36":True,
                "gram_3I":True,"all_648_squared_target_group_law":True,
                "all_648_intertwining_identities":True},
      "boundary":"Exact finite Clifford/compiler theorem. It does not identify safe planes with E8 roots and does not by itself choose a heterotic vacuum or laboratory implementation."
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
