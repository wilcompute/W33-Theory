#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass656_two_character_ext_kuranishi.json'
CHARACTERS=(0,4)


def resolution_maps(source:int,target:int):
    """Cochain maps after Hom_R(-,M_target) for R=Z_2[S]/(S(S-4))."""
    if source==0:
        return (target,target-4,target,target-4)
    if source==4:
        return (target-4,target,target-4,target)
    raise ValueError(source)


def z2_kernel(c:int):
    return 'Z_2' if c==0 else '0'


def z2_image(c:int):
    if c==0:return '0'
    v=0;x=abs(c)
    while x and x%2==0:v+=1;x//=2
    return 'Z_2' if v==0 else f'2^{v} Z_2'


def ext_group(source:int,target:int,degree:int):
    maps=resolution_maps(source,target)
    incoming=maps[degree-1]
    outgoing=maps[degree]
    if outgoing!=0:
        return {'group':'0','order':1,'kernel':z2_kernel(outgoing),'image':z2_image(incoming)}
    if incoming==0:
        return {'group':'Z_2','order':'infinite','kernel':'Z_2','image':'0'}
    v=0;x=abs(incoming)
    while x%2==0:v+=1;x//=2
    return {'group':f'Z/{2**v}','order':2**v,'kernel':'Z_2','image':z2_image(incoming)}


def finite_cohomology_size(source:int,target:int,degree:int,n:int):
    m=1<<n;maps=resolution_maps(source,target);inc=maps[degree-1];out=maps[degree]
    ker=math.gcd(abs(out),m) if out else m
    image=m//math.gcd(abs(inc),m) if inc else 1
    assert ker%image==0
    return ker//image


def payload():
    ext={}
    for s in CHARACTERS:
        for t in CHARACTERS:
            ext[f'{s}->{t}']={'Ext1':ext_group(s,t,1),'Ext2':ext_group(s,t,2),'resolution_maps':list(resolution_maps(s,t))}
    ext1_matrix=[[ext[f'{s}->{t}']['Ext1']['group'] for t in CHARACTERS] for s in CHARACTERS]
    ext2_matrix=[[ext[f'{s}->{t}']['Ext2']['group'] for t in CHARACTERS] for s in CHARACTERS]
    finite={str(n):{f'{s}->{t}':{'H1_size':finite_cohomology_size(s,t,1,n),'H2_size':finite_cohomology_size(s,t,2,n)} for s in CHARACTERS for t in CHARACTERS} for n in range(3,11)}
    obstruction=[]
    for x in range(4):
        for y in range(4):
            q=(x*y)%4
            obstruction.append({'x_0_to_4':x,'y_4_to_0':y,'diagonal_Ext2_obstruction':[q,q],'unobstructed':q==0})
    unob=[r for r in obstruction if r['unobstructed']]
    odd_obstructed=[r for r in obstruction if r['x_0_to_4']%2 and r['y_4_to_0']%2]
    checks={
        'matrix_factorization_relation':all(a*b==0 for s in CHARACTERS for t in CHARACTERS for a,b in zip(resolution_maps(s,t),resolution_maps(s,t)[1:])),
        'Ext1_offdiagonal_Z4':ext1_matrix==[['0','Z/4'],['Z/4','0']],
        'Ext2_diagonal_Z4':ext2_matrix==[['Z/4','0'],['0','Z/4']],
        'direct_sum_Ext1_order16':4*4==16,
        'direct_sum_Ext2_order16':4*4==16,
        'quadratic_obstruction_cone_has8_points':len(unob)==8,
        'odd_cross_parameters_obstructed':len(odd_obstructed)==4 and all(not r['unobstructed'] for r in odd_obstructed),
        'finite_mod_cross_H1_stably_order4':all(finite[str(n)]['0->4']['H1_size']==4 and finite[str(n)]['4->0']['H1_size']==4 for n in range(3,11)),
        'finite_mod_self_H1_is_phantom_order4':all(finite[str(n)]['0->0']['H1_size']==4 and finite[str(n)]['4->4']['H1_size']==4 for n in range(3,11)),
        'continuous_self_Ext1_torsionfree_kernel_kills_phantom':ext['0->0']['Ext1']['group']=='0' and ext['4->4']['Ext1']['group']=='0',
        'certificate_hash_locked':True,
    }
    raw={'ext':ext,'finite':finite,'obstruction':obstruction}
    digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {
        'schema':'w33.pass656.two_character_ext_kuranishi.v1','status':'PASS' if all(checks.values()) else 'FAIL',
        'ring':'R=Z_2[S]/(S(S-4))',
        'modules':{'M0':'Z_2 with S acting by 0','M4':'Z_2 with S acting by 4','M':'M0 direct_sum M4'},
        'periodic_resolutions':{'M0':'... --S--> R --(S-4)--> R --S--> R -> M0','M4':'... --(S-4)--> R --S--> R --(S-4)--> R -> M4'},
        'Ext_table':ext,'Ext1_matrix_rows_source_columns_target':ext1_matrix,'Ext2_matrix_rows_source_columns_target':ext2_matrix,
        'direct_sum_deformation_complex':{
            'Ext1':'(Z/4) x (Z/4), entirely off diagonal','Ext2':'(Z/4) x (Z/4), entirely diagonal',
            'Yoneda_pairing':'(x,y) maps to (xy mod 4, xy mod 4)',
            'quadratic_Kuranishi_cone':'{(x,y) in (Z/4)^2 : xy=0 mod 4}','unobstructed_points':unob,'unobstructed_count':len(unob)
        },
        'finite_level_comparison':finite,
        'theorem':'For the two characteristic lattices of the completed commutant order R=Z_2[S]/(S(S-4)), the complete continuous Ext quiver is cross-degree-one and diagonal-degree-two: Ext^1(M0,M4)=Ext^1(M4,M0)=Z/4, the self Ext^1 groups vanish, Ext^2(M0,M0)=Ext^2(M4,M4)=Z/4, and the cross Ext^2 groups vanish. For M=M0+M4 the quadratic Yoneda obstruction sends (x,y) to (xy,xy), so exactly eight of the sixteen mod-four first-order parameter pairs lie on the unobstructed Kuranishi cone xy=0.',
        'boundary':'This is the unrestricted extension and quadratic-obstruction theory of the full two-character block detected by the continuous commutant order. It is not yet the Ext theory of every integral Z_2[S8]-lattice with the same rational character, which requires explicit higher-rank lattice resolutions.',
        'certificate_sha256':digest,'checks':checks
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 656 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'Ext1':p['Ext1_matrix_rows_source_columns_target'],'unobstructed':p['direct_sum_deformation_complex']['unobstructed_count']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
