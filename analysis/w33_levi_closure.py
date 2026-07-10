#!/usr/bin/env python3
"""Exact five-track closure of the binary Levi operator of W(3,3)."""
from __future__ import annotations
from collections import Counter, deque
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import w33_levi_five_frontiers as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_2026_07_10_LEVI_CLOSURE_results.json"


def apply_cols(cols, v):
    out = 0
    while v:
        bit = v & -v
        out ^= cols[bit.bit_length() - 1]
        v ^= bit
    return out


def compose(a, b):
    return tuple(apply_cols(a, col) for col in b)


def group_order(gens, dim):
    identity = tuple(1 << i for i in range(dim))
    seen, queue = {identity}, deque([identity])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = compose(g, x)
            if y not in seen:
                seen.add(y); queue.append(y)
    return len(seen)


def permute(mask, perm):
    out = 0
    while mask:
        bit = mask & -mask; i = bit.bit_length() - 1
        out |= 1 << perm[i]; mask ^= bit
    return out


def invariant_span(seed, gens):
    orbit, queue = {seed}, deque([seed])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = apply_cols(g, x)
            if y not in orbit:
                orbit.add(y); queue.append(y)
    return tuple(base.gf2_row_basis(orbit)), len(orbit)


def restrict(gens, basis):
    tagged = base.tagged_basis(list(basis)); out = []
    for g in gens:
        cols = []
        for v in basis:
            rem, tag = base.coordinates(apply_cols(g, v), tagged)
            assert rem == 0
            cols.append(tag)
        out.append(tuple(cols))
    return out


def orbit_sizes_and_irreducibility(gens, dim):
    visited = bytearray(1 << dim); visited[0] = 1; rows = []
    for seed in range(1, 1 << dim):
        if visited[seed]: continue
        orbit, queue = [], deque([seed]); visited[seed] = 1
        while queue:
            x = queue.popleft(); orbit.append(x)
            for g in gens:
                y = apply_cols(g, x)
                if not visited[y]: visited[y] = 1; queue.append(y)
        rows.append((len(orbit), base.gf2_rank(orbit)))
    return [size for size, _ in rows], all(span == dim for _, span in rows)


def transvections(geom):
    field = base.FiniteField(3)
    pindex = {p:i for i,p in enumerate(geom.points)}
    lindex = {l:i for i,l in enumerate(geom.lines)}
    seeds = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
             (1,1,0,0),(1,0,1,0),(0,1,0,1),(1,1,1,1)]
    pp, lp = [], []
    for v in seeds:
        p = []
        for x in geom.points:
            c = field.symplectic_form(x, v)
            y = field.add_vectors(x, field.scale(c, v))
            p.append(pindex[field.normalize_projective(y)])
        pp.append(p)
        lp.append([lindex[frozenset(p[i] for i in line)] for line in geom.lines])
    return pp, lp


def homology_action(diff, perms):
    image = base.gf2_row_basis(diff)
    hom = base.quotient_basis(base.gf2_nullspace(diff, 40), image)
    tagged = base.tagged_basis(image + hom)
    gens = []
    for perm in perms:
        cols = []
        for rep in hom:
            rem, tag = base.coordinates(permute(rep, perm), tagged); assert rem == 0
            cols.append(tag >> len(image))
        gens.append(tuple(cols))
    return image, hom, gens


def ambient(coord, reps):
    out = 0
    for i, rep in enumerate(reps):
        if (coord >> i) & 1: out ^= rep
    return out


def arf_of_subspace(coord_basis, reps):
    vectors = [ambient(x, reps) for x in coord_basis]
    return sum(base.weight_quadratic(e)*base.weight_quadratic(f)
               for e,f in base.symplectic_pairs(vectors)) & 1


def rank_track():
    prior = json.loads((ROOT/"data/PART_2026_07_10_LEVI_FIVE_FRONTIERS_results.json").read_text())
    rows = prior["tracks"]["1_odd_q_jordan_census"]["orders"]
    checks = {
        "q_3_5_7_9_exact": {r["q"] for r in rows} == {3,5,7,9},
        "all_census_rows_pass": all(r["all_pass"] for r in rows),
        "D3_offdiag_J_checked": all(r["d3_top_is_all_ones_matrix"] and r["d3_bottom_is_all_ones_matrix"] for r in rows),
    }
    return {
        "all_pass": all(checks.values()), "checks": checks,
        "proved_all_odd_q": "D^3=[[0,J],[J,0]] and D^4=0 by the GQ incidence parity argument",
        "rank_lemmas_remaining": {
            "rank_M":"(q(q+1)^2+2)/2", "rank_A_point":"q(q^2+1)/2+1", "rank_A_line":"q^2+1"},
        "derived_if_rank_lemmas_hold":"J4^2 + J3^((q^3+2q^2+q-4)/2) + J1^(q(q-1)^2/2)",
        "scope":"No primary proof of the cross-characteristic rank lemmas was located; they are certified at q=3,5,7,9, not promoted as proved for all odd q."
    }


