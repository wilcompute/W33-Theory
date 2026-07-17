#!/usr/bin/env python3
"""Pass 404: compile the q=3 Heisenberg voltage cover to conflict-free layers."""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_pass404_photonic_voltage_compiler.json"
SCHEDULE=ROOT/"data"/"w33_pass404_photonic_voltage_schedule_q3.json"
def base_coord(q,b):return divmod(b,q)
def mode_id(q,b,z):return b*q+z
def omega(q,u,v):x,y=u;xp,yp=v;return(y*xp-x*yp)%q
def round_robin_odd(n):
 dummy=n;arr=list(range(n+1));rounds=[]
 for _ in range(n):
  pairs=[]
  for i in range((n+1)//2):
   a,b=arr[i],arr[-1-i]
   if dummy not in(a,b):pairs.append(tuple(sorted((a,b))))
  rounds.append(sorted(pairs));arr=[arr[0],arr[-1],*arr[1:-1]]
 return rounds
def compile_schedule(q=3):
 layers=[];all_edges=set()
 for r,pairs in enumerate(round_robin_odd(q*q)):
  couplers=[];matches=[];used=set()
  for a,b in pairs:
   d=omega(q,base_coord(q,a),base_coord(q,b));matches.append({"bases":[a,b],"shift":d})
   for z in range(q):
    i=mode_id(q,a,z);j=mode_id(q,b,(z+d)%q);edge=tuple(sorted((i,j)))
    if i in used or j in used:raise AssertionError("mode conflict")
    used|={i,j};all_edges.add(edge);couplers.append([i,j])
  layers.append({"layer":r,"base_matches":matches,"couplers":couplers,"idle_modes":sorted(set(range(q**3))-used)})
 control=[]
 for b in range(q*q):
  for z in range(q):control.append([mode_id(q,b,z),mode_id(q,b,(z+1)%q)])
 return layers,control,all_edges
def native_edges_direct(q=3):
 edges=set()
 for a in range(q*q):
  for b in range(a+1,q*q):
   d=omega(q,base_coord(q,a),base_coord(q,b))
   for z in range(q):edges.add(tuple(sorted((mode_id(q,a,z),mode_id(q,b,(z+d)%q)))))
 return edges
def build_payload():
 q=3;layers,control,compiled=compile_schedule(q);direct=native_edges_direct(q);counts={}
 for L in layers:
  for m in L["base_matches"]:
   k=tuple(m["bases"]);counts[k]=counts.get(k,0)+1
 checks={"nine_native_layers":len(layers)==9,"four_base_pairs_per_layer":all(len(L["base_matches"])==4 for L in layers),"twelve_mode_couplers_per_layer":all(len(L["couplers"])==12 for L in layers),"no_mode_conflicts":all(len({v for e in L["couplers"] for v in e})==24 and len(L["idle_modes"])==3 for L in layers),"each_K9_edge_once":len(counts)==36 and set(counts.values())=={1},"compiled_edges_equal_native_graph":compiled==direct,"native_edge_count_108":len(compiled)==108,"control_edge_count_27":len(control)==27,"control_is_nine_oriented_triangles":all(sum(e[0]//3==b for e in control)==3 for b in range(9))}
 schedule={"schema":"w33.pass404.photonic_voltage_schedule.q3.v2","q":3,"mode_count":27,"mode_order":"mode_id=3*(3*x+y)+z","native_layers":layers,"magnetic_control":{"couplers":control,"magnitude":"1/sqrt(3)","directed_phase_radians":"+pi/2 from first mode to second"},"hardware_summary":{"native_time_slices":9,"native_parallel_couplers_per_slice":12,"native_coupler_activations":108,"magnetic_triangle_couplers":27,"calibration_triggers":10,"detectors":27},"loss_placeholders":{"native_coupler_insertion_loss_db":None,"magnetic_coupler_insertion_loss_db":None,"switch_loss_db":None,"detector_efficiency":None}}
 st=json.dumps(schedule,indent=2,sort_keys=True)+"\n";sha=hashlib.sha256(st.encode()).hexdigest();p={"schema":"w33.pass404.photonic_voltage_compiler.v2","status":"PASS" if all(checks.values()) else "FAIL","compiler_law":"for base pair u<v, connect (u,z) to (v,z+omega(u,v)); edge-colour K_9 with nine near-perfect matchings","native_hardware":{"layers":9,"base_pairs_per_layer":4,"parallel_mode_couplers_per_layer":12,"total_edges":108,"idle_fibre_per_layer":1},"control_hardware":{"layer":"nine simultaneous magnetic triangles","couplers":27,"magnitude":"1/sqrt(3)","directed_phase":"+pi/2","gate_time":"2*pi/3"},"blinded_choi_protocol":{"physical_experiment_completed":False,"study_type":"compiled_protocol_not_physical_data","blind_labels":{"A7":"native-only","B2":"native-plus-magnetic-control"},"predictions":{"A7":"identity up to omega","B2":"central phase shift up to omega","process_cross_overlap":"0 because Tr(S)=0"},"required_ingestion":"Pass-397 sealed external raw-count bundle"},"schedule_path":"data/w33_pass404_photonic_voltage_schedule_q3.json","schedule_sha256":sha,"checks":checks};canonical=json.dumps(p,sort_keys=True,separators=(",",":")).encode();p["certificate_sha256"]=hashlib.sha256(canonical).hexdigest();return p,st
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ap.add_argument("--output",type=Path,default=OUT);ap.add_argument("--schedule",type=Path,default=SCHEDULE);a=ap.parse_args();p,s=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit("Pass 404 certificate stale")
  if not a.schedule.exists() or a.schedule.read_text()!=s:raise SystemExit("Pass 404 schedule stale")
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text);a.schedule.write_text(s)
 print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"])}));return 0 if p["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
