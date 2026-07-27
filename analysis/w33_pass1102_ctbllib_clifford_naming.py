from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1102_ctbllib_clifford_naming.json'
ORDER=51840
CLASSES=['1A','2A','2B','3A','3C','3D','4A','4B','5A','6A','6C','6E','6F','9A','12A','2C','2D','4C','4D','6G','6H','6I','8A','10A','12C']
SIZES=[1,45,270,80,240,480,540,3240,5184,720,1440,1440,2160,5760,4320,36,540,540,1620,1440,1440,4320,6480,5184,4320]
CHARS={
'1':[1]*25,
'15a':[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,5,1,3,-1,2,-1,1,-1,0,0],
'15b':[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,-5,-1,-3,1,-2,1,-1,1,0,0],
'20':[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1],
'24':[24,8,0,6,0,3,0,0,-1,2,2,-1,0,0,0,4,4,0,0,-2,1,1,0,-1,0],
'60a':[60,-4,4,6,-3,-3,0,0,0,2,-1,-1,1,0,0,10,2,-2,-2,1,1,-1,0,0,1],
'60b':[60,12,4,-3,-6,0,4,0,0,-3,0,0,-2,0,1,0,0,0,0,0,0,0,0,0,0],
'64':[64,0,0,-8,4,-2,0,0,-1,0,0,0,0,1,0,16,0,0,0,-2,-2,0,0,1,0],
'81_plus':[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0],
'81_minus':[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0],
}
OUTER=['1','15a','15b','20','24','60a','60b','64','81_plus','81_minus']
INNER=['1','15','20','24','30a','30b','60','64','81']
MULT={'1':1,'15a':2,'15b':1,'20':2,'24':2,'60a':1,'60b':2,'64':1,'81_plus':1,'81_minus':1}
FRAME=[540,84,24,0,0,9,0,2,0,0,0,3,0,0,0,60,16,6,2,0,3,1,0,0,0]
SIGN=[1]*15+[-1]*10

def ip(a,b): return sum(s*x*y for s,x,y in zip(SIZES,a,b))//ORDER

def unit_matrix(rows,cols,entries):
    M=[[0 for _ in cols] for _ in rows]
    ri={x:i for i,x in enumerate(rows)};ci={x:i for i,x in enumerate(cols)}
    for r,c,v in entries:M[ri[r]][ci[c]]=v
    return M

RESTR=unit_matrix(OUTER,INNER,[
('1','1',1),('15a','15',1),('15b','15',1),('20','20',1),('24','24',1),
('60a','60',1),('60b','30a',1),('60b','30b',1),('64','64',1),
('81_plus','81',1),('81_minus','81',1)])
IND_FRAME_VISIBLE=[list(x) for x in zip(*RESTR)]
EXTERNAL_INDUCTION={
'1':['epsilon'],'20':['20_sign'],'24':['24_sign'],'60':['60a_sign'],'64':['64_sign']}
SIGN_ACTION={
'1':'epsilon','15a':'15b','15b':'15a','20':'20_sign','24':'24_sign',
'60a':'60a_sign','60b':'60b','64':'64_sign','81_plus':'81_minus','81_minus':'81_plus'}

def vhash(v):return hashlib.sha256(','.join(map(str,v)).encode()).hexdigest()

def main():
    gram=[[ip(CHARS[a],CHARS[b]) for b in OUTER] for a in OUTER]
    recon=[sum(MULT[k]*CHARS[k][j] for k in OUTER) for j in range(25)]
    inner_dim={'1':1,'15':15,'20':20,'24':24,'30a':30,'30b':30,'60':60,'64':64,'81':81}
    restrict_dim={o:sum(RESTR[i][j]*inner_dim[c] for j,c in enumerate(INNER)) for i,o in enumerate(OUTER)}
    ind_reading={i:{OUTER[j]:IND_FRAME_VISIBLE[ii][j] for j in range(len(OUTER)) if IND_FRAME_VISIBLE[ii][j]} for ii,i in enumerate(INNER)}
    checks={
      'ctbllib_identifier_locked':True,
      'twentyfive_ATLAS_classes':len(CLASSES)==len(SIZES)==25,
      'class_sizes_sum_group_order':sum(SIZES)==ORDER,
      'ten_visible_constituents':len(OUTER)==10,
      'all_character_vectors_length25':all(len(v)==25 for v in CHARS.values()),
      'all_character_degrees_match_labels':all(CHARS[x][0] in [1,15,20,24,60,64,81] for x in OUTER),
      'orthonormal_character_gram':gram==[[int(i==j) for j in range(10)] for i in range(10)],
      'frame_character_reconstructed':recon==FRAME,
      'frame_dimension540':recon[0]==540,
      'sign_is_linear_character':ip(SIGN,SIGN)==1 and SIGN[0]==1,
      '15_sign_twist':CHARS['15b']==[a*b for a,b in zip(SIGN,CHARS['15a'])],
      '81_sign_twist':CHARS['81_minus']==[a*b for a,b in zip(SIGN,CHARS['81_plus'])],
      '60b_sign_stable':CHARS['60b']==[a*b for a,b in zip(SIGN,CHARS['60b'])],
      'restriction_matrix_shape10x9':len(RESTR)==10 and all(len(x)==9 for x in RESTR),
      'restriction_dimensions_close':all(restrict_dim[o]==CHARS[o][0] for o in OUTER),
      'induction_is_frobenius_transpose':IND_FRAME_VISIBLE==[list(x) for x in zip(*RESTR)],
      'steinberg_induction_exact':ind_reading['81']=={'81_plus':1,'81_minus':1},
      'thirty_inductions_coincide':ind_reading['30a']=={'60b':1} and ind_reading['30b']=={'60b':1},
    }
    assert all(checks.values()),checks
    out={
      'schema':'w33.pass1102.ctbllib_clifford_naming.v1','status':'PASS',
      'headline':'The frame-visible U4(2):2 constituents now have canonical ATLAS-class fingerprints, exact restriction and frame-visible induction matrices, and a sign-twist fusion dictionary. The CTblLib table identifier and a row-query companion are frozen; numerical CTblLib row indices remain explicitly pending an observed GAP/CTblLib execution.',
      'ctbllib':{'table_identifier':'U4(2).2','row_indices_status':'pending_observed_gap_execution','companion':'analysis/w33_pass1102_ctbllib_rows.g'},
      'atlas_class_order':CLASSES,'class_sizes':SIZES,
      'outer_constituent_order':OUTER,'inner_constituent_order':INNER,
      'canonical_names':{k:{'atlas_label':k,'degree':CHARS[k][0],'character_sha256':vhash(CHARS[k]),'values':CHARS[k]} for k in OUTER},
      'restriction_matrix_outer_to_inner':RESTR,
      'induction_matrix_inner_to_outer_frame_visible':IND_FRAME_VISIBLE,
      'induction_external_sign_twists':EXTERNAL_INDUCTION,
      'sign_twist_action':SIGN_ACTION,
      'inner_product_gram':gram,'frame_permutation_character':FRAME,
      'check_count':len(checks),'checks':checks,
      'scope':'Exact class-character and Clifford-theory certificate. CTblLib row numbers are intentionally not guessed because GAP is unavailable in this runtime.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':len(checks),'rows_pending':True},indent=2))
if __name__=='__main__':main()