def module_track(geom):
    pp, lp = transvections(geom)
    _, hp, gp = homology_action(geom.point_adjacency, pp)
    _, hl, gl = homology_action(geom.line_adjacency, lp)
    p_orbits, p_irred = orbit_sizes_and_irreducibility(gp, 8)
    u6, u6_orbit = invariant_span(0xDC1B, gl)
    u14, u14_orbit = invariant_span(0xFF, gl)
    g6, g14 = restrict(gl, u6), restrict(gl, u14)
    o6, ir6 = orbit_sizes_and_irreducibility(g6, 6)
    o14, ir14 = orbit_sizes_and_irreducibility(g14, 14)
    orthogonal = all(base.dot2(ambient(x,hl), ambient(y,hl)) == 0 for x in u6 for y in u14)
    checks = {
        "dimensions_8_6_14": len(hp)==8 and len(u6)==6 and len(u14)==14,
        "faithful_images": group_order(gp,8)==group_order(gl,20)==25920,
        "all_three_irreducible": p_irred and ir6 and ir14,
        "line_direct_sum": base.gf2_rank(list(u6)+list(u14))==20,
        "line_summands_orthogonal": orthogonal,
        "line_summands_minus_type": arf_of_subspace(u6,hl)==arf_of_subspace(u14,hl)==1,
    }
    return {
        "all_pass":all(checks.values()), "checks":checks, "group":"PSp(4,3)", "group_order":25920,
        "decomposition":"H_P + H_L = U8+ orthogonal-sum U6- orthogonal-sum U14-",
        "point":{"dimension":8,"type":"O+_8(2)","orbit_sizes":p_orbits},
        "line":{"dimension":20,"type":"O+_20(2)","summands":[
            {"dimension":6,"type":"O-_6(2)","orbit_sizes":o6,"seed_orbit":u6_orbit,"isotropic_nonzero":27},
            {"dimension":14,"type":"O-_14(2)","orbit_sizes":o14,"seed_orbit":u14_orbit,"isotropic_nonzero":8127}]},
        "embedding":"block action in O+_8(2) x O-_6(2) x O-_14(2) < O+_28(2)"
    }


def levi_apply(geom, p, l):
    return base.gf2_apply(geom.incidence_rows,l), base.gf2_apply(geom.incidence_columns,p)


def selector_track(geom):
    pc, lc = [(1,0)], [(0,1)]
    for _ in range(3): pc.append(levi_apply(geom,*pc[-1])); lc.append(levi_apply(geom,*lc[-1]))
    selector=[[3,68],[4,42],[38,65],[90,144]]; rows=[]
    for s in range(4):
        for rail,chain in (("point_seeded",pc),("line_seeded",lc)):
            p,l=chain[s]; m=p or l
            rows.append({"slot":s,"support_pair":selector[s],"rail":rail,"BT982_column":2*s+(rail=="line_seeded"),
                         "grade":"point" if p else "line","Z40_hex":f"0x{m:010x}","weight":m.bit_count()})
    checks={"both_chains_close":levi_apply(geom,*pc[-1])==(0,0)==levi_apply(geom,*lc[-1]),
            "weights_1_4_12_40":[(p or l).bit_count() for p,l in pc]==[1,4,12,40] and [(p or l).bit_count() for p,l in lc]==[1,4,12,40],
            "eight_control_states":len(rows)==8}
    return {"all_pass":all(checks.values()),"checks":checks,"selector":selector,"rows":rows,
            "mapping":"slot s uses stage s of both J4 rails for BT982 columns 2s and 2s+1",
            "phase":"v -> -v commutes with the integral boundary: D(-v)=-D(v)",
            "scope":"canonical control/payload crosswalk; the J4 span is not identified with E8 homology"}


