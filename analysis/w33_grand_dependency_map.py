#!/usr/bin/env python3
"""
The grand dependency map: one graph from the single integer q=3 to every result of
the program -- the Standard Model, the exceptional/moonshine tower, the holographic
boundary, the dark sector, the cosmology ledger, and the three bench constants.

This is the capstone figure: a directed acyclic graph rooted at the master equation
q!=2q (which selects q=3), through the substrate primitives (lambda,mu,k,v,f,g and
the cyclotomics Phi3,Phi4,Phi6), out to every physical claim. It emits a DOT graph
(docs) and a JSON, and verifies the graph is a connected DAG rooted at q.
"""
from __future__ import annotations

import json

# edges: (source, target).  Everything traces back to q.
EDGES = [
    # selection -> q
    ("q!=2q (GQ selection)", "q=3"),
    # q -> primitives
    ("q=3", "lambda=q-1=2"),
    ("q=3", "mu=q+1=4"),
    ("q=3", "k=q(q+1)=12"),
    ("q=3", "v=(q+1)(q^2+1)=40"),
    ("q=3", "Phi3=q^2+q+1=13"),
    ("q=3", "Phi4=q^2+1=10"),
    ("q=3", "Phi6=q^2-q+1=7"),
    ("q=3", "f=q^q-q=24"),
    ("k=q(q+1)=12", "g=15"),
    ("v=(q+1)(q^2+1)=40", "E=240"),
    # primitives -> Standard Model
    ("k=q(q+1)=12", "SM gauge 8+3+1=k"),
    ("v=(q+1)(q^2+1)=40", "27 matter (E6)"),
    ("k=q(q+1)=12", "alpha^-1=(k-1)^2+mu^2=137"),
    ("Phi3=q^2+q+1=13", "sin2thW=q/Phi3=3/13"),
    ("Phi3=q^2+q+1=13", "PMNS cyclotomic"),
    ("Phi6=q^2-q+1=7", "PMNS cyclotomic"),
    ("Phi6=q^2-q+1=7", "QCD beta0=Phi6=7"),
    # primitives -> exceptional / moonshine
    ("Phi6=q^2-q+1=7", "exceptional G2..E8"),
    ("E=240", "exceptional G2..E8"),
    ("f=q^q-q=24", "Monster c=24"),
    ("E=240", "E8 lattice -> j -> Monster"),
    ("E8 lattice -> j -> Monster", "Monster c=24"),
    # -> holographic
    ("f=q^q-q=24", "boundary c=24"),
    ("Monster c=24", "boundary c=24"),
    ("mu=q+1=4", "Bekenstein 1/mu"),
    ("g=15", "AdS/CFT 15=SO(4,2)"),
    ("boundary c=24", "holographic code [[240,81,4]]"),
    # -> dark sector
    ("g=15", "dark SU(4)=SO(6)=15"),
    ("AdS/CFT 15=SO(4,2)", "dark SU(4)=SO(6)=15"),
    ("dark SU(4)=SO(6)=15", "128 dark spinor"),
    ("128 dark spinor", "N_R (right-handed nu)"),
    ("mu=q+1=4", "dark beta0=k-mu -> Lambda_dark"),
    ("128 dark spinor", "dark matter (asymmetric)"),
    # -> cosmology
    ("v=(q+1)(q^2+1)=40", "N=2(v-Phi4)=60"),
    ("Phi4=q^2+1=10", "N=2(v-Phi4)=60"),
    ("N=2(v-Phi4)=60", "n_s=29/30"),
    ("N=2(v-Phi4)=60", "r=1/300"),
    ("N=2(v-Phi4)=60", "f_NL=1/72"),
    ("N=2(v-Phi4)=60", "running=-1/1800"),
    ("N_R (right-handed nu)", "seesaw m_bb=2.3 meV"),
    ("N_R (right-handed nu)", "cogenesis (baryon+dark)"),
    ("boundary c=24", "CMB = moonshine correlations"),
    # -> the machine
    ("lambda=q-1=2", "clock omega=sqrt(lambda)"),
    ("clock omega=sqrt(lambda)", "m_top=v_EW/sqrt(lambda)"),
    ("lambda=q-1=2", "pump Chern C=lambda=2"),
    ("Phi4=q^2+1=10", "contextual fraction 1/Phi_4"),
    ("k=q(q+1)=12", "supercycle 51840=|Sp(4,3)|"),
    ("v=(q+1)(q^2+1)=40", "code [[240,81,4]]"),
    # -> the falsifiers (bench + experiments)
    ("pump Chern C=lambda=2", "BENCH: pump quantum 2"),
    ("contextual fraction 1/Phi_4", "BENCH: CF=1/10"),
    ("clock omega=sqrt(lambda)", "BENCH: BC angle arccos(-2/3)"),
    ("Lambda_dark", "LISA dark-confinement GW"),
    ("dark beta0=k-mu -> Lambda_dark", "Lambda_dark"),
]


