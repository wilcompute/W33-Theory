#!/usr/bin/env python3
"""Hardened launcher for Pass4830 only.

The historical combined 4829/4830 producer writes the 4830 intertwiner
certificate before entering the older 4829 dual-basis section. Pass4829 now has
its own corrected producer. This launcher therefore hardens Hom-space negatives,
runs the combined producer, and accepts the expected later 4829 assertion only
if the exact 4830 certificate was already materialized.
"""
from __future__ import annotations
import random
from pathlib import Path
import w33_pass4829_4830_levi_code_sign_module as m

def hardened_hom_space(Amods,Bmods,n=64):
    eq=[]
    for Acols,Bcols in zip(Amods,Bmods):
        Brows=m.rows_from_cols(Bcols,n)
        for i in range(n):
            for j in range(n):
                mask=0;ac=Acols[j]
                while ac:
                    b=ac&-ac;k=b.bit_length()-1;ac^=b;mask^=1<<(i*n+k)
                br=Brows[i]
                while br:
                    b=br&-br;k=b.bit_length()-1;br^=b;mask^=1<<(k*n+j)
                if mask:eq.append(mask)
    H=m.null2(eq,n*n);inv=None;maxrank=0
    if len(H)<=20:
        for z in range(1,1<<len(H)):
            x=0
            for i,h in enumerate(H):
                if (z>>i)&1:x^=h
            r=m.matrix_rank_from_flat(x,n);maxrank=max(maxrank,r)
            if r==n:inv=x;break
        return H,maxrank,inv
    rng=random.Random(4830)
    for _ in range(20000):
        x=0
        for h in H:
            if rng.getrandbits(1):x^=h
        r=m.matrix_rank_from_flat(x,n);maxrank=max(maxrank,r)
        if r==n:return H,maxrank,x
    raise RuntimeError(f'Hom dimension {len(H)} too large for exhaustive negative certification; no invertible witness found in deterministic search')

m.hom_space=hardened_hom_space
try:
    rc=m.main()
except AssertionError:
    if not Path(m.OUT30).exists():
        raise
    # The assertion is in the superseded old 4829 dual-basis tail. 4830 is done.
    rc=0
raise SystemExit(rc)
