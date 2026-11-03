"""Compress the induced324 carrier to313 without changing its common cover.

The Nov2 induced module owns the Schreier cover and60-dimensional kernel.
This identifies its12 trivial scalar coordinates, retaining the exact old27
action on the reference subspace. No global minimum degree is asserted.
"""
import collections
import itertools
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]


def rank(values):
    basis={}
    for x in values:
        while x:
            k=x.bit_length()-1
            if k in basis:x^=basis[k]
            else:basis[k]=x;break
    return len(basis)


def build():
    d=json.loads((ROOT/'data/w33_20261102_induced_cubic_common_cover.json').read_text())
    native=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    terms={tuple(row['triple']):row['coefficient'] for row in native['coefficient_rows']}
    gens=d['signed_generator_permutations'];signs=[int(x,16) for x in d['signed_generator_bits_hex']]
    relations=[int(w['sign_delta_hex'],16) for w in d['kernel_relation_witnesses']]
    characters=[sum(((w>>i)&1)<<j for j,w in enumerate(relations)) for i in range(324)]
    zero=[i for i,c in enumerate(characters) if not c]
    assert zero==list(range(0,324,27))
    unseen=set(range(324));orbits=[]
    while unseen:
        root=min(unseen);seen={root};queue=[root]
        for a in queue:
            for p in gens:
                if p[a] not in seen:seen.add(p[a]);queue.append(p[a])
        unseen-=seen;orbits.append(sorted(seen))
    assert list(map(len,orbits))==[12,120,192]
    assert collections.Counter(collections.Counter(characters).values())=={12:1,2:60,1:192}
    def compress(i):return 0 if i%27==0 else 1+(i//27)*26+(i%27-1)
    compressed=[]
    for p,b in zip(gens,signs):
        q=[None]*313;bits=[None]*313
        for i in range(324):
            a=compress(i);image=compress(p[i]);sign=(b>>i)&1
            if q[a] is not None:assert q[a]==image and bits[a]==sign
            q[a]=image;bits[a]=sign
        assert q[0]==0 and bits[0]==0 and sorted(q)==list(range(313))
        compressed.append((q,bits))
    cubic=collections.Counter()
    for block in range(12):
        for t,c in terms.items():cubic[tuple(sorted(compress(27*block+i) for i in t))]+=c
    cubic={t:c for t,c in cubic.items() if c};assert len(cubic)==540  # {540:unrelated}
    for q,bits in compressed:
        transformed={tuple(sorted(q[i] for i in t)):c*(-1)**sum(bits[i] for i in t) for t,c in cubic.items()}
        assert transformed==cubic
    for j,(p,b) in enumerate(compressed[:6]):
        old=native['signed_generators'][j]
        assert p[:27]==old['permutation'] and b[:27]==old['sign_bits']
    restricted={t:c for t,c in cubic.items() if max(t)<27}
    assert restricted==terms
    compressed_relations=[sum(((w>>i)&1)<<compress(i) for i in range(324) if i%27) for w in relations]
    assert rank(relations)==rank(compressed_relations)==60
    orbit_rank={str(len(o)):rank([sum(((w>>i)&1)<<j for j,i in enumerate(o)) for w in relations]) for o in orbits}
    return dict(status='PASS_INDUCED313_NATIVE_CUBIC_COMPRESSION',old_dimension=324,new_dimension=313,
        old_coordinate_orbits=orbits,kernel_character_multiplicity_histogram={'1':192,'2':60,'12':1},
        sign_kernel_restriction_ranks=orbit_rank,coordinate_map=[compress(i) for i in range(324)],
        signed_generator_permutations=[p for p,b in compressed],signed_generator_bits=[b for p,b in compressed],
        compressed_cubic=[dict(triple=t,coefficient=c) for t,c in sorted(cubic.items())],
        old_reference27_subspace=list(range(27)),old_native45_term_restriction=True,
        common_cover_order=d['paired_common_cover_order'],remaining_sign_kernel_rank=60,
        group_obstruction='Within this induced cover, a normal sign-kernel quotient preserving the exact faithful old27 action on block0 must act trivially there. Conjugation transports that condition to all12 blocks. The signed action is faithful, so that quotient kernel is trivial. Other common-cover constructions are not excluded.',
        compression_scope='Identify all12 fixed local scalar coordinates with one common scalar. Retain every312 nontrivial coordinate and the homogeneous native cubic on the reference27. This is a concrete313-dimensional carrier, not a global minimal-degree theorem.',
        boundary='Algebraic carrier compression with unchanged finite group order. No physical multiplet count, generations or gauge dynamics inferred.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_induced_cubic_compression.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['new_dimension'],d['sign_kernel_restriction_ranks'],flush=True)