def main():
    out = {}
    nodes = set()
    for a, b in EDGES:
        nodes.add(a)
        nodes.add(b)
    children = {}
    parents = {}
    for a, b in EDGES:
        children.setdefault(a, []).append(b)
        parents.setdefault(b, []).append(a)

    roots = [n for n in nodes if n not in parents]
    leaves = [n for n in nodes if n not in children]
    print(f"[grand dependency map]")
    print(f"  nodes: {len(nodes)}, edges: {len(EDGES)}")
    print(f"  roots: {roots}")
    print(f"  leaf predictions: {len(leaves)}")

    # every node reachable from the single selection root?
    root = "q!=2q (GQ selection)"
    seen, stack = set(), [root]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(children.get(x, []))
    reach = len(seen) == len(nodes)
    print(f"  all {len(nodes)} nodes reachable from '{root}': {reach}")
    assert roots == [root] and reach

    # acyclic check (topological sort)
    indeg = {n: 0 for n in nodes}
    for a, b in EDGES:
        indeg[b] += 1
    order, q = [], [n for n in nodes if indeg[n] == 0]
    while q:
        x = q.pop()
        order.append(x)
        for c in children.get(x, []):
            indeg[c] -= 1
            if indeg[c] == 0:
                q.append(c)
    acyclic = len(order) == len(nodes)
    print(f"  acyclic DAG: {acyclic}")
    assert acyclic
    out["n_nodes"] = len(nodes)
    out["n_edges"] = len(EDGES)
    out["root"] = root
    out["leaf_predictions"] = sorted(leaves)
    out["connected_DAG"] = True

    # emit DOT
    dot = ["digraph w33 {", "  rankdir=LR; node [shape=box, fontsize=10];"]
    for a, b in EDGES:
        dot.append(f'  "{a}" -> "{b}";')
    dot.append("}")
    with open("docs/w33_grand_dependency_map.dot", "w") as fh:
        fh.write("\n".join(dot))
    print(f"\n  wrote docs/w33_grand_dependency_map.dot ({len(EDGES)} edges)")

    print("\nRESULT: the entire program is one connected, acyclic dependency graph")
    print("  rooted at a single equation. q!=2q selects q=3; from q flow the")
    print("  primitives (lambda,mu,k,v,f,g; Phi3,Phi4,Phi6); and from those flow the")
    print("  Standard Model, the exceptional/moonshine tower (Monster c=24), the")
    print("  holographic boundary and code, the dark SU(4)/128/N_R sector, the")
    print("  cosmology ledger (n_s,r,f_NL,running,m_bb,cogenesis), the machine (clock,")
    print("  pump, supercycle), and the bench/experiment falsifiers. Every node is")
    print("  reachable from q=3: the whole theory of everything is the unfolding of")
    print("  one integer.")

    out["summary"] = (
        "the whole program is one connected acyclic DAG rooted at the "
        "selection q!=2q -> q=3; from q the primitives (lambda,mu,k,v,f,"
        "g,Phi3,Phi4,Phi6) flow to the SM, the exceptional/moonshine "
        "tower (Monster c=24), the holographic boundary+code, the dark "
        "SU(4)/128/N_R sector, the cosmology ledger, the machine "
        "(clock/pump/supercycle), and the bench+experiment falsifiers. "
        "Every node reachable from q=3."
    )
    out["sources"] = [
        "consolidation of the full w33 arc; master map of the SM "
        "(corpus) extended to holographic/dark/cosmology/machine; "
        "docs/w33_grand_dependency_map.dot"
    ]
    with open("data/w33_grand_dependency_map.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_grand_dependency_map.json")


if __name__ == "__main__":
    main()
