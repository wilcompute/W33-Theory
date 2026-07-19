#!/usr/bin/env python3
"""Pass 475: concrete flat Heisenberg/Weyl experiment over GR(9,2).

We use GR(9,2)=Z/9Z[u]/(u^2+1), whose reduction x^2+1 over F_3 is
irreducible.  Primitive and depth-one central characters are represented by
1 and 3.  The executable witness computes exact orbit/radical data and
numerical Weyl spectra, then records the induced full central-sheet spectrum.
"""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass475_gr92_flat_weyl_spectrum.json'
P=3;N=9;F=2;Q=N**F

def ab(x:int)->tuple[int,int]:return x%N,x//N
def enc(a:int,b:int)->int:return (a%N)+N*(b%N)
def add(x:int,y:int)->int:
    a,b=ab(x);c,d=ab(y);return enc(a+c,b+d)
def neg(x:int)->int:
    a,b=ab(x);return enc(-a,-b)
def mul(x:int,y:int)->int:
    a,b=ab(x);c,d=ab(y);return enc(a*c-b*d,a*d+b*c)
def scalar(c:int,x:int)->int:return mul(enc(c,0),x)
def trace(x:int)->int:
    a,_b=ab(x);return 2*a%N

def is_unit(x:int)->bool:
    a,b=ab(x);return not (a%P==0 and b%P==0)

def weyl_block(t:int)->np.ndarray:
    omega=np.exp(2j*np.pi/N);inv2=pow(2,-1,N)
    elements=range(Q);vectors=[(x,y) for x in elements for y in elements if (x,y)!=(0,0)]
    matrix=np.zeros((Q,Q),dtype=np.complex128)
    for x,y in vectors:
        half_xy=scalar(inv2,mul(x,y))
        for s in elements:
            target=add(s,x)
            phase=add(mul(y,s),half_xy)
            exponent=trace(mul(t,phase))%N
            matrix[target,s]+=omega**exponent
    return matrix

def clustered_spectrum(matrix:np.ndarray)->dict[str,int]:
    values=np.linalg.eigvalsh((matrix+matrix.conj().T)/2)
    rounded=[int(round(float(x))) for x in values]
    if max(abs(float(x)-r) for x,r in zip(values,rounded))>1e-7:raise AssertionError('nonintegral spectrum recovery')
    return {str(k):v for k,v in sorted(Counter(rounded).items())}

def polynomial_residual(matrix:np.ndarray,roots:list[int])->float:
    identity=np.eye(matrix.shape[0],dtype=np.complex128);value=identity
    for root in roots:value=value@(matrix-root*identity)
    return float(np.max(np.abs(value)))

def valuation(number:int,p:int)->int:
    value=abs(number);answer=0
    while value and value%p==0:value//=p;answer+=1
    return answer

def radical(t:int)->list[tuple[int,int]]:
    return [(x,y) for x in range(Q) for y in range(Q) if mul(t,x)==0 and mul(t,y)==0]

