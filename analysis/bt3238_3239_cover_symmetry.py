#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, math
import numpy as np
from bt3238_3249_common import compose, perm_order, psp_group, frame_permutations

def cover_symmetry(m,h,points,lines,frames,point_generators,cover,loci,coords,family):
    group,word=psp_group(point_generators)
    fp=frame_permutations(group,points,lines,frames)
    c2i={c:i for i,c in enumerate(coords)}
    t2i={t:i for i,t in enumerate(family)}
    # Deterministic two-channel hashes only shortlist candidates; every candidate is checked exactly.
    weights=[]
    for salt in ("w33-cover-hash-A","w33-cover-hash-B"):
        weights.append(np.array([int.from_bytes(hashlib.sha256(f"{salt}:{v}".encode()).digest()[:8],"big")
                                 for v in range(540)],dtype=np.uint64))
    fam_hash=collections.defaultdict(list)
    for i,cov in enumerate(family):
        fam_hash[tuple(int(np.sum(w[list(cov)],dtype=np.uint64)) for w in weights)].append(i)

    def exact_images(cov):
        arr=np.asarray(cov,dtype=np.int64); images=fp[:,arr]
        hh=[np.sum(w[images],axis=1,dtype=np.uint64) for w in weights]
        return arr,images,hh

    stabilizers=[]; intersections=[]
    for i,cov in enumerate(family):
        arr,images,hh=exact_images(cov)
        target=tuple(int(np.sum(w[arr],dtype=np.uint64)) for w in weights)
        stab=0; members=set()
        for gi,key in enumerate(zip(*(map(int,x) for x in hh))):
            candidates=fam_hash.get(key,())
            if key==target or candidates:
                image=tuple(sorted(map(int,images[gi])))
                if key==target and image==cov: stab+=1
                for j in candidates:
                    if image==family[j]: members.add(j)
        stabilizers.append(stab); intersections.append(len(members))
    assert collections.Counter(stabilizers)==collections.Counter({2:216,4:27})
    assert collections.Counter(intersections)==collections.Counter({2:216,1:27})

    tau=lambda x:((-x[3])%3,(1-x[2])%3,(1-x[1])%3,(-x[0])%3,x[4])
    fixed=[c for c in coords if tau(c)==c]
    assert len(fixed)==27
    for i,c in enumerate(coords):
        orbit_members={j for j,d in enumerate(coords) if d in {c,tau(c)}}
        # exact PSp orbit intersection has size one or two and is precisely the affine involution orbit
        arr,images,hh=exact_images(family[i]); found=set()
        for gi,key in enumerate(zip(*(map(int,x) for x in hh))):
            for j in fam_hash.get(key,()):
                if tuple(sorted(map(int,images[gi])))==family[j]: found.add(j)
        assert found==orbit_members

    base=np.asarray(family[0],dtype=np.int64)
    candidate_setwise=[]
    for gi in range(len(group)):
        image=tuple(sorted(map(int,fp[gi,base])))
        if image in t2i:
            ok=True
            for cov in family:
                if tuple(sorted(map(int,fp[gi,np.asarray(cov,dtype=np.int64)]))) not in t2i:
                    ok=False; break
            if ok: candidate_setwise.append(gi)
    assert len(candidate_setwise)==4
    orders=sorted(perm_order(group[g]) for g in candidate_setwise)
    assert orders==[1,2,4,4]
    generator=next(g for g in candidate_setwise if perm_order(group[g])==4)
    square=next(g for g in candidate_setwise if perm_order(group[g])==2)
    assert compose(group[generator],group[generator])==group[square]
    for c,cov in zip(coords,family):
        image=tuple(sorted(map(int,fp[generator,np.asarray(cov,dtype=np.int64)])))
        assert coords[t2i[image]]==tau(c)
        image2=tuple(sorted(map(int,fp[square,np.asarray(cov,dtype=np.int64)])))
        assert image2==cov

    # The 27 fixed points form an affine [5,3] ternary code, not a Schlaefli graph.
    param={(a,b,c):(a,b,(1-b)%3,(-a)%3,c) for a,b,c in itertools.product(range(3),repeat=3)}
    fixed_sets={p:set(family[c2i[x]]) for p,x in param.items()}
    relation=collections.Counter()
    relm={}
    for p,q in itertools.combinations(sorted(param),2):
        da,db,dc=((q[k]-p[k])%3 for k in range(3))
        expected=60-8*(da!=0)-8*(db!=0)-4*(dc!=0)
        actual=len(fixed_sets[p]&fixed_sets[q]); assert actual==expected
        relation[actual]+=1
    assert relation==collections.Counter({40:108,48:108,44:54,52:54,56:27})
    values=sorted(relation)
    for val in values:
        A=np.zeros((27,27),dtype=np.int8)
        ps=sorted(param)
        for i,j in itertools.combinations(range(27),2):
            if len(fixed_sets[ps[i]]&fixed_sets[ps[j]])==val:A[i,j]=A[j,i]=1
        relm[val]=A
    schlaefli_hits=[]
    for mask in range(1,1<<len(values)):
        A=sum((relm[values[i]] for i in range(len(values)) if mask>>i&1),np.zeros((27,27),dtype=np.int8))
        if set(map(int,A.sum(1)))!={10}: continue
        AA=A@A; lam=set(); mu=set()
        for i,j in itertools.combinations(range(27),2):
            (lam if A[i,j] else mu).add(int(AA[i,j]))
        if lam=={1} and mu=={5}: schlaefli_hits.append(mask)
    assert not schlaefli_hits
    return {
      "group_order":len(group),
      "setwise_stabilizer_order":4,
      "setwise_stabilizer_structure":"C4",
      "setwise_element_orders":orders,
      "order4_generator_index":generator,
      "order4_generator_word_in_four_transvections":word(generator),
      "pointwise_kernel_order":2,
      "pointwise_kernel_generator_index":square,
      "pointwise_kernel_word_in_four_transvections":word(square),
      "induced_affine_involution":"(-x4, 1-x3, 1-x2, -x1, x5) over F3",
      "fixed_affine_flat_equations":["x3=1-x2","x4=-x1"],
      "fixed_covers":27,
      "paired_covers":216,
      "internal_PSp_orbit_classes":135,
      "internal_orbit_intersection_histogram":{"1":27,"2":216},
      "cover_stabilizer_order_histogram":{"2":216,"4":27},
      "full_PSp_orbit_sizes":{"generic":12960,"fixed_flat":6480},
      "five_qutrit_boundary":"The F3^5 coordinates parametrize 243 exact covers, but PSp(4,3) induces only one affine involution (with a C2 pointwise kernel), not a five-qutrit affine symmetry.",
      "fixed27_affine_code":{
        "parameterization":"(a,b,c) -> (a,b,1-b,-a,c)",
        "length":5,"dimension":3,"minimum_hamming_distance":1,
        "difference_weight_distribution":{"1":2,"2":4,"3":8,"4":4,"5":8},
        "cover_intersection_formula":"60-8[da!=0]-8[db!=0]-4[dc!=0]",
        "intersection_pair_histogram":{str(k):int(v) for k,v in sorted(relation.items())},
        "Schlaefli_SRG_27_10_1_5_relation_unions":0,
        "conclusion":"The count 27 does not produce the Schlaefli graph; the exact structure is a weighted ternary Hamming cube."
      }
    }
