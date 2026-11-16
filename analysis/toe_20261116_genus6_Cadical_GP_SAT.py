"""Fast CNF/XOR SAT test for generic 12-plane genus-six dual embeddings.

Encode 715 rank4 signs on 13 vectors (12 face planes + vertical) and
25,740 GP 3-term axioms via Tseitin XOR2s, plus 528 11-gon
no-proper-self-crossing clauses. Uses compiled CaDiCaL 1.9.5.

SAT => abstract signed uniform oriented matroid satisfying LOCAL face
simplicity only, not a geometrically realizable polyhedron.
UNSAT => uniform rank4 oriented-matroid local-no-cross necessary
conditions impossible for this ONE abstract triangulation; to claim
formal mathematical proof export independently verifiable DRAT/LRAT.
UNKNOWN => resource budget depleted.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import ast,json,time
from pysat.solvers import Solver
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_genus6_cadical_chirotope_local_sat.json"

def facets():
    tree=ast.parse((ROOT/"analysis"/"w33_genus_six_execution.py").read_text())
    return {tuple(sorted(int(x)-1 for x in f)) for n in tree.body
       if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="FACETS_ONE" for t in n.targets)
       for f in ast.literal_eval(n.value)}

def inv(seq):
    return sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2

def run():
    F=facets();assert len(F)==44
    minors={t:i+1 for i,t in enumerate(combinations(range(13),4))}
    assert len(minors)==715
    N=715; clauses=[];gp=0
    def lit(seq):
        v=minors[tuple(sorted(seq))]
        return -v if inv(seq) else v
    def xor2(x,y):
        nonlocal N
        N+=1;v=N
        # v is xor of Boolean truth of two literals
        clauses.extend([[-x,-y,-v],[x,y,-v],[x,-y,v],[-x,y,v]])
        return v
    def xor_many(values):
        it=iter(values);total=next(it)
        for val in it:total=xor2(total,val)
        return total
    constraints=0
    for i in range(12):
        links={}
        for f in F:
            if i in f:
                x,y=sorted(set(f)-{i})
                links.setdefault(x,set()).add(y)
                links.setdefault(y,set()).add(x)
        assert len(links)==11 and all(len(z)==2 for z in links.values())
        cyc=[min(links),min(links[min(links)])]
        while len(cyc)<11:
            cyc.append(next(iter(links[cyc[-1]]-{cyc[-2]})))
        assert cyc[0] in links[cyc[-1]]
        edges=[(cyc[j],tuple(sorted((i,cyc[j],cyc[(j-1)%11]))),
                     tuple(sorted((i,cyc[j],cyc[(j+1)%11]))))
               for j in range(11)]
        for a,b in combinations(range(11),2):
            if b==a+1 or (a==0 and b==10):continue
            j,f0,f1=edges[a];k,g0,g1=edges[b]
            first=xor_many([lit((*f0,k)),lit((*f0,12)),lit((*f1,k)),lit((*f1,12))])
            second=xor_many([lit((*g0,j)),lit((*g0,12)),lit((*g1,j)),lit((*g1,12))])
            clauses.append([-first,-second])
            constraints+=1
    assert constraints==528
    for a,b in combinations(range(13),2):
        rem=[x for x in range(13) if x not in (a,b)]
        for i,j,k,l in combinations(rem,4):
            p=xor2(lit((a,b,i,j)),lit((a,b,k,l)))
            q=-xor2(lit((a,b,i,k)),lit((a,b,j,l)))
            r=xor2(lit((a,b,i,l)),lit((a,b,j,k)))
            clauses.extend([[p,q,r],[-p,-q,-r]])
            gp+=1
    assert gp==25740
    stats={
      "status":"GENUS6_UNIFORM_RANK4_LOCAL_NO_CROSS_CADICAL_SAT_CONTROL",
      "combinatorial_type":"FACETS_ONE, single member of 59 neighborly genus-six maps",
      "solver":"PySAT CaDiCaL195, brute 3-term Grassmann-Pluecker sign CNF with Tseitin XOR",
      "rank4_chirotope_variables":715,
      "face_local_no_cross_clauses":constraints,
      "grassmann_pluecker_axioms":gp,
      "cnf_variables":N,
      "cnf_clauses":len(clauses),
      "conflict_budget":35000,
      "scope":"A SAT model is an abstract oriented matroid (not necessarily representable over reals); it does not ensure no global face intersections. UNSAT excludes this generic local sign system for one map only; no proof-grade UNSAT absent independently verified proof log. UNKNOWN is inconclusive."
    }
    t=time.monotonic()
    with Solver(name="cadical195",bootstrap_with=clauses,use_timer=True) as sat:
        sat.conf_budget(stats["conflict_budget"])
        ans=sat.solve_limited(expect_interrupt=True)
        stats["solver_result"]={True:"sat",False:"unsat",None:"unknown"}[ans]
        stats["solve_seconds"]=time.monotonic()-t
        if ans:
            model={abs(x):x>0 for x in sat.get_model()}
            assert len(model)>=N
            assert all(any(model[abs(z)]==(z>0) for z in clause) for clause in clauses)
            stats["sat_model_original_minor_neg_sign_bits"]= [
              int(model[minors[t]]) for t in sorted(minors)]
            stats["all_CNF_clauses_independently_satisfied"]=True
        elif ans is False:
            stats["formal_proof_log_exported"]=False
    OUT.write_text(json.dumps(stats,indent=2)+"\n")
    return stats

if __name__=="__main__":
    x=run()
    print("RESULT",x["solver_result"],x["cnf_variables"],x["cnf_clauses"],"seconds",round(x["solve_seconds"],1),flush=True)
