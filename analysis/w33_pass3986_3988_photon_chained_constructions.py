#!/usr/bin/env python3
"""Passes 3986-3988: W33 spectral metrology, dual-geometry echo, and exact self-similar photon kernel."""
from __future__ import annotations
import hashlib, json, math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def bits(x,n=4): return [(x>>i)%3 for i in range(n)]
def canon(v):
    for x in v:
        if x%3:
            inv=1 if x%3==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError

def symp(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
def w33():
    pts=[]
    for n in range(1,3**4):
        v=tuple((n//(3**i))%3 for i in range(4)); c=canon(v)
        if c not in pts: pts.append(c)
    assert len(pts)==40
    A=[[0]*40 for _ in range(40)]
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):
            if i!=j and symp(x,y)==0: A[i][j]=1
    assert all(sum(r)==12 for r in A)
    return A

def matmul(X,Y):
    return [[sum(X[i][k]*Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]
def eye(n): return [[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
def canonical_sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    A=w33(); n=40; I=eye(n); J=[[Fraction(1) for _ in range(n)] for _ in range(n)]
    U=[[Fraction(-1,3)*(I[i][j]+A[i][j])+Fraction(2,15)*J[i][j] for j in range(n)] for i in range(n)]
    assert matmul(U,U)==I
    assert set(x for row in U for x in row)=={Fraction(-1,5),Fraction(2,15)}
    assert all(sum(row)==1 for row in U)
    row_counts=[{str(Fraction(-1,5)):sum(x==Fraction(-1,5) for x in row),str(Fraction(2,15)):sum(x==Fraction(2,15) for x in row)} for row in U]
    assert all(r=={'-1/5':13,'2/15':27} for r in row_counts)
    # Pass 3986: QFI of L spectrum 0^1,10^24,16^15.
    mean=(24*10+15*16)/40; mean2=(24*100+15*256)/40; var=mean2-mean*mean
    assert mean==12 and var==12
    qfi_local=4*var; qfi_opt=(16-0)**2
    metrology=[]
    for m in range(1,7):
        metrology.append({'copies':m,'localized_product_qfi':qfi_local*m,'spectral_cat_qfi':qfi_opt*m*m,
                          'cat_over_product':qfi_opt*m*m/(qfi_local*m)})
    # Pass 3987: A/B echo spectra.
    Aeval=[12,2,-4]; Beval=[27,-3,3]
    Seval=[a+b for a,b in zip(Aeval,Beval)]; Deval=[a-b for a,b in zip(Aeval,Beval)]
    assert Seval==[39,-1,-1] and Deval==[-15,5,-7]
    echo={'A_eigenvalues':Aeval,'complement_eigenvalues':Beval,'sum_channel':Seval,'difference_channel':Deval,
          'sum_nontrivial_degeneracy':True,'difference_nontrivial_gap':12,
          'full_space_optimal_qfi':(max(Deval)-min(Deval))**2,
          'protected_nontrivial_qfi':(5-(-7))**2,
          'interpretation':'The sum arm is a geometry-blind common-mode control on the 39-dimensional nonuniform space; the difference arm resolves the two W33 sectors.'}
    # Pass 3988: tensor-power amplitude shells.
    shells={}
    for m in range(1,7):
        rows=[]
        norm=Fraction(0)
        for r in range(m+1):
            mult=math.comb(m,r)*(13**(m-r))*(27**r)
            amp=(Fraction(-1,5)**(m-r))*(Fraction(2,15)**r)
            norm+=mult*amp*amp
            rows.append({'far_coordinates':r,'multiplicity_per_row':mult,'amplitude':str(amp)})
        assert norm==1 and sum(x['multiplicity_per_row'] for x in rows)==40**m
        shells[str(m)]=rows
    result={'schema':'w33.pass3986_3988.photon_chained_constructions.v1','status':'PASS',
      'pass3986_spectral_metrology':{'laplacian_spectrum':{'0':1,'10':24,'16':15},'localized_mean':mean,'localized_variance':var,
        'localized_qfi':qfi_local,'optimal_single_copy_qfi':qfi_opt,'scaling':metrology,
        'boundary':'QFI assumes ideal coherent access to the declared spectral generator; it is not a measured sensitivity.'},
      'pass3987_dual_geometry_echo':echo,
      'pass3988_exact_global_reflection':{'formula':'exp(-i*pi*L/2)=I-2E_10=-(I+A)/3+2J/15',
        'period':'pi','half_period':'real symmetric involution','row_amplitudes':{'point_or_neighbor':'-1/5','nonneighbor':'2/15'},
        'row_multiplicities':{'point_or_neighbor':13,'nonneighbor':27},'tensor_power_shells':shells,
        'interpretation':'A continuous-time W33 coupling performs a global parallel 40-mode reflection in one analog evolution interval. This does not represent forty sequential orthogonal updates.',
        'boundary':'Physical realization requires an engineered Hamiltonian and calibrated coupling time; tensor powers require genuine independent mode factors and do not change vacuum c.'}}
    result['semantic_sha256']=canonical_sha(result)
    (ROOT/'data/PART_3986_3988_PHOTON_CHAINED_CONSTRUCTIONS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_PHOTON_CHAINED_CONSTRUCTIONS',qfi_local,qfi_opt,echo['full_space_optimal_qfi'],result['semantic_sha256'])
if __name__=='__main__': main()
