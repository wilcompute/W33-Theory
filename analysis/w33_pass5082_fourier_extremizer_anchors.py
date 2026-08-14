#!/usr/bin/env python3
"""Pass5082: exact Fourier-extremizer anchors for the full apartment code.

The Fourier identity is elementary once Pass5066 identifies the code with
characters evaluated on apartment boundaries.  This script freezes the exact
q=2,3,4 maxima supplied by already-certified minimum distances and records
where equality is completely classified.
"""
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5082_FOURIER_EXTREMIZER_ANCHORS.json'

def mu(n,d): return Fraction(n-2*d,n)
def formula(q): return Fraction((q+1)**2*(q*q+1)-16,(q+1)**2*(q*q+1))
def main():
    anchors={
      2:{'length':90,'distance':16,'minimum_shell':'45 chamber stars, complete'},
      3:{'length':1620,'distance':81,'minimum_shell':'160 chamber stars, complete'},
      4:{'length':13600,'distance':256,'minimum_shell':'open; distance exact'},
    }
    for q,a in anchors.items():
        m=mu(a['length'],a['distance']); assert m==formula(q)
        a['max_nontrivial_fourier']=f'{m.numerator}/{m.denominator}'
        a['spectral_gap']=f'{(1-m).numerator}/{(1-m).denominator}'
    out={'pass':5082,'status':'EXACT_ANCHORS_WITH_ALL_Q_BOUND_OPEN',
      'identity':'wt(c_y)=N_A*(1-muhat(y))/2',
      'target':'max_nontrivial muhat <= 1-16/((q+1)^2(q^2+1))',
      'anchors':{str(q):a for q,a in anchors.items()},
      'equality_classification':{'q2':'all 45 chamber stars','q3':'all 160 chamber stars','q4':'not classified'},
      'boundary':'This executes the Fourier attack at q=2,3,4 but does not prove the all-q extremizer inequality or q=5 distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
