#!/usr/bin/env python3
"""Pass 397: sealed laboratory ingestion for the Choi-visibility protocol.

The production CLI has no synthetic fallback. It accepts caller-supplied files
through three ordered stages: seal, analyze, and unblind. A separately gated
contract-test uses an explicit nonclaim fixture and can never emit a physical
claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_GATES = {"I":1.0,"X":0.0,"Z":0.0,"F3":1.0/3.0}
EXPECTED_PHASES = [0.0,math.pi/2.0,math.pi,3.0*math.pi/2.0]
SCHEMA_VERSION = "w33.photonic.sealed-lab.v1"


class ContractError(ValueError):
    pass


def load_bytes(path:Path)->bytes:
    if not path.is_file():
        raise ContractError(f"missing required file: {path}")
    return path.read_bytes()


def sha256_bytes(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload:object)->bytes:
    return (json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n").encode()


def write_json(path:Path,payload:object)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(canonical_json(payload))


def read_json(path:Path)->dict[str,Any]:
    try:
        payload=json.loads(load_bytes(path))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload,dict):
        raise ContractError(f"top-level JSON must be an object: {path}")
    return payload


def parse_time(value:Any,field:str)->datetime:
    if not isinstance(value,str):
        raise ContractError(f"{field} must be an ISO-8601 string")
    try:
        parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError as exc:
        raise ContractError(f"invalid timestamp {field}: {value}") from exc
    if parsed.tzinfo is None:
        raise ContractError(f"timestamp {field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def require_keys(payload,keys,label):
    missing=sorted(set(keys).difference(payload))
    if missing:
        raise ContractError(f"{label} missing keys: {missing}")


def validate_raw(payload:dict[str,Any],test_mode:bool)->dict[str,Any]:
    require_keys(payload,{"schema","study_type","blinded","gate_labels_present","acquisition_started_at","acquisition_completed_at","device_id","phases_radians","rows"},"raw counts")
    if payload["schema"]!=SCHEMA_VERSION+".raw-counts":
        raise ContractError("raw-count schema mismatch")
    allowed="nonclaim_test_fixture" if test_mode else "physical_lab_raw_counts_v1"
    if payload["study_type"]!=allowed:
        raise ContractError(f"raw study_type must be {allowed!r}; no synthetic production fallback")
    if payload["blinded"] is not True or payload["gate_labels_present"] is not False:
        raise ContractError("raw counts must be blinded and contain no gate labels")
    started=parse_time(payload["acquisition_started_at"],"acquisition_started_at")
    completed=parse_time(payload["acquisition_completed_at"],"acquisition_completed_at")
    if completed<started:
        raise ContractError("acquisition completion precedes start")
    phases=[float(v) for v in payload["phases_radians"]]
    if len(phases)!=4 or any(abs(a-b)>1e-12 for a,b in zip(phases,EXPECTED_PHASES)):
        raise ContractError("exact four-phase schedule required")
    rows=payload["rows"]
    if not isinstance(rows,list) or not rows:
        raise ContractError("raw rows must be nonempty")
    codes=set(); groups={}
    for number,row in enumerate(rows):
        require_keys(row,{"blind_gate_code","replicate","phase_index","phase_radians","shots","count_port0","count_port1"},f"raw row {number}")
        if "gate" in row or "gate_label" in row:
            raise ContractError(f"raw row {number} leaks a gate label")
        code=row["blind_gate_code"]
        replicate=int(row["replicate"]); phase_index=int(row["phase_index"])
        shots=int(row["shots"]); count0=int(row["count_port0"]); count1=int(row["count_port1"])
        if phase_index not in range(4) or abs(float(row["phase_radians"])-phases[phase_index])>1e-12:
            raise ContractError(f"raw row {number} phase mismatch")
        if shots<=0 or count0<0 or count1<0 or count0+count1!=shots:
            raise ContractError(f"raw row {number} count conservation failure")
        codes.add(code); groups.setdefault((code,replicate),set()).add(phase_index)
    if len(codes)!=4 or any(indices!={0,1,2,3} for indices in groups.values()):
        raise ContractError("four codes and four phases per replicate required")
    replicate_sets={code:{r for candidate,r in groups if candidate==code} for code in codes}
    if len({tuple(sorted(v)) for v in replicate_sets.values()})!=1:
        raise ContractError("all codes must use the same replicate indices")
    return {"codes":sorted(codes),"replicates":len(next(iter(replicate_sets.values()))),"rows":len(rows),"started":started.isoformat(),"completed":completed.isoformat()}


def validate_calibration(payload:dict[str,Any],test_mode:bool)->dict[str,Any]:
    require_keys(payload,{"schema","study_type","calibrated_at","device_id","mode_overlap","non_dark_fraction","method","operator"},"calibration")
    if payload["schema"]!=SCHEMA_VERSION+".calibration":
        raise ContractError("calibration schema mismatch")
    allowed="nonclaim_test_fixture" if test_mode else "physical_lab_calibration_v1"
    if payload["study_type"]!=allowed:
        raise ContractError(f"calibration study_type must be {allowed!r}")
    calibrated=parse_time(payload["calibrated_at"],"calibrated_at")
    overlap=float(payload["mode_overlap"]); non_dark=float(payload["non_dark_fraction"])
    if not (0<overlap<=1 and 0<non_dark<=1):
        raise ContractError("calibration fractions must lie in (0,1]")
    return {"calibrated_at":calibrated.isoformat(),"visibility_dilution_eta":overlap*non_dark}


def file_record(path:Path)->dict[str,Any]:
    data=load_bytes(path)
    return {"path":path.name,"sha256":sha256_bytes(data),"size_bytes":len(data)}


def verify_record(path:Path,record,label):
    data=load_bytes(path)
    if len(data)!=int(record["size_bytes"]) or sha256_bytes(data)!=record["sha256"]:
        raise ContractError(f"{label} hash/size drift")


def seal_bundle(raw_path,calibration_path,output,protocol_frozen_at,test_mode):
    raw=read_json(raw_path); calibration=read_json(calibration_path)
    raw_meta=validate_raw(raw,test_mode); calibration_meta=validate_calibration(calibration,test_mode)
    if raw["device_id"]!=calibration["device_id"]:
        raise ContractError("raw and calibration device IDs differ")
    frozen=parse_time(protocol_frozen_at,"protocol_frozen_at")
    if frozen>parse_time(raw["acquisition_started_at"],"acquisition_started_at"):
        raise ContractError("protocol must be frozen before acquisition")
    manifest={"schema":SCHEMA_VERSION+".manifest","pass":397,"test_mode":test_mode,"claim_eligible":False,"protocol_frozen_at":frozen.isoformat(),"device_id":raw["device_id"],"raw_counts":file_record(raw_path),"calibration":file_record(calibration_path),"raw_metadata":raw_meta,"calibration_metadata":calibration_meta,"stage":"sealed_before_analysis"}
    manifest["manifest_sha256"]=sha256_bytes(canonical_json(manifest))
    write_json(output,manifest); return manifest


def analyze_counts(raw,eta):
    grouped={}
    for row in raw["rows"]:
        grouped.setdefault(row["blind_gate_code"],{}).setdefault(int(row["replicate"]),[]).append(row)
    result={}
    for code,replicates in sorted(grouped.items()):
        visibility=[]; quadrature=[]
        for rows in replicates.values():
            ordered=sorted(rows,key=lambda row:int(row["phase_index"]))
            y=[2*int(row["count_port0"])/int(row["shots"])-1 for row in ordered]
            cosine=[math.cos(float(row["phase_radians"])) for row in ordered]
            sine=[math.sin(float(row["phase_radians"])) for row in ordered]
            a=sum(v*b for v,b in zip(y,cosine))/sum(b*b for b in cosine)
            b=sum(v*s for v,s in zip(y,sine))/sum(s*s for s in sine)
            visibility.append(a/eta); quadrature.append(b/eta)
        mean=statistics.fmean(visibility); se=statistics.stdev(visibility)/math.sqrt(len(visibility)) if len(visibility)>1 else 0
        qmean=statistics.fmean(quadrature); qse=statistics.stdev(quadrature)/math.sqrt(len(quadrature)) if len(quadrature)>1 else 0
        result[code]={"visibility_corrected_mean":mean,"visibility_standard_error":se,"visibility_ci95":[mean-1.96*se,mean+1.96*se],"sine_quadrature_mean":qmean,"sine_quadrature_standard_error":qse,"replicate_estimates":visibility}
    return result


def analyze_bundle(manifest_path,raw_path,calibration_path,output,completed_at,test_mode):
    manifest=read_json(manifest_path)
    if manifest.get("schema")!=SCHEMA_VERSION+".manifest" or bool(manifest.get("test_mode"))!=test_mode:
        raise ContractError("manifest schema/test-mode mismatch")
    verify_record(raw_path,manifest["raw_counts"],"raw counts"); verify_record(calibration_path,manifest["calibration"],"calibration")
    raw=read_json(raw_path); calibration=read_json(calibration_path)
    validate_raw(raw,test_mode); meta=validate_calibration(calibration,test_mode)
    completed=parse_time(completed_at,"analysis_completed_at")
    if completed<parse_time(raw["acquisition_completed_at"],"acquisition_completed_at"):
        raise ContractError("analysis completion precedes acquisition")
    payload={"schema":SCHEMA_VERSION+".blinded-analysis","pass":397,"test_mode":test_mode,"claim_eligible":False,"manifest_sha256":sha256_bytes(load_bytes(manifest_path)),"raw_counts_sha256":manifest["raw_counts"]["sha256"],"calibration_sha256":manifest["calibration"]["sha256"],"analysis_completed_at":completed.isoformat(),"gate_labels_present":False,"analysis_by_blind_code":analyze_counts(raw,float(meta["visibility_dilution_eta"])),"stage":"blinded_analysis_frozen"}
    payload["analysis_sha256"]=sha256_bytes(canonical_json(payload)); write_json(output,payload); return payload


def validate_key(payload,test_mode):
    require_keys(payload,{"schema","study_type","key_frozen_at","key_revealed_at","mapping","custodian"},"blind key")
    if payload["schema"]!=SCHEMA_VERSION+".blind-key":
        raise ContractError("blind-key schema mismatch")
    allowed="nonclaim_test_fixture" if test_mode else "physical_lab_blind_key_v1"
    if payload["study_type"]!=allowed:
        raise ContractError(f"blind-key study_type must be {allowed!r}")
    frozen=parse_time(payload["key_frozen_at"],"key_frozen_at"); revealed=parse_time(payload["key_revealed_at"],"key_revealed_at")
    if revealed<frozen or not isinstance(payload["mapping"],dict) or set(payload["mapping"].values())!=set(ALLOWED_GATES):
        raise ContractError("invalid blind-key timing or mapping")
    return {"frozen":frozen,"revealed":revealed,"mapping":payload["mapping"]}


def unblind_bundle(manifest_path,raw_path,calibration_path,analysis_path,key_path,output,test_mode):
    manifest=read_json(manifest_path); analysis=read_json(analysis_path); key=read_json(key_path)
    if bool(manifest.get("test_mode"))!=test_mode or bool(analysis.get("test_mode"))!=test_mode:
        raise ContractError("test-mode mismatch")
    verify_record(raw_path,manifest["raw_counts"],"raw counts"); verify_record(calibration_path,manifest["calibration"],"calibration")
    if analysis.get("manifest_sha256")!=sha256_bytes(load_bytes(manifest_path)):
        raise ContractError("analysis points to a different manifest")
    key_meta=validate_key(key,test_mode); raw=read_json(raw_path); validate_raw(raw,test_mode)
    if key_meta["frozen"]>parse_time(raw["acquisition_started_at"],"acquisition_started_at"):
        raise ContractError("key was not frozen before acquisition")
    if key_meta["revealed"]<parse_time(analysis["analysis_completed_at"],"analysis_completed_at"):
        raise ContractError("key was revealed before blinded analysis froze")
    if set(key_meta["mapping"])!=set(analysis["analysis_by_blind_code"]):
        raise ContractError("key codes do not match analysis")
    results={gate:{"blind_gate_code":code,"target_visibility":ALLOWED_GATES[gate],**analysis["analysis_by_blind_code"][code]} for code,gate in key_meta["mapping"].items()}
    payload={"schema":SCHEMA_VERSION+".unblinded-result","pass":397,"test_mode":test_mode,"claim_eligible":not test_mode,"physical_experiment_completed":not test_mode,"manifest_sha256":sha256_bytes(load_bytes(manifest_path)),"blinded_analysis_sha256":sha256_bytes(load_bytes(analysis_path)),"blind_key_sha256":sha256_bytes(load_bytes(key_path)),"unblinded_results":results,"stage":"unblinded_hash_locked","scope":"Passing this contract establishes ordering and integrity, not apparatus validity or physical interpretation."}
    payload["result_sha256"]=sha256_bytes(canonical_json(payload)); write_json(output,payload); return payload


def make_fixture(root):
    rows=[]; codes=["A7","B2","C9","D4"]
    for ci,code in enumerate(codes):
        for replicate in range(3):
            for phase_index,phase in enumerate(EXPECTED_PHASES):
                shots=100; count0=50+((ci+replicate+phase_index)%5-2)
                rows.append({"blind_gate_code":code,"replicate":replicate,"phase_index":phase_index,"phase_radians":phase,"shots":shots,"count_port0":count0,"count_port1":shots-count0})
    raw={"schema":SCHEMA_VERSION+".raw-counts","study_type":"nonclaim_test_fixture","blinded":True,"gate_labels_present":False,"acquisition_started_at":"2026-07-17T12:00:00-04:00","acquisition_completed_at":"2026-07-17T12:10:00-04:00","device_id":"TEST-DEVICE-NOT-PHYSICAL","phases_radians":EXPECTED_PHASES,"rows":rows}
    calibration={"schema":SCHEMA_VERSION+".calibration","study_type":"nonclaim_test_fixture","calibrated_at":"2026-07-17T11:30:00-04:00","device_id":"TEST-DEVICE-NOT-PHYSICAL","mode_overlap":0.96,"non_dark_fraction":0.98,"method":"contract-test-only","operator":"automated-fixture"}
    key={"schema":SCHEMA_VERSION+".blind-key","study_type":"nonclaim_test_fixture","key_frozen_at":"2026-07-17T11:50:00-04:00","key_revealed_at":"2026-07-17T12:30:00-04:00","mapping":{"A7":"X","B2":"F3","C9":"I","D4":"Z"},"custodian":"contract-test-only"}
    paths=[root/"raw.json",root/"calibration.json",root/"key.json"]
    for path,payload in zip(paths,[raw,calibration,key]): write_json(path,payload)
    return paths


def contract_test(output):
    checks={}
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary); raw,calibration,key=make_fixture(root)
        manifest=root/"manifest.json"; blinded=root/"blinded.json"; result=root/"result.json"
        seal_bundle(raw,calibration,manifest,"2026-07-17T11:00:00-04:00",True)
        analyze_bundle(manifest,raw,calibration,blinded,"2026-07-17T12:20:00-04:00",True)
        final=unblind_bundle(manifest,raw,calibration,blinded,key,result,True)
        checks["full_explicit_test_mode_pipeline_passes"]=final["claim_eligible"] is False
        checks["test_mode_cannot_claim_physical_completion"]=final["physical_experiment_completed"] is False
        try: seal_bundle(raw,calibration,root/"bad.json","2026-07-17T11:00:00-04:00",False)
        except ContractError: checks["production_rejects_nonclaim_fixture"]=True
        else: checks["production_rejects_nonclaim_fixture"]=False
        original=raw.read_bytes(); raw.write_bytes(original+b" ")
        try: analyze_bundle(manifest,raw,calibration,root/"tampered.json","2026-07-17T12:20:00-04:00",True)
        except ContractError: checks["tamper_after_seal_is_detected"]=True
        else: checks["tamper_after_seal_is_detected"]=False
        raw.write_bytes(original)
        premature=read_json(key); premature["key_revealed_at"]="2026-07-17T12:15:00-04:00"; premature_path=root/"premature.json"; write_json(premature_path,premature)
        try: unblind_bundle(manifest,raw,calibration,blinded,premature_path,root/"out.json",True)
        except ContractError: checks["premature_key_reveal_is_detected"]=True
        else: checks["premature_key_reveal_is_detected"]=False
    payload={"pass":397,"title":"Sealed laboratory ingestion contract","status":"PASS" if all(checks.values()) else "FAIL","production_has_synthetic_fallback":False,"production_stages":["seal","analyze","unblind"],"contract_test_uses_nonclaim_fixture":True,"checks":checks}
    payload["certificate_sha256"]=sha256_bytes(canonical_json(payload)); write_json(output,payload); return payload


def parser():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="command",required=True)
    s=sub.add_parser("seal"); s.add_argument("--raw",type=Path,required=True); s.add_argument("--calibration",type=Path,required=True); s.add_argument("--output",type=Path,required=True); s.add_argument("--protocol-frozen-at",required=True); s.add_argument("--test-mode",action="store_true")
    a=sub.add_parser("analyze"); a.add_argument("--manifest",type=Path,required=True); a.add_argument("--raw",type=Path,required=True); a.add_argument("--calibration",type=Path,required=True); a.add_argument("--output",type=Path,required=True); a.add_argument("--completed-at",required=True); a.add_argument("--test-mode",action="store_true")
    u=sub.add_parser("unblind"); u.add_argument("--manifest",type=Path,required=True); u.add_argument("--raw",type=Path,required=True); u.add_argument("--calibration",type=Path,required=True); u.add_argument("--blinded-analysis",type=Path,required=True); u.add_argument("--key",type=Path,required=True); u.add_argument("--output",type=Path,required=True); u.add_argument("--test-mode",action="store_true")
    t=sub.add_parser("contract-test"); t.add_argument("--output",type=Path,default=Path("data/w33_pass397_sealed_lab_ingestion_contract.json")); t.add_argument("--check",action="store_true")
    return p


def main():
    args=parser().parse_args()
    if args.command=="seal": payload=seal_bundle(args.raw,args.calibration,args.output,args.protocol_frozen_at,args.test_mode)
    elif args.command=="analyze": payload=analyze_bundle(args.manifest,args.raw,args.calibration,args.output,args.completed_at,args.test_mode)
    elif args.command=="unblind": payload=unblind_bundle(args.manifest,args.raw,args.calibration,args.blinded_analysis,args.key,args.output,args.test_mode)
    elif args.check:
        with tempfile.TemporaryDirectory() as temporary:
            generated=Path(temporary)/"contract.json"; payload=contract_test(generated)
            if not args.output.exists() or args.output.read_bytes()!=generated.read_bytes(): raise SystemExit("Pass 397 certificate drift")
    else: payload=contract_test(args.output)
    print(json.dumps({"stage":payload.get("stage","contract-test"),"status":payload.get("status","PASS"),"claim_eligible":payload.get("claim_eligible",False)}))


if __name__=="__main__":
    main()
