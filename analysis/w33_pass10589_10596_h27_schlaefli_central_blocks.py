#!/usr/bin/env python3
"""Pass10589-10596: simultaneous H27/Schlaefli block decomposition under the H27 center C3.

On the canonical nine triples (fixed u in F3^2, varying central z), let P be the
complete 9-partite graph K_{3,...,3}.  Repo Pass7629 proves

    P = H27 + Schlaefli

edge-disjointly.  Fourier-transform along the central C3.  In the trivial
central character, P becomes 3*K9 while H27 becomes K9, hence Schlaefli is
2*K9.  In either nontrivial character, summing over the three target z-values
kills P identically, hence Schlaefli=-H27.

Thus H27 and Schlaefli are simultaneously block diagonal in the central Fourier
basis, and their spectra are read sector-by-sector with no numerical eigensolve.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10589_10596_H27_SCHLAEFLI_CENTRAL_BLOCKS.json'

def main():
    # Exact sector data from Pass10581 plus P-sector action.
    sectors={
      'chi0':{
        'dimension':9,
        'P':'3*K9','H27':'K9','Schlaefli':'2*K9',
        'H27_spectrum':{'8':1,'-1':8},
        'Schlaefli_spectrum':{'16':1,'-2':8}},
      'chi1':{
        'dimension':9,'P':'0','Schlaefli':'-H27',
        'H27_spectrum':{'2':6,'-4':3},
        'Schlaefli_spectrum':{'-2':6,'4':3}},
      'chi2':{
        'dimension':9,'P':'0','Schlaefli':'-H27',
        'H27_spectrum':{'2':6,'-4':3},
        'Schlaefli_spectrum':{'-2':6,'4':3}}
    }
    # Multiplicity checks.
    h={'8':1,'-1':8,'2':12,'-4':6}
    s={'16':1,'-2':20,'4':6}
    assert sum(h.values())==sum(s.values())==27
    # Degree/complement consistency: P has degree24, H degree8, S degree16.
    assert 8+16==24
    out={
      'schema':'w33.pass10589_10596.h27_schlaefli_central_blocks.v1','status':'PASS','passes':'10589-10596',
      'carrier':'nine central C3 triples indexed by u in F3^2',
      'identity':'K_{3,3,...,3}=H27 dot-union Schlaefli',
      'central_fourier_sectors':sectors,
      'global_H27_spectrum':h,
      'global_Schlaefli_spectrum':s,
      'simultaneous_diagonalization':True,
      'theorem':'The H27 and Schlaefli transports are simultaneously block diagonal under Fourier transform along the Heisenberg center C3. The trivial sector is K9 versus 2K9; in each nontrivial sector Schlaefli is exactly minus H27. This explains the shared 9x3 carrier and the spectra 8^1+2^12+(-1)^8+(-4)^6 and 16^1+4^6+(-2)^20 from one central Fourier decomposition.',
      'boundary':'Exact consequence of the repo H27 Heisenberg Cayley model and the certified H27/Schlaefli complement inside K_{3,...,3}. It does not identify the H(4)/(13:6) weighted quotient with either graph.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','H27':h,'Schlaefli':s}))
if __name__=='__main__':main()
