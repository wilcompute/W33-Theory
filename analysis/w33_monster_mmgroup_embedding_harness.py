"""Fail-closed mmgroup embedding-certificate harness for Passes 3614-3627."""
from __future__ import annotations
import argparse,json
from pathlib import Path
EXPECTED_ORDER=25920
REQUIRED={"mmgroup_generator_integers","generator_orders","relation_orders","class_fusion","independent_image_order"}
def validate_static(cert):
    errors=[]; missing=REQUIRED-set(cert)
    if missing: errors.append(f"missing keys: {sorted(missing)}")
    if cert.get("independent_image_order")!=EXPECTED_ORDER: errors.append("independent image order is not 25920")
    if len(cert.get("mmgroup_generator_integers",[]))<2: errors.append("at least two Monster generators required")
    fusion=cert.get("class_fusion",{})
    for source,target in {"involutions":"2B","order_3":"3B","order_5":"5B"}.items():
        if fusion.get(source)!=target: errors.append(f"documented 5B-type fusion requires {source}->{target}")
    return errors
def validate_mmgroup(cert):
    try: from mmgroup import MM_from_int
    except Exception as exc: return [f"mmgroup unavailable: {exc}"]
    errors=[]; gens=[MM_from_int(int(x)) for x in cert["mmgroup_generator_integers"]]
    observed=[g.order() for g in gens]
    if observed!=cert["generator_orders"]: errors.append(f"generator-order mismatch: {observed}")
    for word,expected in cert.get("relation_orders",{}).items():
        if word=="g0g1": got=(gens[0]*gens[1]).order()
        elif word=="g0g1inv": got=(gens[0]*gens[1]**-1).order()
        else: errors.append(f"unsupported relation {word}"); continue
        if got!=expected: errors.append(f"{word} order {got}, expected {expected}")
    return errors
def main():
    p=argparse.ArgumentParser(); p.add_argument("certificate",type=Path); p.add_argument("--strict-mmgroup",action="store_true"); a=p.parse_args()
    cert=json.loads(a.certificate.read_text()); errors=validate_static(cert); mm_errors=validate_mmgroup(cert)
    if a.strict_mmgroup: errors.extend(mm_errors)
    print(json.dumps({"static_pass":not errors,"mmgroup_diagnostics":mm_errors,"promotable":not errors and not mm_errors,"boundary":"Character-table fusion alone is not a generator-level embedding."},indent=2))
    return int(bool(errors))
if __name__=="__main__": raise SystemExit(main())
