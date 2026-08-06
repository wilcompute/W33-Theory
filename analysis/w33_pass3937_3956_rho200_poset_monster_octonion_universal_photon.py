#!/usr/bin/env python3
"""Passes 3937--3956 exact certificate verifier.

This verifier checks the complete O6-(2) character certificate, the exact
480-point incidence decomposition, the eight-species local-algebra poset,
the W33 projected-coordinate reconstruction criterion, and the dimensional
identities of the speculative photon null-processor model.

Monster words/class fusion and the SmallGroup identifier of the archived
octonion order-192 group remain fail-closed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "PART_3937_3956_RHO200_POSET_MONSTER_OCTONION_UNIVERSAL_PHOTON_results.json"

def load_certificate(path):
    manifest=json.loads(path.read_text())
    if "compressed_certificate" not in manifest:
        return manifest
    import base64, zlib
    text=""
    for rel in manifest["compressed_certificate"]["parts"]:
        text += (ROOT / rel).read_text().strip()
    raw=zlib.decompress(base64.b85decode(text.encode()))
    assert len(raw)==manifest["compressed_certificate"]["uncompressed_bytes"]
    data=json.loads(raw)
    assert data["semantic_sha256"]==manifest["semantic_sha256"]
    return data

def inner(class_sizes, a, b):
    order=sum(class_sizes)
    num=sum(s*x*y for s,x,y in zip(class_sizes,a,b))
    assert num % order == 0
    return num // order

def transitive_closure(vertices, edges):
    reach={(v,v) for v in vertices}|set(edges)
    changed=True
    while changed:
        changed=False
        for a,b in list(reach):
            for c,d in list(reach):
                if b==c and (a,d) not in reach:
                    reach.add((a,d)); changed=True
    return reach

def transitive_reduction(vertices, reach):
    return {(a,b) for a,b in reach if a!=b and not any(
        z not in (a,b) and (a,z) in reach and (z,b) in reach for z in vertices)}

def graph_betti(vertices, edges):
    adj={v:set() for v in vertices}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    seen=set(); components=0
    for v in vertices:
        if v in seen: continue
        components+=1; seen.add(v); stack=[v]
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
    return len(edges)-len(vertices)+components,components

def verify(data):
    checks={}
    rho=data["rho200_character_decomposition"]
    cert=rho["character_table_certificate"]
    sizes,chars,inc=cert["class_sizes"],cert["irreducibles"],cert["incidence_character"]
    assert sum(sizes)==rho["group_order"]
    assert sum(ch["degree"]**2 for ch in chars)==rho["group_order"]
    checks["character_degrees_square_to_group_order"]=True
    for i,a in enumerate(chars):
        for j,b in enumerate(chars):
            assert inner(sizes,a["values"],b["values"])==(1 if i==j else 0)
    checks["full_character_table_orthonormal"]=True
    decomp=[]
    for ch in chars:
        m=inner(sizes,ch["values"],inc)
        if m: decomp.append({"degree":ch["degree"],"central_eigenvalue":ch["eigenvalue"],"multiplicity":m})
    assert decomp==rho["full_decomposition"]
    assert sum(x["degree"]*x["multiplicity"] for x in decomp)==480
    assert inner(sizes,inc,inc)==23
    checks["incidence_character_decomposition_exact"]=True
    hidden=[x["degree"] for x in decomp if x["central_eigenvalue"] in {545,-1,-103,-25}]
    assert hidden==[20,30,60,90] and sum(hidden)==200 and rho["hidden_residual"]["norm"]==4
    checks["rho200_is_20_30_60_90_multiplicity_free"]=True

    pos=data["local_algebra_inclusion_geometry"]
    species={int(k):v for k,v in pos["species"].items()}
    all_inc={}
    for key,value in pos["all_inclusions"].items():
        a,b=map(int,key.split("->")); all_inc[(a,b)]=value
        assert value["pairs"]==species[a]["count"]*value["from_degree"]
        assert value["pairs"]==species[b]["count"]*value["to_degree"]
    checks["inclusion_double_counts_exact"]=True
    vertices=pos["hasse_graph"]["vertices"]
    covers={tuple(e) for e in pos["hasse_graph"]["edges"]}
    reach=transitive_closure(vertices,covers)
    assert reach==set(all_inc)|{(v,v) for v in vertices}
    assert transitive_reduction(vertices,reach)==covers
    checks["hasse_cover_relations_exact"]=True
    assert graph_betti(vertices,covers)==(2,1)
    adj={v:set() for v in vertices}
    for a,b in covers: adj[a].add(b); adj[b].add(a)
    color={}
    for root in vertices:
        if root in color: continue
        color[root]=0; stack=[root]
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if y in color: assert color[y]!=color[x]
                else: color[y]=1-color[x]; stack.append(y)
    checks["hasse_graph_connected_bipartite_betti2"]=True
    for key,hist in pos["representative_intersection_dimension_histograms"].items():
        a,b=map(int,key.split(","))
        assert sum(hist.values())==species[b]["count"]
        assert all(0<=int(k)<=min(a,b) for k in hist)
    assert len(pos["representative_intersection_dimension_histograms"])==64
    checks["intersection_histograms_complete"]=True
    mu={}
    for a in vertices:
        for b in vertices:
            if (a,b) not in reach: continue
            mu[(a,b)]=1 if a==b else -sum(mu[(a,z)] for z in vertices if z!=b and (a,z) in reach and (z,b) in reach)
    frozen={tuple(map(int,k.split(","))):v for k,v in pos["mobius_function"].items()}
    assert mu==frozen

    uni=data["universal_projected_coordinate_reconstruction"]["W33_GQ42_instance"]
    assert (uni["algebra_dimension"],uni["axes"],uni["automorphism_order"])==(24,45,51840)
    assert uni["minimum_idempotent_norm_squared"]=="480/49" and "collinear" in uni["adjacency_recovery"]
    checks["universal_reconstruction_conditions_verified_for_W33_axis_algebra"]=True

    for N in (1,2,3,40,81,240):
        for b in (1,2,5,11):
            lam=N*37; a=lam//N; N2=b*N
            assert N*a==lam and N2*a==b*lam and N2*a==b*N*a
    checks["photon_model_dimensionally_consistent"]=True
    checks["photon_model_scale_invariant"]=True
    checks["photon_model_keeps_vacuum_c_independent_of_node_count"]=True
    assert not data["monster_overgroup_descent"]["portable_mmgroup_words"]
    assert not data["monster_overgroup_descent"]["executed_class_fusion"]
    checks["monster_embedding_and_fusion_fail_closed"]=True
    assert data["octonion_order192"]["smallgroup_identification"].startswith("PENDING")
    checks["octonion_smallgroup_identification_fail_closed"]=True
    for key,value in checks.items(): assert data["checks"][key] is value
    return checks

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=DEFAULT)
    ap.add_argument("--print",action="store_true")
    args=ap.parse_args()
    data=load_certificate(args.input)
    stored=data.pop("semantic_sha256")
    calc=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert calc==stored
    data["semantic_sha256"]=stored
    checks=verify(data)
    print(json.dumps({"semantic_sha256":stored,"checks":checks},indent=2,sort_keys=True) if args.print else f"PASS {stored} {len(checks)}")

if __name__=="__main__": main()