def gl2():
    return [(a|(c<<1),b|(d<<1)) for a,b,c,d in product(range(2),repeat=4) if (a*d-b*c)%2]

def gmul(a,b): return (apply_cols(a,b[0]),apply_cols(a,b[1]))
def gid(): return (1,2)
def gord(g):
    x=gid()
    for n in range(1,7):
        x=gmul(g,x)
        if x==gid(): return n
    raise AssertionError

def sdmul(x,y,copies):
    vx,gx=x; vy,gy=y; moved=0
    for i in range(copies): moved |= apply_cols(gx,(vy>>(2*i))&3)<<(2*i)
    return vx^moved,gmul(gx,gy)

def order(x,mul,e):
    y=e
    for n in range(1,25):
        y=mul(x,y)
        if y==e:return n
    raise AssertionError

def profile(elements,mul,e): return dict(sorted(Counter(order(x,mul,e) for x in elements).items()))

def group_track():
    s3=gl2(); e=gid(); s4=[(v,g) for v in range(4) for g in s3]; tomo=[(v,g) for v in range(16) for g in s3]
    m4=lambda x,y:sdmul(x,y,1); mt=lambda x,y:sdmul(x,y,2)
    trans=next(g for g in s3 if gord(g)==2); d4=[(v,g) for v in range(4) for g in (e,trans)]
    d12=[(g,z) for g in s3 for z in range(2)]; md=lambda x,y:(gmul(x[0],y[0]),x[1]^y[1])
    sign=lambda g:1 if gord(g)==2 else 0
    g48=[(d,h) for d in d4 for h in d12 if (d[1]!=e)==bool(sign(h[0]))]
    m48=lambda x,y:(m4(x[0],y[0]),md(x[1],y[1])); e48=((0,e),(e,0))
    p_t=profile(tomo,mt,(0,e)); p48=profile(g48,m48,e48)
    p96=profile([(x,z) for x in g48 for z in range(2)],lambda x,y:(m48(x[0],y[0]),x[1]^y[1]),(e48,0))
    fiber={(a,b) for a in s4 for b in s4 if a[1]==b[1]}; image={((v&3,g),((v>>2)&3,g)) for v,g in tomo}
    checks={"tomotope_profile":p_t=={1:1,2:27,3:32,4:36},"fiber_product":fiber==image,
            "local_D4":profile(d4,m4,(0,e))=={1:1,2:5,4:2},"mirror_D12":profile(d12,md,(e,0))=={1:1,2:7,3:2,6:2},
            "runtime_48":len(g48)==48,"two_order96_groups_not_isomorphic":p96!=p_t}
    return {"all_pass":all(checks.values()),"checks":checks,
            "tomotope":{"structure":"(V4+V4):S3 = S4 fiber-product_over_S3 S4","order":96,"profile":p_t},
            "runtime_48":{"structure":"D4 fiber-product_over_C2 D12","profile":p48},
            "phase_doubled_runtime":{"order":96,"profile":p96,"is_tomotope":False,
                                     "separator":"has order-6 elements; tomotope has none"}}


def typed_track():
    import holonet_typed_packet as typed
    k=typed.LeviTypedKernel(); demo=k.demo(); fuzz=k.fuzz(20260710,256)
    checks={"widths_8_20":k.contexts[0].homology_dimension==8 and k.contexts[1].homology_dimension==20,
            "legal_mirror_zero_syndrome":demo["legal_mirror"]["target_syndrome"]==0,
            "raw_retag_rejected":demo["raw_retag"]["rejected"],"fuzz":fuzz["all_pass"]}
    return {"all_pass":all(checks.values()),"checks":checks,"implementation":"analysis/holonet_typed_packet.py",
            "commands":["packet-info","packet-demo","packet-fuzz"],"fuzz":fuzz}


@lru_cache(maxsize=1)
def analyze():
    geom=base.build_geometry(3)
    tracks={"1_rank_proof_boundary":rank_track(),"2_module_decomposition":module_track(geom),
            "3_typed_packet_vm":typed_track(),"4_selector_closure":selector_track(geom),"5_group_bridge":group_track()}
    checks={"all_five_present":len(tracks)==5,"all_five_pass":all(x["all_pass"] for x in tracks.values())}
    return {"status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"tracks":tracks,
            "honest_scope":"D^3/D^4 is proved for all odd q; the three simple binary rank formulas remain exact q=3,5,7,9 theorem targets."}


def main():
    out=analyze(); OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out["status"]=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
