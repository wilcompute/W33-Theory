#!/usr/bin/env python3
"""Fail-closed calibration ingestion for the W33 qutrit optical primitive.

Two evidence classes are intentionally kept separate:

* EXTERNAL_PRIOR_ART_MEASUREMENT: real measurements from published optical
  qudit experiments. They are benchmarks, never W33 hardware calibration.
* W33_DEVICE_MEASUREMENT: a bench packet produced by the actual target device.
  Only this class may replace engineering defaults or satisfy CALIBRATED_DEVICE.

A W33 device packet must bind a device/run identity, measurement digest, sample
count, primitive engineering metrics, directly estimated circuit fault rates,
and explicit coverage of BOTH semantic Clifford classes and the physical
micro-ISA component classes to which they are lowered:

  WEYL_DISPLACEMENT
  TRANSVECTION_QUADRATIC_PHASE
  QUTRIT_FOURIER_MIXER
  QUTRIT_CONTROLLED_ADD

Aggregate fidelity or insertion loss is never reverse-engineered into an
unstated Pauli/leakage model.
"""
from __future__ import annotations

from pathlib import Path
import hashlib,json,math

ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/"data/w33_qutrit_optical_primitive_calibration.json"
PRIOR=ROOT/"data/w33_qutrit_optical_prior_art_benchmark.json"
RATE_KEYS=(
 "ancilla_prep_syndrome_shift","ancilla_readout_syndrome_shift",
 "coupling_ancilla_shift","coupling_data_pauli",
 "coupling_heralded_loss","coupling_unheralded_leakage",
)
METRIC_KEYS=("insertion_loss_db","crosstalk_probability","leakage_probability","phase_rms_rad")
SEMANTIC_PRIMITIVE_KEYS=("WEYL_DISPLACEMENT","TRANSVECTION_QUADRATIC_PHASE")
PHYSICAL_PRIMITIVE_KEYS=("QUTRIT_FOURIER_MIXER","QUTRIT_CONTROLLED_ADD")
PRIMITIVE_KEYS=SEMANTIC_PRIMITIVE_KEYS+PHYSICAL_PRIMITIVE_KEYS

def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"))
def digest(v):return "sha256:"+hashlib.sha256(canonical(v).encode()).hexdigest()
def probability(x):return isinstance(x,(int,float)) and math.isfinite(float(x)) and 0<=float(x)<=1
def nonnegative(x):return isinstance(x,(int,float)) and math.isfinite(float(x)) and float(x)>=0

def prior_art():
    if not PRIOR.exists():return {"present":False,"accepted_for_w33":False}
    try:raw=json.loads(PRIOR.read_text(encoding="utf-8"))
    except Exception as e:return {"present":True,"accepted_for_w33":False,"error":str(e)}
    return {"present":True,"accepted_for_w33":False,"digest":digest(raw),"packet":raw}

def validate_device_packet(raw):
    errors=[]
    if raw.get("schema")!="w33.qutrit-optical-device-calibration.v1":errors.append("SCHEMA")
    if raw.get("evidence_class")!="W33_DEVICE_MEASUREMENT":errors.append("EVIDENCE_CLASS")
    if raw.get("hardware_backed") is not True:errors.append("HARDWARE_BACKED")
    for k in ("device_id","run_id","measurement_digest"):
        if not isinstance(raw.get(k),str) or not raw[k]:errors.append(k.upper())
    if not isinstance(raw.get("sample_count"),int) or raw.get("sample_count",0)<=0:errors.append("SAMPLE_COUNT")
    metrics=raw.get("metrics") if isinstance(raw.get("metrics"),dict) else {}
    for k in METRIC_KEYS:
        if k not in metrics or not nonnegative(metrics.get(k)):errors.append(f"METRIC_{k}")
    rates=raw.get("fault_rates") if isinstance(raw.get("fault_rates"),dict) else {}
    for k in RATE_KEYS:
        if k not in rates or not probability(rates.get(k)):errors.append(f"RATE_{k}")
    coverage=raw.get("primitive_coverage")
    if not isinstance(coverage,list) or any(not isinstance(x,str) or not x for x in coverage):
        errors.append("PRIMITIVE_COVERAGE")
        coverage=[]
    elif len(set(coverage))!=len(coverage):
        errors.append("PRIMITIVE_COVERAGE_DUPLICATE")
    missing=sorted(set(PRIMITIVE_KEYS)-set(coverage))
    if missing:errors.append("PRIMITIVE_COVERAGE_MISSING_"+"_".join(missing))
    if not isinstance(raw.get("fault_model_method"),str) or not raw.get("fault_model_method"):errors.append("FAULT_MODEL_METHOD")
    return {
      "accepted":not errors,
      "errors":errors,
      "rates":{k:float(rates[k]) for k in RATE_KEYS} if not errors else None,
      "metrics":metrics if not errors else None,
      "primitive_coverage":sorted(set(coverage)),
      "required_primitive_coverage":list(PRIMITIVE_KEYS),
      "required_semantic_coverage":list(SEMANTIC_PRIMITIVE_KEYS),
      "required_physical_coverage":list(PHYSICAL_PRIMITIVE_KEYS),
    }

