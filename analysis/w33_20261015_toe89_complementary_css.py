"""TOE89 complementary X/Z qutrit syndrome circuits and flag hooks.

All 99 Z face checks and 27 X incidence checks mutually commute.
Compile qutrit SUM^w gates for each, add paired pre/post flag ancilla
couplings, and repeat 3 rounds with Pauli-frame faults. A per-check
Viterbi time filter is a baseline *not* a full spacetime CSS decoder.
"""
from __future__ import annotations
import collections,json,random
from analysis.w33_20261015_toe85_h2_relation_module import ROOT,geometry
from analysis.w33_20261015_toe86_geometry_integral_routing import native
SHOTS=144;ROUNDS=3;SEED=891991
RATE={"data_X":.00025,"data_Z":.00025,
      "Z_ancilla_Z_hook":.00065,"X_ancilla_X_hook":.00065,
      "digit_readout":.0015,"idle_X":.00010,"idle_Z":.00010}

def checks():
    _,HZ,_=geometry()
    tri,edges,ei,perms,orbits=native()
    HX=[[0]*135 for _ in range(27)]
    for j,(u,v) in enumerate(edges):
        HX[u][j]=2
        HX[v][j]=1
    assert all(sum(a*b for a,b in zip(hz,hx))%3==0 for hz in HZ for hx in HX)
    return HX,HZ
def make_layers(rows):
    jobs=[(i,j,v%3) for i,row in enumerate(rows) for j,v in enumerate(row) if v%3]
    layers=[]
    for f,e,w in jobs:
        for layer in layers:
            if all(f!=a and e!=b for a,b,c in layer):
                layer.append((f,e,w));break
        else:layers.append([(f,e,w)])
    assert all(len({f for f,e,w in layer})==len(layer) and
               len({e for f,e,w in layer})==len(layer) for layer in layers)
    return layers
def matvec(rows,v):
    return [sum(a*b for a,b in zip(row,v))%3 for row in rows]
def synd_lookup(rows):
    out={}
    for j in range(135):
        for c in (1,2):
            v=tuple((c*row[j])%3 for row in rows)
            if v in out:out[v]=None
            else:out[v]=(j,c)
    return out

def viterbi_latest(records,penalty=3):
    # ternary hidden syndrome s_t with a unit mismatch cost and a
    # larger per-change cost. Assumes arbitrary per-check Markov drift,
    # ignores coupled stabilizers and nonuniform fault likelihoods.
    out=[]
    for i in range(len(records[0])):
        cost=[int(v!=0)*penalty+int(v!=records[0][i]) for v in range(3)]
        trace=[]
        for t in range(1,len(records)):
            new=[];ptr=[]
            for v in range(3):
                arr=[cost[u]+penalty*int(u!=v)+int(v!=records[t][i])
                     for u in range(3)]
                which=min(range(3),key=lambda u:arr[u])
                new.append(arr[which]);ptr.append(which)
            cost=new;trace.append(ptr)
        out.append(min(range(3),key=lambda v:cost[v]))
    return out

