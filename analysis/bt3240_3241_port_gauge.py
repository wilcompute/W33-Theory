#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, json, math
import numpy as np

def block_complex(m,h,blocks):
    d=np.zeros((540,45),dtype=np.int8)
    for j,b in enumerate(blocks):d[b,j]=1
    n=((d.T@m)>0).astype(np.int8)
    support_blocks=[]; edge_to_support={}
    for e in range(240):
        bs=tuple(map(int,np.where(n[:,e])[0])); assert len(bs)==3
        support_blocks.append(bs)
        for i,j in itertools.combinations(bs,2):
            key=tuple(sorted((i,j))); assert key not in edge_to_support
            edge_to_support[key]=e
    edges=sorted(edge_to_support); assert len(edges)==720
    adj=[[] for _ in range(45)]
    for i,j in edges:adj[i].append(j);adj[j].append(i)
    for x in adj:x.sort()
    parent={0:None}; q=collections.deque([0]); tree=set()
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in parent:
                parent[v]=u;q.append(v);tree.add(tuple(sorted((u,v))))
    assert len(tree)==44
    chords=set(edges)-tree; assert len(chords)==676
    pivots={}
    for e,bs in enumerate(support_blocks):
        tri={tuple(sorted(x)) for x in itertools.combinations(bs,2)}
        choices=sorted(tri&chords); assert choices
        pivots[e]=choices[0]
    assert len(set(pivots.values()))==240
    free=sorted(chords-set(pivots.values())); assert len(free)==436
    manifest={"tree_edges":sorted(map(list,tree)),
              "face_pivot_edges":{str(e):list(pivots[e]) for e in range(240)},
              "free_chord_edges":list(map(list,free))}
    mh=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    classes=(6**436+3*2**436+2*3**436)//6
    return {
      "cell_counts":{"V":45,"E":720,"F":240},
      "face_edges_partition_all_720_edges":True,
      "spanning_tree_edges":44,"chords_after_tree_gauge":676,
      "independent_face_pivots":240,"free_nonabelian_generators":436,
      "fundamental_group":"free group F_436",
      "proof":"Tree gauge sets 44 gains to identity. Every edge lies in one triangular face, so one distinct non-tree edge per face is eliminated by its flatness relation; no relations remain on the other 436 chords.",
      "flat_S3_switching_classes_formula":"(6^436 + 3*2^436 + 2*3^436)/6",
      "flat_S3_switching_classes_decimal":str(classes),
      "flat_S3_switching_classes_digits":len(str(classes)),
      "fixed_length_information_bits":math.ceil(436*math.log2(6)),
      "naive_three_bits_per_generator":1308,
      "enumerative_encoding_saves_bits":1308-math.ceil(436*math.log2(6)),
      "sign_abelianization":"S3 -> C2 gives 2^436 binary classes, exactly the 436-dimensional H1/CSS logical shadow.",
      "manifest_sha256":mh,
      "manifest":manifest
    }
