#!/usr/bin/env python3
"""Pass5621: a genuine continuum appears under many-cell magnetic composition, but it is not a Weyl law.

Pass5611 proved that increasing q in the maximally symmetric affine magnetic bulk
leaves an atomic limiting spectral measure.  The repo also contains genuine
finite covers (selected135 -> its 270-vertex Kronecker closure; 810 flags -> 1620
apartments), but a finite cover is not an infinite continuum argument.

Use instead the exact deck-odd 16-dimensional q=3 magnetic cell from Pass5619:
  spec H_- = {-6^4,-3^4,3^4,6^4}.
For N independent cells define the commuting tensor-sum
  H_N = sum_j I tensor ... tensor H_- tensor ... tensor I.
Its empirical spectral distribution is exactly the N-fold convolution of the
single-cell law P(X=+/-3)=P(X=+/-6)=1/4.  Hence the classical CLT applies.

The exact single-cell characteristic function is
  phi(t)=1/2(cos 3t + cos 6t),
variance sigma^2=45/2, and excess kurtosis=-41/25.  Therefore
  H_N/(sqrt(N)*sigma) -> N(0,1)
and the excess kurtosis is -41/(25N).

This produces a continuous limiting spectral density without changing q, but it
is a many-body/configuration-space continuum with exponential degeneracy, not a
Weyl counting law for physical spacetime.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5621_MANY_CELL_MAGNETIC_CLT.json'

def convolve(a,b):
    c=Counter()
    for x,nx in a.items():
        for y,ny in b.items(): c[x+y]+=nx*ny
    return c

def main():
    # Multiplicities in the 16-dimensional deck-odd cell.
    one=Counter({-6:4,-3:4,3:4,6:4})
    dim=sum(one.values()); assert dim==16
    mean=Fraction(sum(x*m for x,m in one.items()),dim); assert mean==0
    mu2=Fraction(sum(x*x*m for x,m in one.items()),dim)
    mu4=Fraction(sum(x**4*m for x,m in one.items()),dim)
    assert mu2==Fraction(45,2) and mu4==Fraction(1377,2)
    kappa4=mu4-3*mu2*mu2
    excess=kappa4/(mu2*mu2)
    assert excess==Fraction(-41,25)

    finite={}
    dist=Counter({0:1})
    for N in range(1,9):
        dist=convolve(dist,one)
        assert sum(dist.values())==16**N
        m2=Fraction(sum(e*e*n for e,n in dist.items()),16**N)
        m4=Fraction(sum(e**4*n for e,n in dist.items()),16**N)
        ex=(m4-3*m2*m2)/(m2*m2)
        assert m2==N*mu2 and ex==Fraction(-41,25*N)
        finite[str(N)]={'hilbert_dimension':16**N,'distinct_energies':len(dist),'min_energy':min(dist),'max_energy':max(dist),'variance':str(m2),'excess_kurtosis':str(ex)}

    out={
      'pass':5621,'status':'EXACT_MANY_CELL_GAUSSIAN_SPECTRAL_CONTINUUM_NOT_WEYL_SPACETIME',
      'single_cell':{'dimension':16,'spectrum':{'-6':4,'-3':4,'3':4,'6':4},'characteristic_function':'phi(t)=1/2(cos(3t)+cos(6t))','variance':'45/2','fourth_moment':'1377/2','excess_kurtosis':'-41/25'},
      'N_cell':{'operator':'H_N=sum_j H_-^(j) on (C^16)^{tensor N}','normalization':'sqrt((45/2)N)','limit':'standard Gaussian empirical spectral distribution','excess_kurtosis':'-41/(25N)','finite_checks_N1_to_N8':finite},
      'continuum_mechanism':'Level spacing after sqrt(N) normalization shrinks like N^{-1/2} while the normalized empirical measure converges to a continuous Gaussian.',
      'weyl_firewall':'Hilbert dimension grows as 16^N and the limit is a many-body convolution law. No polynomial eigenvalue counting N(lambda)~C lambda^d, local spatial refinement map, Lorentzian manifold, or 3+1-dimensional Weyl law follows.',
      'repo_cover_context':'Pass4719 gives a genuine selected135 -> 270 Kronecker cover and Pass4713 gives an 810 -> 1620 apartment C2 cover. They establish real finite refinement maps, but not an indefinitely iterable connected tower with a derived geometric scaling ratio.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
