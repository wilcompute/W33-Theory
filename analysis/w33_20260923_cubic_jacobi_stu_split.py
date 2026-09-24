#!/usr/bin/env python3
"""Replay the cubic-Jacobi split module at two completely split primes."""
from __future__ import annotations
import json, os, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/w33_20260923_cubic_jacobi_split107.py"
OUT=ROOT/"data/w33_20260923_cubic_jacobi_stu_split.json"

def run(p):
    env=dict(os.environ); env["W33_SPLIT_PRIME"]=str(p)
    cp=subprocess.run([sys.executable,str(SOURCE)],cwd=ROOT,env=env,
                      capture_output=True,text=True,check=True)
    s=cp.stdout
    def need(pattern):
        m=re.search(pattern,s)
        assert m, (p,pattern,s)
        return m
    roots=need(r"split .*?\[(.*?)\]").group(1)
    modules=tuple(map(int,need(r"modules (\d+) (\d+) (\d+)").groups()))
    comm=tuple(map(int,need(r"commdims (\d+) (\d+)").groups()))
    assoc=tuple(map(int,need(r"full assoc W8/U6 (\d+) (\d+)").groups()))
    inv={}

    for deg in (1,2,3,4):
        m=need(rf"W8 invariant degree {deg} \((\d+), (\d+)\)")
        inv[str(deg)]=[int(m.group(1)),int(m.group(2))]
    perfect=list(map(int,need(r"factor_perfect_dims \[(\d+), (\d+), (\d+)\]").groups()))
    cross=need(r"factor_cross_zero \[(True|False), (True|False), (True|False)\]").groups()
    assert modules==(14,8,6)
    assert comm==(1,3)
    assert assoc==(64,12)
    assert [inv[str(k)][0] for k in (1,2,3,4)]==[0,0,0,1]
    assert perfect==[3,3,3] and all(x=="True" for x in cross)
    return {
        "prime":p,"centroid_split_eigenvalues":roots,
        "module_dimensions":{"h15_over_Z":14,"h9_over_Z":8,"h15_over_h9":6},
        "commutant_dimensions":{"W8":comm[0],"U6":comm[1]},
        "associative_algebra_dimensions":{"W8":assoc[0],"U6":assoc[1]},
        "invariant_polynomial_dimensions":inv,
        "factor_derived_dimensions":perfect,"factor_cross_brackets_zero":True,
        "stdout":s,
    }

runs=[run(107),run(151)]
out={
  "schema":"w33.20260923.cubic_jacobi_stu_split.v1",
  "status":"PASS_CUBIC_JACOBI_SPLITS_TO_A1_CUBED_WITH_222_PLUS_LOCAL_DOUBLETS",
  "runs":runs,
  "split_representation":{
    "levi":"sl2^3",
    "W8":"(2,2,2)",
    "U6":"(2,1,1) + (1,2,1) + (1,1,2)",
    "quartic_invariant":"one-dimensional degree-4 invariant space; no invariants in degrees 1,2,3",
  },

  "interpretation":"After splitting the totally real cubic centroid field, the nested Heisenberg phase space contains an irreducible three-doublet tensor sector with the classical 2x2x2 quartic-invariant fingerprint.",
  "boundary":"This identifies the finite representation/invariant package. It does not derive an STU black-hole solution, spacetime dynamics, or physical entropy."
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],
                  "primes":[r["prime"] for r in runs],
                  "W8_assoc":[r["associative_algebra_dimensions"]["W8"] for r in runs],
                  "quartic":[r["invariant_polynomial_dimensions"]["4"][0] for r in runs]},indent=2))
