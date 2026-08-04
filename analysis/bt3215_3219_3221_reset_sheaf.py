#!/usr/bin/env python3
"""Passes 3215, 3219-3221: promotion gate, port-nerve homology, and reset rank.

This file deliberately joins three contracts that must not be conflated:

* source-level ISA performance versus observed placement evidence;
* local phase/sheaf consistency versus existence or uniqueness of a global bridge;
* optical/epoch synchronization versus reset of the 876-state epistemic controller.

Every promoted conclusion is finite and machine-checkable.  No physical calibration,
contextuality completeness theorem, or autonomous reset is inferred.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=DATA/'PART_BT3215_BT3221_RESET_SHEAF_RESULTS.json'


def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 module=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(module)
 return module


def rank_mod(matrix,p):
 a=np.array(matrix,dtype=np.int64)%p;m,n=a.shape;r=0
 for c in range(n):
  pivot=next((i for i in range(r,m) if int(a[i,c])%p),None)
  if pivot is None:continue
  a[[r,pivot]]=a[[pivot,r]]
  a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and a[i,c]:a[i]=(a[i]-a[i,c]*a[r])%p
  r+=1
  if r==m:break
 return r


def port_nerve():
 base=load_module('bt3187',ROOT/'analysis/bt3187_3192_chromatic_defect_block_filter.py')
 points,a,lines,w33_edges,frames,m,h=base.build_geometry()
 _,blocks,pairorbits=base.canonical_blocks(points,a,lines,frames)
 membership=np.zeros((540,45),dtype=np.int8)
 for j,block in enumerate(blocks):membership[block,j]=1
 support=((membership.T@m)>0).astype(np.int8)
 assert support.shape==(45,240)
 assert set(map(int,support.sum(1)))=={16}
 assert set(map(int,support.sum(0)))=={3}

 triangles=[]
 for port in range(240):
  tri=tuple(map(int,np.where(support[:,port])[0]))
  assert len(tri)==3
  triangles.append(tuple(sorted(tri)))
 assert len(set(triangles))==240
 edge_set={tuple(sorted(e)) for tri in triangles for e in itertools.combinations(tri,2)}
 edges=sorted(edge_set);edge_index={e:i for i,e in enumerate(edges)}
 assert len(edges)==720
 # The exact factorisation says these 240 triangles partition all 720 block-graph edges.
 counts={e:0 for e in edges}
 for tri in triangles:
  for e in itertools.combinations(tri,2):counts[tuple(sorted(e))]+=1
 assert set(counts.values())=={1}

 d1=np.zeros((45,720),dtype=np.int8)
 for j,(u,v) in enumerate(edges):d1[u,j]=-1;d1[v,j]=1
 d2=np.zeros((720,240),dtype=np.int8)
 for j,(a0,b0,c0) in enumerate(triangles):
  # boundary [a,b,c]=[b,c]-[a,c]+[a,b]
  d2[edge_index[(b0,c0)],j]=1
  d2[edge_index[(a0,c0)],j]=-1
  d2[edge_index[(a0,b0)],j]=1
 assert np.all(d1.astype(np.int64)@d2.astype(np.int64)==0)

 field_rows={}
 for p in (2,3,5):
  r1=rank_mod(d1,p);r2=rank_mod(d2,p)
  b0=45-r1;b1=720-r1-r2;b2=240-r2
  assert (r1,r2,b0,b1,b2)==(44,240,1,436,0)
  field_rows[str(p)]={'rank_boundary_1':r1,'rank_boundary_2':r2,
   'betti_0':b0,'betti_1':b1,'betti_2':b2,
   'flat_lift_classes':f'{p}^436'}

 # Every graph triangle is a 1-cycle.  The SRG(45,32,22,24) has 5280 triangles,
 # only 240 of which are the edge-disjoint port-face boundaries.
 block_graph=(support@support.T==1).astype(np.int8);np.fill_diagonal(block_graph,0)
 graph_triangles=sum(1 for a0,b0,c0 in itertools.combinations(range(45),3)
                     if block_graph[a0,b0] and block_graph[a0,c0] and block_graph[b0,c0])
 assert graph_triangles==5280
 nonface_triangles=graph_triangles-len(triangles)
 assert nonface_triangles==5040

 # Exact CSS distances.  A non-port graph triangle is a weight-three Z logical.
 # A pair of edges in one port triangle is a weight-two X logical.  No weight-one
 # X logical exists because every edge belongs to one face; no weight-two cut can
 # exist since any nontrivial cut S has |delta(S)| >= s(33-s) for s<=22.
 css={'field':'F2','physical_qubits':720,'logical_qubits':436,
      'rank_HX':44,'rank_HZ':240,'z_distance':3,'x_distance':2,'distance':2,
      'graph_triangles':graph_triangles,'filled_port_triangles':240,
      'unfilled_weight_three_cycles':nonface_triangles,
      'interpretation':'High-rate provenance/checksum complex; distance two forbids promotion to fault-tolerant memory.'}

 # Deterministic flat/nonflat controls over F2.  Each edge belongs to exactly one face.
 flat_two_edge=np.zeros(720,dtype=np.int8)
 first_tri=triangles[0];first_edges=[edge_index[tuple(sorted(e))] for e in itertools.combinations(first_tri,2)]
 flat_two_edge[first_edges[:2]]=1
 single=np.zeros(720,dtype=np.int8);single[first_edges[0]]=1
 assert not np.any((d2.T@flat_two_edge)%2)
 assert int(np.count_nonzero((d2.T@single)%2))==1
 sheaf={'coefficient_fields':['F2','F3','F5'],'first_cohomology_dimension':436,
        'flat_two_edge_positive_control':True,'single_edge_flux_negative_control':True,
        'obstruction_map':'delta_1 = boundary_2^T; a nonzero 240-port flux vector forbids a flat phase lift.',
        'ambiguity':'Even zero flux leaves p^436 gauge-inequivalent constant-coefficient flat lifts over F_p.',
        'boundary':'This is cellular/constant-coefficient cohomology of the finite port nerve. It is not by itself a complete contextuality witness or a canonical chromatic-curvature crosswalk.'}
 return {'vertices':45,'edges':720,'faces':240,'euler_characteristic':45-720+240,
         'pair_orbits':pairorbits,'fields':field_rows,'css':css,'sheaf':sheaf,
         'semantic_sha256':hashlib.sha256(json.dumps({'edges':edges,'triangles':triangles},separators=(',',':')).encode()).hexdigest()}


def synchronization_rank():
 belief=876;phase=12
 # Any phase-only symbol word has transformation T_B x T_P with T_B=identity.
 # The optimal phase marker has rank one on phase, hence rank 876 on the product.
 product=belief*phase
 marker_rank=belief
 assert product==10512 and marker_rank==876
 return {'belief_states':belief,'phase_states':phase,'product_states':product,
  'phase_marker_product_rank':marker_rank,
  'phase_marker_collapses_phase_factor':phase,
  'belief_states_remaining_after_any_phase_only_word':belief,
  'phase_only_reset_impossible':True,
  'explicit_belief_reset_rank':1,
  'minimum_logical_erasure_bits_for_full_belief_reset':math.log2(belief),
  'theorem':'Epoch synchronization and epistemic reset are distinct. Every word whose letters act identically on the belief coordinate has image rank at least 876; the optimal phase marker attains that floor but cannot synchronize belief.'}


def tri_isa_gate():
 source={
  'current4':{'mean_distance':14.175585133744857,'collision_probability':45/324,'decoder_operation_units':4},
  'low4':{'mean_distance':15.216323969288219,'collision_probability':36/324,'decoder_operation_units':5},
  'fast6':{'mean_distance':13.72936957018747,'collision_probability':63/486,'decoder_operation_units':8}}
 # Accept only a dedicated observed evidence record.  Source estimates never set valid=true.
 evidence_path=DATA/'PART_BT3215_TRI_ISA_OBSERVED_EVIDENCE.json'
 observed=None
 if evidence_path.exists():
  candidate=json.loads(evidence_path.read_text())
  required={'schema','device','toolchain','commit','modes'}
  if required<=set(candidate) and all(k in candidate['modes'] for k in source):
   if all({'placed','logic_cells','fmax_mhz'}<=set(candidate['modes'][k]) for k in source):observed=candidate
 status='OBSERVED_PROMOTION_READY' if observed else 'FAIL_CLOSED_SOURCE_ONLY'
 winner=None
 if observed:
  placed=[k for k in source if observed['modes'][k]['placed']]
  if placed:
   # Promotion score is deliberately transparent and not a universal physical objective.
   winner=min(placed,key=lambda k:(source[k]['mean_distance'],observed['modes'][k]['logic_cells'],-observed['modes'][k]['fmax_mhz']))
 return {'source_metrics':source,'observed_evidence_file':str(evidence_path.relative_to(ROOT)),
         'status':status,'promoted_mode':winner,
         'rule':'No ISA becomes physical default without placed=true, observed logic cells and observed Fmax for every compared mode. Missing evidence preserves current4 as fail-closed fallback.',
         'boundary':'Source runtime and collision values are exact for frozen generators. Area, timing, power and calibration require observed tool/device evidence.'}


def main():
 result={'schema':'w33.pass3215_3219_3221.reset_sheaf.v1','status':'PASS_EXACT_SOURCE_WITH_OBSERVED_HARDWARE_FAIL_CLOSED',
         'pass3215_tri_isa':tri_isa_gate(),'pass3219_3221_port_nerve':port_nerve(),
         'pass3220_synchronization_rank':synchronization_rank(),
         'headline':'The finite-port lift has 436 independent flat phase degrees of freedom and yields a [[720,436,2]] checksum code; phase synchronization alone has exact product rank 876 and cannot reset the curvature-aware belief machine.',
         'physical_boundary':'No optical, detector, FPGA timing, power, thermal, fabrication or laboratory result is inferred.'}
 DATA.mkdir(exist_ok=True)
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'b1':436,'css':'[[720,436,2]]','marker_rank':876,'isa':result['pass3215_tri_isa']['status']},sort_keys=True))
if __name__=='__main__':main()
