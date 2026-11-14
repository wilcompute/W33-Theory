#!/usr/bin/env python3
"""Independent SAT formulation of n=5 eight-maximal-Pauli-MUB question.

This is a different solver family (CaDiCaL/CDCL), with deterministic
rebuildable CNF: choose exactly four GF(2)-symmetric 5x5 rank-code
matrices among 2336 extenders of 0,infty,I,S2; enforce pairwise
nonsingularity and coverage of every extender. Both S3 class reps
692 and 694 are required for a complete no-go. Any timeout/budget
exhaustion remains UNDECIDED, never an UNSAT claim.
"""
from pathlib import Path
from itertools import combinations
import time,json,hashlib,sys,numpy as np
from pysat.solvers import Solver
from pysat.card import CardEnc,EncType
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as D
OUT=ROOT/"data/toe_20261114_fivequbit_MUB_independent_CaDiCaL_SAT.json"

def signature(A):
    raw=";".join(",".join(str(x) for x in row) for row in A)
    return hashlib.sha256(raw.encode()).hexdigest()

def solve_sat(n,rep,size,conflicts):
    pos,sing,ns,I,cand,reps=D.prep(n)
    universe=ns[~sing[ns^I]&~sing[ns^rep]&(ns!=I)&(ns!=rep)]
    assert rep in reps
    count=len(universe);choose=size-4
    cardinality=CardEnc.equals(lits=list(range(1,count+1)),
          bound=choose,encoding=EncType.seqcounter)
    started=time.perf_counter()
    dig=hashlib.sha256()
    clause_counts={"exact_cardinality":len(cardinality.clauses),"cover":0,"incompatible_pairs":0}
    s=Solver(name="cadical195",with_proof=True)
    def add(clause):
        s.add_clause(clause)
        for v in clause:dig.update(str(int(v)).encode()+b",")
        dig.update(b"0;")
    for clause in cardinality.clauses:add(clause)
    # Each still-compatible extender T must be killed by at least one
    # selected C: C==T OR det(C+T)==0; choose C=T handles chosen items.
    for u in universe:
        killers=np.flatnonzero(sing[universe^u] | (universe==u))
        assert len(killers)>0
        add((killers+1).tolist())
        clause_counts["cover"]+=1
    # Any two selected C,D must have C+D nonsingular.
    for i in range(count):
        inds=np.flatnonzero(sing[universe[i]^universe[i+1:]])
        for off in inds:
            add([-(i+1),-(i+2+int(off))])
        clause_counts["incompatible_pairs"]+=len(inds)
    building=time.perf_counter()-started
    s.conf_budget(conflicts)
    beginning=time.perf_counter()
    sat=s.solve_limited(expect_interrupt=False)
    solving=time.perf_counter()-beginning
    result="UNDECIDED_BOUNDED_CONFLICTS" if sat is None else ("SAT_WITNESS" if sat else "UNSAT_CADICAL")
    witness=None;proof_lines=0
    if sat is True:
        values={x for x in s.get_model() if x>0}
        witness=[int(universe[i]) for i in range(count) if i+1 in values]
        assert len(witness)==choose
        chosen=[int(I),int(rep)]+witness
        assert all(not sing[a^b] for a,b in combinations(chosen,2))
        for u in ns:
            assert u in chosen or any(sing[u^z] for z in chosen)
    if sat is False:
        proof=s.get_proof() or []
        proof_lines=len(proof)
        # Save a portable DRAT transcript alongside exact deterministic
        # clause generator only if proof size is controlled (<12 MB).
        payload="\n".join(proof)+"\n"
        if proof and len(payload.encode())<=12_000_000:
            proofpath=ROOT/"data"/f"toe_20261114_MUB_n{n}_s2_{rep}_cadical.drat"
            proofpath.write_text(payload)
        else:
            proofpath=None
    else:proofpath=None
    s.delete()
    return dict(n=n,rep=int(rep),target_maximal_Pauli_MUB_size=size,
       universe_candidates=count,picks_remaining=choose,
       number_CNF_variables=cardinality.nv,
       clause_counts=clause_counts,
       total_clauses=sum(clause_counts.values()),
       deterministic_CNF_clause_SHA256=dig.hexdigest(),
       build_seconds=round(building,3),solver_seconds=round(solving,3),
       CDCL_conflict_budget=conflicts,status=result,
       valid_witness=witness,
       proof_lines=proof_lines,portable_DRAT_path=str(proofpath.relative_to(ROOT)) if proofpath else None,
       proof_boundary="If result is UNDECIDED, no UNSAT claim. If UNSAT, proof still requires independent DRAT checker and confirmation of CNF generator. This does not rely on full 433-million-node DFS.")

def main():
    rows=[]
    # Tiny independent solver controls: 3 qubits size5 EXISTS, size7 UNSAT.
    for size in (5,7):
        for rep in D.prep(3)[-1]:
            r=solve_sat(3,rep,size,100000)
            rows.append(r)
            assert (r["status"]=="SAT_WITNESS")==(size==5)
    # Bigger five-qubit two S3 class reps; a bounded CDCL search
    # documents an independent attempt without mislabeling UNKNOWN.
    for rep in (692,694):
        row=solve_sat(5,rep,8,30000)
        rows.append(row)
        print("REP",rep,row["status"],"clauses",row["total_clauses"],
            "build",row["build_seconds"],"solve",row["solver_seconds"],flush=True)
    classification=("INDEPENDENT_CADICAL_UNSAT_BOTH_CLASSES" if
                    all(x["status"]=="UNSAT_CADICAL" for x in rows[-2:])
                    else "INDEPENDENT_SAT_FRONT_UNDECIDED")
    output=dict(status="PASS_INDEPENDENT_CADICAL_GF2_RANK_CODE_CNF_CONSTRUCTION",
        classification=classification,
        records=rows,
        solver="PySAT CaDiCaL 195 with DRAT logging, conflict-budgeted",
        overall_proof_boundary="The previously reported DFS exclusion is not itself a DRAT/LRAT certificate. A full independently checked no-size8 proof requires UNSAT for both n5 class reps and checker-verified proof logs.")
    OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("FINAL",classification,flush=True)
    return output
if __name__=="__main__":main()