def full_sheet_spectrum(t_depth:int)->dict[str,int]:
    a=P**(F*t_depth);d=Q//a
    if t_depth==0:
        return {str(Q-1):Q*(Q+1)//2,str(-(Q+1)):Q*(Q-1)//2}
    return {
      str(Q*a-1):d*(d+1)//2,
      str(-(Q*a+1)):d*(d-1)//2,
      '-1':Q*Q-d*d,
    }

def sheet_laplacian_valuation(spectrum:dict[str,int])->int:
    degree=Q*Q-1
    return sum(mult*valuation(degree-int(eigen),P) for eigen,mult in spectrum.items())

def build_payload()->dict:
    units=[x for x in range(Q) if is_unit(x)]
    depth=[x for x in range(Q) if x!=0 and not is_unit(x)]
    primitive_orbit={mul(u,enc(1,0)) for u in units}
    depth_orbit={mul(u,enc(3,0)) for u in units}
    primitive=weyl_block(enc(1,0));imprimitive=weyl_block(enc(3,0))
    primitive_spectrum=clustered_spectrum(primitive);depth_spectrum=clustered_spectrum(imprimitive)
    primitive_full=full_sheet_spectrum(0);depth_full=full_sheet_spectrum(1)
    primitive_residual=polynomial_residual(primitive,[80,-82])
    depth_residual=polynomial_residual(imprimitive,[728,-730,-1])
    rad_primitive=radical(enc(1,0));rad_depth=radical(enc(3,0))
    reduction_kernel=[(x,y) for x in range(Q) for y in range(Q) if all(c%P==0 for z in (x,y) for c in ab(z))]
    checks={
      'ring_has_81_elements':Q==81,
      'unit_and_depth_strata_72_8':len(units)==72 and len(depth)==8,
      'unit_actions_are_transitive_on_both_strata':primitive_orbit==set(units) and depth_orbit==set(depth),
      'primitive_block_is_hermitian':float(np.max(np.abs(primitive-primitive.conj().T)))<1e-10,
      'depth_block_is_hermitian':float(np.max(np.abs(imprimitive-imprimitive.conj().T)))<1e-10,
      'primitive_spectrum_exactly_80_41_minus82_40':primitive_spectrum=={'-82':40,'80':41},
      'depth_spectrum_exactly_728_5_minus730_4_minus1_72':depth_spectrum=={'-730':4,'-1':72,'728':5},
      'minimal_polynomial_residuals_small':primitive_residual<1e-9 and depth_residual<1e-6,
      'radical_sizes_1_81':len(rad_primitive)==1 and len(rad_depth)==81,
      'depth_radical_is_hjelmslev_reduction_kernel':set(rad_depth)==set(reduction_kernel),
      'full_sheet_dimensions_6561':sum(primitive_full.values())==Q*Q and sum(depth_full.values())==Q*Q,
      'full_sheet_traces_zero':sum(int(k)*v for k,v in primitive_full.items())==0 and sum(int(k)*v for k,v in depth_full.items())==0,
      'sheet_laplacian_valuations_26244_52326':sheet_laplacian_valuation(primitive_full)==26244 and sheet_laplacian_valuation(depth_full)==52326,
    }
    return {
      'schema':'w33.pass475.gr92_flat_weyl_spectrum.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'ring':{'presentation':'GR(9,2)=Z/9Z[u]/(u^2+1)','elements':Q,'residue_field':'F_9','reduction_kernel_size':9},
      'character_strata':{
        'primitive':{'characters':len(units),'representative':'1','radical_size':len(rad_primitive),'weyl_spectrum_81d':primitive_spectrum,'full_central_sheet_spectrum_6561d':primitive_full,'laplacian_3adic_determinant_valuation':sheet_laplacian_valuation(primitive_full)},
        'depth_one':{'characters':len(depth),'representative':'3','radical_size':len(rad_depth),'weyl_spectrum_81d':depth_spectrum,'full_central_sheet_spectrum_6561d':depth_full,'laplacian_3adic_determinant_valuation':sheet_laplacian_valuation(depth_full)},
      },
      'spectral_law':(
        'For Q=81 and annihilator size a, put d=Q/a.  The active irreducible has eigenvalues Qa-1 and -(Qa+1) '
        'with multiplicities (d+1)/2 and (d-1)/2.  In the full central sheet these multiplicities become d(d+1)/2 '
        'and d(d-1)/2, while -1 has multiplicity Q^2-d^2.'),
      'hjelmslev_theorem':(
        'The primitive character has trivial alternating radical.  The depth-one character has radical 3R x 3R '
        'of size 81, exactly the kernel of reduction R^2 -> F_9^2.'),
      'boundary':(
        'The spectra, radical, and block-local 3-adic determinant data are exact executable witnesses.  The global '
        'characteristic-primary Smith group of the 531441-vertex Heisenberg Cayley graph is not claimed, because '
        'characteristic-prime Fourier decomposition is not unimodular.'),
      'numeric_residuals':{'primitive_minpoly_max_abs':primitive_residual,'depth_minpoly_max_abs':depth_residual},
      'checks':checks,
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);args=ap.parse_args()
    payload=build_payload();text=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:
        if not args.output.exists() or args.output.read_text()!=text:raise SystemExit('Pass 475 certificate drift')
    else:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(json.dumps({'status':payload['status'],'checks':sum(payload['checks'].values()),'total':len(payload['checks'])}))
    return 0 if payload['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