def simulate(HX,HZ,Xlayers,Zlayers,flags,seed):
    rng=random.Random(seed)
    sx=synd_lookup(HZ);sz=synd_lookup(HX)
    X=[0]*135;Z=[0]*135
    observed_x=[];observed_z=[]
    hook_total=0;hook_flagged=0;flags_total=0
    for t in range(ROUNDS):
        for j in range(135):
            if rng.random()<RATE["idle_X"]:X[j]=(X[j]+rng.choice((1,2)))%3
            if rng.random()<RATE["idle_Z"]:Z[j]=(Z[j]+rng.choice((1,2)))%3
        # X checks: ancilla controls data, measured in X basis.
        ax=[0]*27;az=[0]*27;flagX=[0]*27
        for layer in Xlayers:
            for f,e,w in layer:
                X[e]=(X[e]+w*ax[f])%3
                az[f]=(az[f]-w*Z[e])%3
                if rng.random()<RATE["X_ancilla_X_hook"]:
                    ax[f]=(ax[f]+rng.choice((1,2)))%3
                    hook_total+=1
                if rng.random()<RATE["data_Z"]:
                    Z[e]=(Z[e]+rng.choice((1,2)))%3
        # physical paired flag SUM(anc->flag) of ±1; pre acted
        # trivially on fresh zero Pauli frame, post detects ax.
        if flags:flagX=[(-x)%3 for x in ax]
        ox=[(-z)%3 for z in az]
        # Z checks: data controls ancilla, measured in Z basis.
        zx=[0]*99;zz=[0]*99;flagZ=[0]*99
        for layer in Zlayers:
            for f,e,w in layer:
                zx[f]=(zx[f]+w*X[e])%3
                Z[e]=(Z[e]-w*zz[f])%3
                if rng.random()<RATE["Z_ancilla_Z_hook"]:
                    zz[f]=(zz[f]+rng.choice((1,2)))%3
                    hook_total+=1
                if rng.random()<RATE["data_X"]:
                    X[e]=(X[e]+rng.choice((1,2)))%3
        if flags:flagZ=zz[:]
        oz=zx[:]
        for row in (ox,oz):
            for i in range(len(row)):
                if rng.random()<RATE["digit_readout"]:
                    row[i]=(row[i]+rng.choice((1,2)))%3
        observed_x.append(ox);observed_z.append(oz)
        flagged=sum(v!=0 for v in flagX)+sum(v!=0 for v in flagZ)
        flags_total+=flagged
        hook_flagged+=int(flagged>0)
    def correct(v,lookup,syn):
        out=v[:]
        if tuple(syn) in lookup and lookup[tuple(syn)] is not None:
            j,c=lookup[tuple(syn)];out[j]=(out[j]-c)%3
        return out
    def zero_residual(x_syn,z_syn):
        cx=correct(X,sx,z_syn)
        cz=correct(Z,sz,x_syn)
        return not any(cx) and not any(cz)
    finalX=matvec(HX,Z);finalZ=matvec(HZ,X)
    # Actual syndrome can differ from last measured one because hook
    # errors happened AFTER complementary checks in same round.
    return {"nonzero_data_X":bool(any(X)),"nonzero_data_Z":bool(any(Z)),
            "any_hook_injected":hook_total>0,
            "hook_faults_count":hook_total,
            "nonzero_flag_qudits_count":flags_total,
            "any_flag_detected":hook_flagged>0,
            "final_true_X_syndrome_nonzero":bool(any(finalX)),
            "final_true_Z_syndrome_nonzero":bool(any(finalZ)),
            "raw_zero_physical_residual":zero_residual(observed_x[-1],observed_z[-1]),
            "temporal_filtered_zero_physical_residual":zero_residual(
                viterbi_latest(observed_x),viterbi_latest(observed_z))}
def certificate():
    HX,HZ=checks()
    Xlayers=make_layers(HX);Zlayers=make_layers(HZ)
    assert sum(len(x) for x in Xlayers)==270
    assert sum(len(x) for x in Zlayers)==351
    def verify_basis_error():
        for j in (0,13,134):
            for c in (1,2):
                x=[0]*135;z=[0]*135;x[j]=c;z[j]=c
                assert matvec(HZ,x)==[(c*v)%3 for v in [row[j] for row in HZ]]
                assert matvec(HX,z)==[(c*v)%3 for v in [row[j] for row in HX]]
    verify_basis_error()
    runs=[]
    for enabled in (False,True):
        samples=[simulate(HX,HZ,Xlayers,Zlayers,enabled,SEED+i) for i in range(SHOTS)]
        metrics={k:sum(float(v[k]) for v in samples)/SHOTS
                 for k in samples[0]}
        runs.append({"flag_ancillas_enabled":enabled,"shots":SHOTS,
                     "means":metrics})
        print("CSS",enabled,"Xlayers",len(Xlayers),"Zlayers",len(Zlayers),
              "hooks",metrics["any_hook_injected"],
              "flags",metrics["any_flag_detected"],
              "raw",metrics["raw_zero_physical_residual"],
              "filtered",metrics["temporal_filtered_zero_physical_residual"],flush=True)
    # With the same seeds flags only observe faults: they do not
    # magically correct data or modify the actual syndrome.
    for k,v in runs[0]["means"].items():
        if not k.startswith(("any_flag","nonzero_flag")):
            assert abs(v-runs[1]["means"][k])<1e-12
    assert runs[1]["means"]["any_flag_detected"]>0
    assert runs[0]["means"]["nonzero_flag_qudits_count"]==0
    return {"status":"STOCHASTIC_TOY_CSS_CIRCUIT_AND_EXACT_COMMUTATION",
            "data_qutrits":135,"Z_face_checks":99,"X_vertex_checks":27,
            "round_count":ROUNDS,"shots_per_case":SHOTS,
            "Z_SUM_gates_per_round":351,"X_SUM_gates_per_round":270,
            "Z_conflict_free_layers":len(Zlayers),
            "X_conflict_free_layers":len(Xlayers),
            "flag_qudits_per_round_when_enabled":126,
            "flag_prepost_SUM_gates_per_round":2*126,
            "rates":RATE,"runs":runs,
            "limits":"Flag pre/post couplings are ideal noiseless, pre interaction acts trivially in the fresh Pauli frame. No actual flag-aware decoder implemented; viterbi per check is NOT a full spacetime decoder. No X/Z parity measurement gadget calibration, no logical failure or threshold."}
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe89_complementary_css.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
