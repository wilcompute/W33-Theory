#!/usr/bin/env python3
import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)  # Pass 5548: JSONs opened by bare filename
import json, math
import numpy as np
from collections import Counter, deque

def inv_perm(p):
    inv=np.empty_like(p)
    inv[p]=np.arange(len(p),dtype=p.dtype)
    return inv

def perm_order(p):
    n=len(p)
    seen=np.zeros(n,dtype=bool)
    l=1
    for i in range(n):
        if not seen[i]:
            j=i; L=0
            while not seen[j]:
                seen[j]=True
                j=int(p[j]); L+=1
            l=l*L//math.gcd(l,L)
    return l

def gen_group_n(gens, n, max_size=100000):
    idp=np.arange(n,dtype=np.uint16)
    seen={idp.tobytes():idp}
    q=deque([idp])
    while q and len(seen)<max_size:
        p=q.popleft()
        for g in gens:
            h=g[p]
            k=h.tobytes()
            if k not in seen:
                seen[k]=h
                q.append(h)
    return seen

def check_preserve_dot(dot, p):
    dp = dot[p][:,p]
    return np.array_equal(dp, dot)

def main():
    # Load repo artifacts (relative paths assume you run from bundle root)
    with open("sp43_to_we6even_word_map.json","r") as f:
        word_map=json.load(f)
    with open("sp43_root_perms_fixed.json","r") as f:
        sp43_root=[np.array(x,dtype=np.uint16) for x in json.load(f)]
    with open("sp43_line_perms_fixed.json","r") as f:
        sp43_line=[np.array(x,dtype=np.uint16) for x in json.load(f)]
    with open("sp43_line_eps_fixed.json","r") as f:
        sp43_eps=[np.array(x,dtype=np.int8) for x in json.load(f)]
    # Load we6_true_action from extracted repo path if present next to script; otherwise user can copy it in.
    with open("we6_true_action.json","r") as f:
        we6=json.load(f)
    roots=np.array(we6["roots_int2"],dtype=np.int16)  # 240x8
    dot = roots @ roots.T
    # antipode mapping
    root_to_i={tuple(r):i for i,r in enumerate(roots.tolist())}
    antip=np.empty(240,dtype=np.uint16)
    for i,r in enumerate(roots.tolist()):
        antip[i]=root_to_i[tuple([-x for x in r])]
    assert np.all(antip[antip]==np.arange(240))
    # check each generator preserves dot + antipodes
    for i,p in enumerate(sp43_root):
        assert np.array_equal(antip[p], p[antip]), f"antipode fail gen {i}"
        assert check_preserve_dot(dot,p), f"dot fail gen {i}"
    # group orders
    G=gen_group_n(sp43_line,120,max_size=30000)
    assert len(G)==25920, f"line group order mismatch {len(G)}"
    # cocycle triviality check
    # build canonical line reps: use indices < 120 paired with +120 (this holds in we6_true root ordering)
    line_reps=np.arange(120,dtype=np.uint16)
    root_to_line=np.empty(240,dtype=np.uint16)
    for i in range(120):
        root_to_line[i]=i
        root_to_line[i+120]=i
    def line_perm_and_eps(root_perm):
        img=root_perm[line_reps]
        line_img=root_to_line[img]
        rep_img=line_reps[line_img]
        eps=np.where(img==rep_img,1,-1).astype(np.int8)
        ok=np.all((img==rep_img) | (img==antip[rep_img]))
        assert ok
        return line_img.astype(np.uint16), eps
    # compute cocycle for generator pairs
    for i in range(10):
        for j in range(10):
            p_comb = sp43_root[j][sp43_root[i]]
            lp_comb, eps_comb = line_perm_and_eps(p_comb)
            val = sp43_eps[i] * sp43_eps[j][sp43_line[i]] * eps_comb
            if np.any(val==-1):
                raise AssertionError(f"nontrivial cocycle at pair {(i,j)}")
    print("ALL CHECKS PASSED")

if __name__=="__main__":
    main()
