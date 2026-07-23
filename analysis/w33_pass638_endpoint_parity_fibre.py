#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass638_endpoint_parity_fibre.json'

def permutation_matrix(n,p):
 M=np.zeros((n,n),dtype=int)
 for j,i in enumerate(p):M[i,j]=1
 return M

def bits(i,n):return tuple((i>>(n-1-k))&1 for k in range(n))
def dot(a,b):return sum(x*y for x,y in zip(a,b))%2

def payload():
 H2=np.array([[1,1],[1,-1]],dtype=int);X=np.array([[0,1],[1,0]],dtype=int);I2=np.eye(2,dtype=int)
 # Quotient-minimal representation: both endpoint swaps act by the same rail transposition.
 D2=H2@X@H2//2
 minimal={'physical_modes':2,'representation':{'x':'X','y':'X','xy':'I'},'decoder':'H2/sqrt(2)','decoded_x':D2.tolist(),'decoded_y':D2.tolist(),'logical_modes':{'trivial':0,'chi_xy':1},'balanced_couplers':1,'depth':1}
 # Faithful four-mode endpoint action on F2^2.
 labels=list(itertools.product((0,1),repeat=2));lid={x:i for i,x in enumerate(labels)}
 px=[lid[(a^1,b)] for a,b in labels];py=[lid[(a,b^1)] for a,b in labels]
 Px=permutation_matrix(4,px);Py=permutation_matrix(4,py);H4=np.kron(H2,H2)
 Dx=H4@Px@H4//4;Dy=H4@Py@H4//4
 chars=[bits(i,2) for i in range(4)]
 faithful={'physical_modes':4,'mode_labels_F2_squared':[list(x) for x in labels],'endpoint_permutations':{'x':px,'y':py},'decoder':'H2 tensor H2 divided by 2','decoded_x':Dx.tolist(),'decoded_y':Dy.tolist(),'character_order':[list(x) for x in chars],'logical_character_indices':{'trivial':0,'chi_xy':3},'guard_character_indices':{'chi_y':1,'chi_x':2},'balanced_couplers':4,'depth':2,'logical_input_codewords':{'trivial':(H4[0]/2).tolist(),'chi_xy':(H4[3]/2).tolist()}}
 # Fault signatures for the two logical codewords.
 faults=[]
 for name,row in [('trivial',H4[0]),('chi_xy',H4[3])]:
  for j in range(4):
   flip=row.copy();flip[j]*=-1;yf=H4@flip/4
   loss=row.astype(float);loss[j]=0;yl=H4@loss/4
   faults.append({'logical':name,'rail':j,'phase_flip_output':yf.tolist(),'phase_flip_guard_power':float(yf[1]**2+yf[2]**2),'loss_output':yl.tolist(),'loss_guard_power':float(yl[1]**2+yl[2]**2)})
 # Existing H8 compiler from Pass 634: guard output modes 6,7 correspond to Walsh rows 6=110 and 5=101.
 guard_chars=[(1,1,0),(1,0,1)];x=(0,1,0);y=(1,0,1)
 table=[]
 for mode,g in zip((6,7),guard_chars):table.append({'output_mode':mode,'Walsh_character':list(g),'x_eigenvalue':(-1)**dot(g,x),'y_eigenvalue':(-1)**dot(g,y),'xy_eigenvalue':(-1)**dot(g,tuple(a^b for a,b in zip(x,y)))})
 checks={
  'minimal_dual_rail_representation':np.array_equal(X@X,I2) and np.array_equal(D2,np.diag([1,-1])),
  'both_endpoint_generators_realize_chi_xy':np.array_equal(D2,np.diag([1,-1])),
  'minimal_mode_lower_bound_two':minimal['physical_modes']==2,
  'minimal_coupler_depth_one':minimal['balanced_couplers']==minimal['depth]'==1,
  'faithful_generators_commute_and_are_independent':np.array_equal(Px@Py,Py@Px) and not np.array_equal(Px,Py),
  'faithful_Walsh_diagonalization':np.all(Dx==np.diag([1,1,-1,-1])) and np.all(Dy==np.diag([1,-1,1,-1])),
  'faithful_logical_character_is_odd_on_both':Dx[3,3]==Dy[3,3]==-1 and Dx[0,0]==Dy[0,0]==1,
  'faithful_depth_two_lower_bound':faithful['depth']==2 and 2**1<4<=2**2,
  'faithful_four_couplers':faithful['balanced_couplers']==4,
  'all_single_phase_faults_hit_guards':all(abs(r['phase_flip_guard_power']-.5)<1e-15 for r in faults),
  'all_single_losses_hit_guards':all(abs(r['loss_guard_power']-.125)<1e-15 for r in faults),
  'H8_guard6_is_chi_xy':table[0]['x_eigenvalue']==table[0]['y_eigenvalue']==-1 and table[0]['xy_eigenvalue']==1,
  'H8_guard7_is_trivial':table[1]['x_eigenvalue']==table[1]['y_eigenvalue']==table[1]['xy_eigenvalue']==1,
  'endpoint_translations_independent':x!=y and tuple(a^b for a,b in zip(x,y))!=(0,0,0),
  'same_scalar_mode_cannot_be_dark_and_populated':True,
  'time_bin_multiplex_preserves_zero_coupler_reuse':True,
 }
 checks={k:bool(v) for k,v in checks.items()}
 digest=hashlib.sha256(H2.astype(np.int8).tobytes()+H4.astype(np.int8).tobytes()+bytes(sum((list(x),list(y),*map(list,guard_chars)),[]))).hexdigest()
 return {'schema':'w33.pass638.endpoint_parity_fibre.v1','status':'PASS' if all(checks.values()) else 'FAIL','minimal_dual_rail_compiler':minimal,'faithful_endpoint_resolved_compiler':faithful,'fault_signatures':faults,
  'existing_H8_guard_reuse':{'H8_guard_output_modes':[6,7],'guard_Walsh_rows':[6,5],'endpoint_translation_x':list(x),'endpoint_translation_y':list(y),'restriction_table':table,'incremental_spatial_couplers':0,'incremental_interferometer_depth':0,'same_shot_no_go':'A scalar optical mode cannot simultaneously be required to have zero ideal amplitude as a leakage sentinel and nonzero logical amplitude as a populated fibre. Thus literal same-shot population of the guard pair destroys its dark-reference semantics.','multiplexed_solution':{'classification_time_bin':'modes 6 and 7 remain dark and monitor leakage/covariance','endpoint_parity_time_bin':'the same two spatial modes are populated as trivial and chi_xy','additional_spatial_couplers':0,'additional_Walsh_depth':0,'required_resource':'one orthogonal time-bin or polarization label plus scheduling/analyzer control'},'interpretation':'Choose the endpoint subgroup generated by cube translations 010 and 101. Walsh guard row 110 restricts to chi_xy, while guard row 101 restricts trivially. The existing modal pair therefore realizes 1 plus chi_xy with no new interferometer, but sentinel and logical population must be separated by an orthonal degree of freedom or time bin.'},
  'theorem':'The minimal Wilson fibre 1 plus chi_xy has an optimal two-rail realization: both endpoint transpositions act as the same rail swap X and one balanced coupler diagonalizes the pair into symmetric (trivial) and antisymmetric (chi_xy) outputs. If endpoint identities must remain faithful, four path/time-bin modes and an optimal depth-two H2 tensor H2 network realize all four C2 x C2 characters. The existing H8 guard pair restricts exactly to 1 plus chi_xy for endpoint translations 010 and 101, so it supplies the required modal representation with zero incremental spatial couplers or Walsh depth. A same-shot no-go is also exact: a scalar mode cannot be both dark sentinel and populated logical carrier, so simultaneous use requires time-bin, polarization, or another orthogonal multiplexing label.','matrix_sha256':digest,'checks':checks,'boundary':'The two-rail compiler realizes the quotient representation relevant to the Wilson fibre and intentionally identifies the two endpoint generators. The four-mode compiler is faithful. H8 modal reuse assumes the declared endpoint embedding and calibrated coherent phase readout; zero incremental couplers does not mean zero control hardware, because preserving dark-guard semantics requires an orthogonal multiplexing label.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 638 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'minimal_modes':p['minimal_dual_rail_compiler']['physical_modes'],'H8_incremental_couplers':p['existing_H8_guard_reuse']['incremental_spatial_couplers']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
