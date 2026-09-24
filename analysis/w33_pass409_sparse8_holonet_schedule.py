#!/usr/bin/env python3
"""Pass 409: exact optimal Holonet schedule for the minimal 8-root compact-E8 frame."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_pass409_sparse8_holonet_schedule.json"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

dw=load(ROOT/"analysis/w33_diagonal_weld_e8_lie_generation.py","dw")
ri=load(ROOT/"analysis/w33_e8_split_real_form_involution.py","ri")
compiler,bridge,table=dw.load_inputs()
vecs=dw.source_generators(compiler,dw.backgrounds(bridge))
sc=json.loads((ROOT/"artifacts/e8_structure_constants_w33_discrete.json").read_text())
sparse=json.loads((ROOT/"data/w33_20260923_compact_e8_sparse8.json").read_text())
micro=json.loads((ROOT/"data/bt1407_microframe_transaction_composer.json").read_text())
assert sparse["exact_Q"]["dimension"]==248 and micro["verified"]

roots=[tuple(map(int,r)) for r in sc["basis"]["roots"]]
rmap={r:8+i for i,r in enumerate(roots)}
neg={8+i:rmap[tuple(-x for x in r)] for i,r in enumerate(roots)}
phase={i:(-1 if ri.killing(sc,i,neg[i])>0 else 1) for i in range(8,248)}
support=list(map(int,sparse["support"]))
base=vecs[(1,"plus")]

maps=compiler["coordinate_maps"]
g1={int(src):row for row,src in enumerate(maps["grade1_source_indices"])}
g2={int(src):row for row,src in enumerate(maps["grade2_source_indices"])}
addresses={int(i):tuple(map(int,h))
           for i,h in bridge["maps"]["e6id_to_current_H27_address"].items()}

def bracket(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():
            if i==j: continue
            sign=1 if i<j else -1
            for k,c in table.get((min(i,j),max(i,j)),()):
                out[k]=out.get(k,0)+sign*x*y*c
                if out[k]==0: del out[k]
    return out

def atom(src,kind):
    a=int(base[src]); s=phase[src]
    row=g1[src]; assert g2[neg[src]]==row
    eid,external=divmod(row,3)
    return {
      "source":src,"partner":neg[src],"coefficient":a,
      "partner_coefficient":s*a if kind=="A" else -s*a,
      "root":list(roots[src-8]),"H27_address":list(addresses[eid]),
      "external_trit":external,"row":row,
    }

def vector(atom):
    return {atom["source"]:atom["coefficient"],
            atom["partner"]:atom["partner_coefficient"]}

def exact_coloring(G):
    order=sorted(G.nodes(),key=lambda v:G.degree(v),reverse=True)
    colors={}; best=[len(order)+1,None]
    def dfs(t,used):
        if used>=best[0]: return
        if t==len(order):
            best[:]=[used,dict(colors)]; return
        v=order[t]
        forbidden={colors[u] for u in G.neighbors(v) if u in colors}
        for c in range(used):
            if c not in forbidden:
                colors[v]=c; dfs(t+1,used); del colors[v]
        colors[v]=used; dfs(t+1,used+1); del colors[v]
    dfs(0,0)
    return best

schedules={}
for kind in ("A","B"):
    atoms=[atom(src,kind) for src in support]
    vecs8=[vector(a) for a in atoms]
    G=nx.Graph(); G.add_nodes_from(range(8))
    for i in range(8):
        for j in range(i+1,8):
            if bracket(vecs8[i],vecs8[j]): G.add_edge(i,j)
    chi,coloring=exact_coloring(G)
    clique=max(map(len,nx.find_cliques(G)))
    assert chi==3 and clique==3
    batches=[]
    for c in range(chi):
        ids=sorted(i for i,v in coloring.items() if v==c)
        for ii,i in enumerate(ids):
            for j in ids[ii+1:]:
                assert not bracket(vecs8[i],vecs8[j])
        batches.append({
          "color":c,"atom_ids":ids,
          "sources":[support[i] for i in ids],
          "all_commute":True,
        })
    schedules[kind]={
      "atoms":atoms,"conflict_edges":sorted([list(e) for e in G.edges()]),
      "clique_lower_bound":clique,"chromatic_number":chi,
      "batches":batches,
    }

assert schedules["A"]["conflict_edges"]==schedules["B"]["conflict_edges"]

ticks_per_microframe=len(micro["frame_tick_summary"])
microframes_per_cycle=schedules["A"]["chromatic_number"]+schedules["B"]["chromatic_number"]
ticks_per_cycle=ticks_per_microframe*microframes_per_cycle
assert microframes_per_cycle==6 and ticks_per_cycle==432
assert 30 % microframes_per_cycle==0
assert 2160 % ticks_per_cycle==0
assert 51840 % ticks_per_cycle==0

out={
 "schema":"w33.pass409.sparse8_holonet_schedule.v1",
 "status":"PASS_MINIMAL_EIGHT_ROOT_COMPACT_E8_FRAME_HAS_OPTIMAL_SIX_MICROFRAME_AB_CYCLE",
 "support":support,
 "schedules":schedules,
 "microframes_per_AB_cycle":microframes_per_cycle,
 "ticks_per_microframe":ticks_per_microframe,
 "ticks_per_AB_cycle":ticks_per_cycle,
 "AB_cycles_per_30_microframe_Coxeter_bus":30//microframes_per_cycle,
 "AB_cycles_per_2160_tick_bus":2160//ticks_per_cycle,
 "AB_cycles_per_51840_tick_window":51840//ticks_per_cycle,
 "optimality":"Each control conflict graph contains a 3-clique and admits an explicit 3-coloring, so three commuting batches per control are necessary and sufficient.",
 "hardware_reduction":{"dense_atoms_per_control":81,"minimal_atoms_per_control":8,
                       "dense_microframes_per_AB_cycle":30,"minimal_microframes_per_AB_cycle":6},
 "boundary":"This is an exact scheduling/commutation theorem. ROOT_PLANE_ANALOG amplitudes and optical calibration remain physical implementation requirements."
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],"microframes":microframes_per_cycle,
                  "ticks":ticks_per_cycle,
                  "cycles_per_Coxeter_bus":out["AB_cycles_per_30_microframe_Coxeter_bus"]},indent=2))