def device_calibration():
    base={
      "path":str(PACKET.relative_to(ROOT)),
      "required_primitive_coverage":list(PRIMITIVE_KEYS),
      "required_semantic_coverage":list(SEMANTIC_PRIMITIVE_KEYS),
      "required_physical_coverage":list(PHYSICAL_PRIMITIVE_KEYS),
    }
    if not PACKET.exists():return {**base,"present":False,"accepted":False,"reason":"W33 device measurement packet absent"}
    try:raw=json.loads(PACKET.read_text(encoding="utf-8"))
    except Exception as e:return {**base,"present":True,"accepted":False,"reason":f"invalid JSON: {e}"}
    v=validate_device_packet(raw)
    return {**base,"present":True,"accepted":bool(v["accepted"]),"packet_digest":digest(raw),"validation":v,"packet":raw}

def rate_source(defaults):
    dev=device_calibration();prior=prior_art()
    if dev.get("accepted"):
        rates=dev["validation"]["rates"]
        return {"source":"W33_DEVICE_MEASUREMENT","hardware_backed":True,"rates":rates,"device":dev,"prior_art":prior}
    return {"source":"ENGINEERING_DEFAULTS","hardware_backed":False,"rates":{k:float(defaults[k]) for k in RATE_KEYS},"device":dev,"prior_art":prior,"reason":"no accepted W33 device measurement with required semantic+physical primitive coverage; external prior art is benchmark-only"}

def calibrated_device():
    dev=device_calibration()
    declared=dev.get("validation",{}).get("primitive_coverage",[]) if isinstance(dev.get("validation"),dict) else []
    return {
      "tier":"CALIBRATED_DEVICE",
      "admissible":bool(dev.get("accepted")),
      "device_packet_digest":dev.get("packet_digest"),
      "required_primitive_coverage":list(PRIMITIVE_KEYS),
      "required_semantic_coverage":list(SEMANTIC_PRIMITIVE_KEYS),
      "required_physical_coverage":list(PHYSICAL_PRIMITIVE_KEYS),
      "declared_primitive_coverage":declared,
      "boundary":"CALIBRATED_DEVICE is reachable only through an accepted W33_DEVICE_MEASUREMENT packet with directly estimated fault rates and all semantic plus physical micro-ISA primitive coverage."
    }

def verify(defaults=None):
    if defaults is None:defaults={k:1e-5 for k in RATE_KEYS}
    src=rate_source(defaults);prior=src["prior_art"];cal=calibrated_device()
    checks={
      "external_prior_art_never_accepted_as_W33_hardware":prior.get("accepted_for_w33") is False,
      "all_effective_rates_are_probabilities":all(probability(src["rates"][k]) for k in RATE_KEYS),
      "hardware_flag_only_for_accepted_device_packet":src["hardware_backed"]==(src["source"]=="W33_DEVICE_MEASUREMENT"),
      "missing_or_invalid_device_packet_fails_closed":src["hardware_backed"] or src["source"]=="ENGINEERING_DEFAULTS",
      "calibrated_device_equals_accepted_measured_packet":cal["admissible"]==bool(src["device"].get("accepted")),
      "calibrated_device_names_all_required_primitives":set(cal["required_primitive_coverage"])==set(PRIMITIVE_KEYS),
      "semantic_and_physical_coverage_are_both_mandatory":set(cal["required_semantic_coverage"])==set(SEMANTIC_PRIMITIVE_KEYS) and set(cal["required_physical_coverage"])==set(PHYSICAL_PRIMITIVE_KEYS),
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {"schema":"w33.qutrit-optical-calibration-ingest.v3","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"effective_rate_source":src,"calibrated_device":cal,"boundary":"Published measurements from other devices can guide engineering expectations but never become W33 hardware evidence. Only a W33_DEVICE_MEASUREMENT packet with directly estimated fault rates and explicit WEYL_DISPLACEMENT, TRANSVECTION_QUADRATIC_PHASE, QUTRIT_FOURIER_MIXER, and QUTRIT_CONTROLLED_ADD coverage can reach CALIBRATED_DEVICE."}
if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
