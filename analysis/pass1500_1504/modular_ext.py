from __future__ import annotations
import numpy as np
from pass1370_1374 import core, modular_radicals
from .common import SparseRank,capture,factor_kernel_key,sha

def simple_classes(g,p):
    tensor=np.asarray(g['tensor'],dtype=np.int64)%p
    left=[tensor[:,a,:]%p for a in range(83)]
    factors=modular_radicals.composition_factors(left,p)
    grouped={}
    for F in factors: grouped.setdefault(factor_kernel_key(F,p),[]).append(F)
    records=[]
    for key,copies in grouped.items():
      records.append({'degree':int(copies[0][0].shape[0]),'regular_composition_multiplicity':len(copies),'factor':copies[0],'kernel_key':key})
    records.sort(key=lambda r:(r['degree'],r['kernel_key']))
    for i,r in enumerate(records):r['index']=i
    return tensor,factors,records

def hom_dimension(Fi,Fj,p):
    di=Fi[0].shape[0]; dj=Fj[0].shape[0]; rows=[]
    for a in range(len(Fi)):
      for u in range(dj):
       for v in range(di):
        row=np.zeros(dj*di,dtype=np.int64)
        for k in range(dj):row[k*di+v]+=int(Fj[a][u,k])
        for l in range(di):row[u*di+l]-=int(Fi[a][l,v])
        rows.append(row%p)
    return di*dj-modular_radicals.rank(np.asarray(rows,dtype=np.int64),p)

def multiplication_support(tensor):
    out={}
    for a in range(83):
        for b in range(83):
            nz=np.flatnonzero(tensor[:,a,b])
            out[a,b]=[(int(c),int(tensor[c,a,b])) for c in nz]
    return out

def rank_derivation_rows_p2(row_iter):
    pivots={}
    for terms in row_iter:
        bits=0
        for idx,coeff in terms:
            if coeff&1: bits ^= 1<<idx
        while bits:
            c=(bits & -bits).bit_length()-1
            pivot=pivots.get(c)
            if pivot is None:
                pivots[c]=bits;break
            bits ^= pivot
    return len(pivots)

def rank_derivation_rows_p3(row_iter,nvars):
    pivots={}
    for terms in row_iter:
        row=np.zeros(nvars,dtype=np.int8)
        for idx,coeff in terms: row[idx]=(int(row[idx])+coeff)%3
        while np.any(row):
            c=int(np.flatnonzero(row)[0]);pivot=pivots.get(c)
            if pivot is None:
                if row[c]==2: row=(-row)%3
                pivots[c]=row;break
            row=(row-int(row[c])*pivot)%3
    return len(pivots)

def ext_dimension(tensor,support,Fi,Fj,p):
    di=Fi[0].shape[0];dj=Fj[0].shape[0];block=di*dj;nvars=83*block
    def var(a,u,v):return a*block+u*di+v
    def rows():
        for a in range(83):
            Ra=Fj[a]
            for b in range(83):
                Rb=Fi[b];prod=support[a,b]
                for u in range(dj):
                    for v in range(di):
                        terms=[]
                        terms.extend((var(c,u,v),coeff) for c,coeff in prod)
                        terms.extend((var(b,k,v),-int(Ra[u,k])) for k in range(dj) if Ra[u,k])
                        terms.extend((var(a,u,l),-int(Rb[l,v])) for l in range(di) if Rb[l,v])
                        yield terms
    rank=rank_derivation_rows_p2(rows()) if p==2 else rank_derivation_rows_p3(rows(),nvars)
    cocycle=nvars-rank;hom=hom_dimension(Fi,Fj,p);inner=di*dj-hom;ext=cocycle-inner;assert ext>=0
    return {'cocycle_dimension':cocycle,'inner_dimension':inner,'hom_dimension':hom,'ext1_dimension':ext}

def analyze_prime(g,p):
    tensor,_factors,simples=simple_classes(g,p);support=multiplication_support(tensor); profile=modular_radicals.analyze_one(g,core,'full',p)
    for r in simples:
      r['endomorphism_field_dimension']=hom_dimension(r['factor'],r['factor'],p)
      num=r['degree']**2; assert num%r['endomorphism_field_dimension']==0
      r['semisimple_component_dimension']=num//r['endomorphism_field_dimension']
    semidim=sum(r['semisimple_component_dimension'] for r in simples); assert semidim==profile['semisimple_quotient_dimension']
    ext=[]; matrix=[]
    for i,si in enumerate(simples):
      row=[]
      for j,sj in enumerate(simples):
        rec=ext_dimension(tensor,support,si['factor'],sj['factor'],p);rec.update({'source':i,'target':j});ext.append(rec);row.append(rec['ext1_dimension'])
      matrix.append(row)
    vertices=[]
    for r in simples:
      vertices.append({'index':r['index'],'simple_degree_over_base_field':r['degree'],'endomorphism_field_dimension':r['endomorphism_field_dimension'],'semisimple_component_dimension':r['semisimple_component_dimension'],'regular_composition_multiplicity':r['regular_composition_multiplicity'],'annihilator_codimension':83-len(r['kernel_key']),'annihilator_sha256':sha(r['kernel_key'])})
    arrows=[x for x in ext if x['ext1_dimension']]
    assert matrix==[list(row) for row in zip(*matrix)]
    degrees=[v['simple_degree_over_base_field'] for v in vertices]
    weighted=sum(matrix[i][j]*degrees[i]*degrees[j] for i in range(len(degrees)) for j in range(len(degrees)))
    radical_head=profile['radical_power_dimensions'][0]-profile['radical_power_dimensions'][1]
    assert weighted==radical_head
    return {'prime':p,'vertices':vertices,'vertex_count':len(vertices),'semisimple_quotient_dimension_reconstructed':semidim,'all_simple_endomorphism_fields_split':all(x['endomorphism_field_dimension']==1 for x in vertices),'ext1_matrix_source_rows_target_columns':matrix,'ext1_matrix_symmetric':True,'arrows':arrows,'arrow_dimension_sum':sum(x['ext1_dimension'] for x in arrows),'weighted_arrow_bimodule_dimension':weighted,'jacobson_radical_head_dimension':radical_head,'radical_head_reconstructed_from_quiver':True,'radical_power_dimensions':profile['radical_power_dimensions'],'loewy_layers_top_to_socle':profile['loewy_layers_top_to_socle'],'loewy_length':profile['loewy_length']}
def analyze():
    _public,cap=capture();g=cap['g'];primes={str(p):analyze_prime(g,p) for p in (2,3)}
    result={'theorem':'Pass 1500 Exact Modular Gabriel Ext-Quivers','algebra':'83-dimensional selector orbital algebra','convention':'matrix entry (i,j) is dim Ext^1(S_i,S_j), hence arrows i -> j','method':'Simple modules are deduplicated by exact annihilator kernels. Endomorphism fields reconstruct the semisimple quotient without assuming splitness. Ext^1 is computed as derivations modulo inner derivations using all 83 basis products.','primes':primes,'boundary':'The certificate gives Ext^1 and Loewy dimensions. Higher quiver relations require Ext^2/Yoneda products.'}
    result['sha256']=sha(result);return result
