#!/usr/bin/env python3
"""Pass 474: exact original-coordinate intertwiner and monomial obstruction.

The q=5 collision's faithful sheets are conjugate over Q(zeta_5), but this file
works before companion reduction.  It constructs exact cyclic decompositions of
the two 25-dimensional Weyl sheets, builds the resulting original-coordinate
intertwiner, and tests the stronger monomial/phase-gauge possibility using a
triangle-gain invariant.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from fractions import Fraction
from functools import lru_cache, reduce
from math import gcd
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass474_original_coordinate_intertwiner.json'
Q=5
PAIR_A=(0,3,4,1,1,0,2,0,1,1,2,2)
PAIR_B=(0,2,3,0,2,2,4,1,0,3,3,2)
Cyclo=tuple[Fraction,Fraction,Fraction,Fraction]
ZERO:Cyclo=(Fraction(0),)*4
ONE:Cyclo=(Fraction(1),Fraction(0),Fraction(0),Fraction(0))
MONOMIALS=[ONE,(Fraction(0),Fraction(1),Fraction(0),Fraction(0)),(Fraction(0),Fraction(0),Fraction(1),Fraction(0)),(Fraction(0),Fraction(0),Fraction(0),Fraction(1)),(Fraction(-1),Fraction(-1),Fraction(-1),Fraction(-1))]

def cadd(a:Cyclo,b:Cyclo)->Cyclo:return tuple(x+y for x,y in zip(a,b))
def cneg(a:Cyclo)->Cyclo:return tuple(-x for x in a)
def csub(a:Cyclo,b:Cyclo)->Cyclo:return tuple(x-y for x,y in zip(a,b))
def cscale(a:Cyclo,c:Fraction)->Cyclo:return tuple(c*x for x in a)
def czero(a:Cyclo)->bool:return all(x==0 for x in a)
def cmul(a:Cyclo,b:Cyclo)->Cyclo:
    aa=list(a)+[Fraction(0)];bb=list(b)+[Fraction(0)];cc=[Fraction(0)]*5
    for i,x in enumerate(aa):
        if x:
            for j,y in enumerate(bb):
                if y:cc[(i+j)%5]+=x*y
    return tuple(cc[i]-cc[4] for i in range(4))

def cconj(a:Cyclo)->Cyclo:
    out=ZERO
    for coefficient,monomial in zip(a,[MONOMIALS[0],MONOMIALS[4],MONOMIALS[3],MONOMIALS[2]]):out=cadd(out,cscale(monomial,coefficient))
    return out

@lru_cache(None)
def cinv(a:Cyclo)->Cyclo:
    if czero(a):raise ZeroDivisionError
    augmented=[[Fraction(0)]*5 for _ in range(4)]
    for j in range(4):
        product=cmul(a,MONOMIALS[j])
        for i in range(4):augmented[i][j]=product[i]
    for i in range(4):augmented[i][4]=Fraction(i==0)
    for c in range(4):
        pivot=next(i for i in range(c,4) if augmented[i][c]);augmented[c],augmented[pivot]=augmented[pivot],augmented[c]
        value=augmented[c][c];augmented[c]=[x/value for x in augmented[c]]
        for i in range(4):
            if i!=c and augmented[i][c]:
                factor=augmented[i][c];augmented[i]=[x-factor*y for x,y in zip(augmented[i],augmented[c])]
    return tuple(augmented[i][4] for i in range(4))

def cdiv(a:Cyclo,b:Cyclo)->Cyclo:return cmul(a,cinv(b))
def section_pairs():
    vectors=[(a,b) for a in range(Q) for b in range(Q) if (a,b)!=(0,0)];out=[];seen=set()
    for vector in vectors:
        negative=(-vector[0]%Q,-vector[1]%Q);key=tuple(sorted((vector,negative)))
        if key not in seen:seen.add(key);out.append(key)
    return out
PAIRS=section_pairs();BASE=[(a,b) for a in range(Q) for b in range(Q)];INDEX={value:i for i,value in enumerate(BASE)}

def full_section(offsets):
    result={}
    for (vector,negative),c in zip(PAIRS,offsets):result[vector]=c;result[negative]=-c%Q
    return result

def exponent_matrix(offsets,t):
    labels=[[-1]*25 for _ in range(25)]
    for a,b in BASE:
        i=INDEX[(a,b)]
        for (x,y),z in full_section(offsets).items():labels[i][INDEX[((a+x)%Q,(b+y)%Q)]]=t*(z-a*y+x*b)%Q
    return labels

def weyl_matrix(offsets,t):
    labels=exponent_matrix(offsets,t)
    return [[ZERO if labels[i][j]<0 else MONOMIALS[labels[i][j]] for j in range(25)] for i in range(25)]

def matvec(matrix,vector):
    result=[]
    for row in matrix:
        total=ZERO
        for a,x in zip(row,vector):
            if not czero(a) and not czero(x):total=cadd(total,cmul(a,x))
        result.append(total)
    return result

def rank_columns(columns,n=25):
    if not columns:return 0
    matrix=[[columns[j][i] for j in range(len(columns))] for i in range(n)];rank=0
    for column in range(len(columns)):
        pivot=next((i for i in range(rank,n) if not czero(matrix[i][column])),None)
        if pivot is None:continue
        matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank];inverse=cinv(matrix[rank][column]);matrix[rank]=[cmul(x,inverse) for x in matrix[rank]]
        for i in range(rank+1,n):
            if not czero(matrix[i][column]):
                factor=matrix[i][column];matrix[i]=[csub(x,cmul(factor,y)) for x,y in zip(matrix[i],matrix[rank])]
        rank+=1
        if rank==n:break
    return rank

def cyclic_basis(matrix):
    columns=[];generators=[]
    for j in range(25):
        vector=[ZERO]*25;vector[j]=ONE;orbit=[]
        for _ in range(5):orbit.append(vector);vector=matvec(matrix,vector)
        if rank_columns(columns+orbit)==len(columns)+5:
            columns.extend(orbit);generators.append(j)
            if len(columns)==25:break
    if len(columns)!=25:raise AssertionError(('cyclic decomposition failed',generators))
    return [[columns[j][i] for j in range(25)] for i in range(25)],generators

def matrix_multiply(left,right):
    m=len(left);k=len(right);n=len(right[0]);out=[[ZERO for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for s in range(k):
            a=left[i][s]
            if czero(a):continue
            for j in range(n):
                if not czero(right[s][j]):out[i][j]=cadd(out[i][j],cmul(a,right[s][j]))
    return out

def identity(n):return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def matrix_equal(left,right):return all(left[i][j]==right[i][j] for i in range(len(left)) for j in range(len(left[0])))

def inverse_matrix(matrix):
    n=len(matrix);work=[list(matrix[i])+[ONE if i==j else ZERO for j in range(n)] for i in range(n)];determinant=ONE;sign=1
    for column in range(n):
        pivot=next(i for i in range(column,n) if not czero(work[i][column]))
        if pivot!=column:work[column],work[pivot]=work[pivot],work[column];sign*=-1
        value=work[column][column];determinant=cmul(determinant,value);inverse=cinv(value);work[column]=[cmul(x,inverse) for x in work[column]]
        for i in range(n):
            if i!=column and not czero(work[i][column]):
                factor=work[i][column];work[i]=[csub(x,cmul(factor,y)) for x,y in zip(work[i],work[column])]
    if sign<0:determinant=cneg(determinant)
    return [row[n:] for row in work],determinant

def denominator_stats(matrix):
    denominators=[coefficient.denominator for row in matrix for entry in row for coefficient in entry];lcm=lambda a,b:a*b//gcd(a,b)
    return {'maximum_denominator':max(denominators),'common_denominator':reduce(lcm,denominators,1),'nonintegral_entries':sum(any(c.denominator!=1 for c in entry) for row in matrix for entry in row)}

def field_norm(element):
    x=sp.Symbol('x');polynomial=sum(sp.Rational(c.numerator,c.denominator)*x**i for i,c in enumerate(element));return sp.factor(sp.resultant(polynomial,x**4+x**3+x**2+x+1,x))

def matrix_digest(matrix):
    payload=';'.join(','.join('/'.join(f'{c.numerator}:{c.denominator}' for c in entry) for entry in row) for row in matrix);return hashlib.sha256(payload.encode()).hexdigest()

def triangle_histogram(labels):
    histogram=Counter()
    for i in range(25):
        for j in range(i+1,25):
            counts=[0]*5
            for k in range(25):
                if k not in (i,j):counts[(labels[i][j]+labels[j][k]+labels[k][i])%5]+=1
            histogram[tuple(counts)]+=1
    return sorted((list(key),value) for key,value in histogram.items())

def build_payload():
    A=weyl_matrix(PAIR_A,1);B=weyl_matrix(PAIR_B,2);UA,gens_A=cyclic_basis(A);UB,gens_B=cyclic_basis(B);UAinv,det_A=inverse_matrix(UA);UBinv,det_B=inverse_matrix(UB);X=matrix_multiply(UB,UAinv);Xinv=matrix_multiply(UA,UBinv);det_X=cdiv(det_B,det_A);norm_X=field_norm(det_X);hist_A=triangle_histogram(exponent_matrix(PAIR_A,1));hist_B=triangle_histogram(exponent_matrix(PAIR_B,2));stats_X=denominator_stats(X);stats_Xinv=denominator_stats(Xinv)
    checks={'both_weyl_sheets_hermitian':all(A[i][j]==cconj(A[j][i]) and B[i][j]==cconj(B[j][i]) for i in range(25) for j in range(25)),'five_cyclic_generators_each':gens_A==[0,1,2,3,4] and gens_B==[0,1,2,3,4],'cyclic_bases_invert_exactly':matrix_equal(matrix_multiply(UA,UAinv),identity(25)) and matrix_equal(matrix_multiply(UB,UBinv),identity(25)),'exact_original_coordinate_intertwiner':matrix_equal(matrix_multiply(B,X),matrix_multiply(X,A)),'exact_inverse_intertwiner':matrix_equal(matrix_multiply(Xinv,B),matrix_multiply(A,Xinv)),'triangle_gain_histograms_obstruct_monomial_gauge':hist_A!=hist_B,'canonical_krylov_intertwiner_is_not_cyclotomic_integral':stats_X['nonintegral_entries']>0,'canonical_krylov_intertwiner_is_not_unimodular':norm_X not in (1,-1)}
    return {'schema':'w33.pass474.original_coordinate_intertwiner.v1','status':'PASS' if all(checks.values()) else 'FAIL','sheets':{'source':'Graph A, central character t=1','target':'Graph B, central character t=2','dimension':25,'field':'Q(zeta_5)'},'cyclic_decomposition':{'source_generators':gens_A,'target_generators':gens_B,'block_degrees':[5]*5},'intertwiner':{'construction':'X=U_B U_A^{-1} from exact standard-coordinate Krylov bases','sha256':matrix_digest(X),'inverse_sha256':matrix_digest(Xinv),'entry_statistics':stats_X,'inverse_entry_statistics':stats_Xinv,'determinant_norm':str(norm_X)},'monomial_firewall':{'invariant':'global histogram of gauge-invariant oriented triangle gains on each unordered edge','source_color_classes':len(hist_A),'target_color_classes':len(hist_B),'histograms_equal':hist_A==hist_B},'theorem':'The exchanged faithful q=5 sheets are exactly similar in their original 25-dimensional Weyl coordinates over Q(zeta_5). A standard-coordinate cyclic decomposition gives an explicit exact intertwiner X.  However the two complete gain graphs have different triangle-gain color histograms, so no permutation plus diagonal fifth-root phase gauge can implement the exchange.','boundary':'The displayed standard-Krylov intertwiner is nonintegral and nonunimodular.  This proves those properties for the canonical constructed lift, not the nonexistence of every possible GL_25(Z[zeta_5]) intertwiner.','checks':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);args=ap.parse_args();payload=build_payload();text=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:
        if not args.output.exists() or args.output.read_text()!=text:raise SystemExit('Pass 474 certificate drift')
    else:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(json.dumps({'status':payload['status'],'checks':sum(payload['checks'].values()),'total':len(payload['checks'])}));return 0 if payload['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
