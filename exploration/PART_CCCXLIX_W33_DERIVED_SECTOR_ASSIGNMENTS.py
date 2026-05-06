#!/usr/bin/env python3
"""PART CCCXLIX -- W33-Derived Sector Assignment Compiler.

CCCXLVIII registered exact W33 operator sources for the six empirical response
channels.  CCCXLIX derives sector assignments from that registry instead of
using synthetic hypotheses.

Each response channel is encoded by a provenance signature:

    channel -> operator core -> parity/order -> transform class -> trace flag.

From these signatures the compiler derives multiple sector maps:

    core_map:          sectors by operator core G vs G^2
    parity_map:        sectors by odd/first-order vs even/KG algebra
    transform_map:     sectors by algebraic, exponential, resolvent, zeta
    trace_map:         sectors by spectral readout vs traced kernel
    minimal_bridge:    mass/gap geometry sector, G-trace sector, G^2-trace sector

The output is a set of W33-derived sector maps suitable for CCCXLVII model
comparison, plus consistency checks proving they are generated from the operator
registry rather than hand-entered synthetic assignments.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Tuple
ROOT=Path(__file__).resolve().parents[1]
Q=3; K=12; V=40; PHI3=Q*Q+Q+1; PHI4=Q*Q+1; PHI6=Q*Q-Q+1
B=2*V-PHI3; A=(V//2)*PHI6; DELTA=B*B+4*A; M2=Fraction(DELTA,4)
G=((Fraction(B,2),Fraction(A,1)),(Fraction(1,1),Fraction(-B,2)))
I=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)))
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def fs(x): return f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator)
def mm(A,B): return ((A[0][0]*B[0][0]+A[0][1]*B[1][0],A[0][0]*B[0][1]+A[0][1]*B[1][1]),(A[1][0]*B[0][0]+A[1][1]*B[1][0],A[1][0]*B[0][1]+A[1][1]*B[1][1]))
def ms(c,A): return ((c*A[0][0],c*A[0][1]),(c*A[1][0],c*A[1][1]))
def tr(A): return A[0][0]+A[1][1]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def mjson(A): return [[fs(x) for x in row] for row in A]

def provenance_registry() -> Dict[str, Dict[str, Any]]:
    return {
        "mass": {
            "operator_core": "G2",
            "operator_expression": "G^2",
            "order_parity": "even_KG",
            "transform_class": "algebraic_spectral_atom",
            "trace_flag": "spectral_readout",
            "response_formula": "m^2=5049/4",
        },
        "gap": {
            "operator_core": "G",
            "operator_expression": "spec_gap(G)",
            "order_parity": "odd_first_order",
            "transform_class": "algebraic_spectral_gap",
            "trace_flag": "spectral_readout",
            "response_formula": "gap=2m=sqrt(5049)",
        },
        "heat_trace": {
            "operator_core": "G2",
            "operator_expression": "tr(exp(-tau G^2))",
            "order_parity": "even_KG",
            "transform_class": "exponential_kernel",
            "trace_flag": "traced_kernel",
            "response_formula": "H(tau)=2 exp(-(5049/4)tau)",
        },
        "spinor_trace": {
            "operator_core": "G",
            "operator_expression": "tr(exp(tG))",
            "order_parity": "odd_first_order",
            "transform_class": "exponential_kernel",
            "trace_flag": "traced_kernel",
            "response_formula": "T(t)=2 cosh(sqrt(5049)t/2)",
        },
        "resolvent_trace": {
            "operator_core": "G",
            "operator_expression": "tr((sI-G)^-1)",
            "order_parity": "odd_first_order",
            "transform_class": "green_resolvent",
            "trace_flag": "traced_kernel",
            "response_formula": "R(s)=2s/(s^2-5049/4)",
        },
        "zeta": {
            "operator_core": "G2",
            "operator_expression": "tr((G^2)^-p)",
            "order_parity": "even_KG",
            "transform_class": "spectral_zeta",
            "trace_flag": "traced_kernel",
            "response_formula": "zeta_p=2(5049/4)^-p",
        },
    }

def canonical_sector_map(labels: Dict[str,str]) -> Dict[str,int]:
    order=[]
    out={}
    for channel in CHANNELS:
        label=labels[channel]
        if label not in order: order.append(label)
        out[channel]=order.index(label)
    return out

def derive_map(feature: str) -> Dict[str,int]:
    reg=provenance_registry()
    return canonical_sector_map({c:reg[c][feature] for c in CHANNELS})

def derive_minimal_bridge_map() -> Dict[str,int]:
    reg=provenance_registry()
    labels={}
    for c in CHANNELS:
        core=reg[c]["operator_core"]
        traceflag=reg[c]["trace_flag"]
        if traceflag=="spectral_readout":
            labels[c]="geometry_readout"
        elif core=="G":
            labels[c]="first_order_kernel"
        else:
            labels[c]="KG_even_kernel"
    return canonical_sector_map(labels)

def derive_maps() -> Dict[str,Dict[str,Any]]:
    maps={
        "operator_core": {"assignment": derive_map("operator_core"), "rule": "same sector iff channels use the same core operator G or G^2"},
        "order_parity": {"assignment": derive_map("order_parity"), "rule": "same sector iff channels are odd/first-order or even/KG"},
        "transform_class": {"assignment": derive_map("transform_class"), "rule": "same sector iff channels use the same functional transform class"},
        "trace_flag": {"assignment": derive_map("trace_flag"), "rule": "same sector iff channels are spectral readouts or traced kernels"},
        "minimal_bridge": {"assignment": derive_minimal_bridge_map(), "rule": "geometry readout vs first-order traced kernels vs even/KG traced kernels"},
    }
    return maps

def block_signature(assignment: Dict[str,int]) -> Dict[int,List[str]]:
    blocks={}
    for c in CHANNELS:
        blocks.setdefault(assignment[c],[]).append(c)
    return blocks

def count_sectors(assignment: Dict[str,int]) -> int:
    return len(set(assignment.values()))
def response_packet_from_G(tau=0.001,t=0.01,s=100.0,p=2):
    m=math.sqrt(float(M2))
    return {"mass":m,"gap":2*m,"heat_trace":2*math.exp(-float(M2)*tau),"spinor_trace":2*math.cosh(m*t),"resolvent_trace":2*s/(s*s-float(M2)),"zeta":2/(float(M2)**p),"samples":{"tau":tau,"t":t,"s":s,"p":p}}
def anchor_free_scales(packet):
    tau=packet['samples']['tau']; t=packet['samples']['t']; s=packet['samples']['s']; p=packet['samples']['p']
    return {"mass":packet['mass']**2,"gap":(packet['gap']/2)**2,"heat_trace":-math.log(packet['heat_trace']/2)/tau,"spinor_trace":(math.acosh(packet['spinor_trace']/2)/t)**2,"resolvent_trace":s*s-2*s/packet['resolvent_trace'],"zeta":(2/packet['zeta'])**(1/p)}
def map_report() -> Dict[str,Any]:
    maps=derive_maps()
    return {name:{"assignment":data["assignment"],"blocks":block_signature(data["assignment"]),"sector_count":count_sectors(data["assignment"]),"rule":data["rule"]} for name,data in maps.items()}
def build_results():
    checks=[]; reg=provenance_registry(); maps=derive_maps(); G2=mm(G,G); packet=response_packet_from_G(); scales=anchor_free_scales(packet); reports=map_report()
    checks.append(ok('W33 atoms produce B=67',B==67,B))
    checks.append(ok('W33 atoms produce A=140',A==140,A))
    checks.append(ok('M2=5049/4',M2==Fraction(5049,4),fs(M2)))
    checks.append(ok('G^2=M2I',G2==ms(M2,I),mjson(G2)))
    checks.append(ok('registry covers all channels',set(reg.keys())==set(CHANNELS),list(reg.keys())))
    checks.append(ok('operator-core map is derived',maps['operator_core']['assignment']=={'mass':0,'gap':1,'heat_trace':0,'spinor_trace':1,'resolvent_trace':1,'zeta':0},maps['operator_core']['assignment']))
    checks.append(ok('parity map matches core map',maps['order_parity']['assignment']==maps['operator_core']['assignment'],maps['order_parity']['assignment']))
    checks.append(ok('minimal bridge has three sectors',count_sectors(maps['minimal_bridge']['assignment'])==3,maps['minimal_bridge']['assignment']))
    checks.append(ok('transform class has five sectors',count_sectors(maps['transform_class']['assignment'])==5,maps['transform_class']['assignment']))
    checks.append(ok('trace flag has two sectors',count_sectors(maps['trace_flag']['assignment'])==2,maps['trace_flag']['assignment']))
    checks.append(ok('internal response packet recovers M2 in all channels',max(abs(v-float(M2)) for v in scales.values())<1e-9,scales))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXLIX","title":"W33-Derived Sector Assignment Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"w33_generator":{"G":mjson(G),"G_squared":mjson(G2),"trace":fs(tr(G)),"determinant":fs(det(G)),"M2":fs(M2)},"provenance_registry":reg,"derived_sector_maps":reports,"recommended_next_sector_tests":["operator_core","minimal_bridge","transform_class"],"internal_response_packet":packet,"anchor_free_scales":scales,"architecture_upgrade":"CCCXLVIII tied response channels to finite W33 operators. CCCXLIX derives sector assignments directly from operator provenance signatures: core operator, order parity, transform class, trace flag, and a minimal bridge rule.","theorem":"Given the W33 operator-response registry, sector assignments are induced by equivalence relations on operator provenance. The operator-core and parity relations split channels into G and G^2 sectors; the trace relation splits spectral readouts from traced kernels; the transform relation refines by functional calculus; and the minimal bridge map separates geometry readout, first-order kernels, and even/KG kernels.","honesty_boundary":"These sector maps are mathematically derived from the finite operator registry. Selecting which sector map is physically correct still requires empirical comparison or additional W33 representation-theoretic constraints.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXLIX_w33_derived_sector_assignments_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
