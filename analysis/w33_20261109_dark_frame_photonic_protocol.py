#!/usr/bin/env python3
"""Prepare a native 40-port W33 dark-frame column with a balanced binary tree.

Exact photon probabilities: 1 center *3/8, 12 neighbors *1/24,
27 other points *1/216. 39 two-mode splits in 6 layers plus 12 pi
phase flips, with arbitrary mode-pair access. Full 80-mode Hamiltonian
dynamics predicts zero line clicks; single-edge flux and differential
loss create analytically known t² leakage. No fabricated apparatus.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261109_flux_dark_mode_fragility import build

def build_balanced_tree(target):
    probs=abs(target)**2
    assert len(probs)==40
    layers=[[] for _ in range(math.ceil(math.log2(len(probs))))]
    psi=np.zeros(40);psi[0]=1.
    def recurse(nodes,depth):
        if len(nodes)==1:return
        half=(len(nodes)+1)//2
        left,right=nodes[:half],nodes[half:]
        a,b=left[0],right[0]
        pm=sum(probs[i] for i in nodes)
        pleft=sum(probs[i] for i in left);pright=sum(probs[i] for i in right)
        c=math.sqrt(pleft/pm);s=math.sqrt(pright/pm)
        x,y=psi[a],psi[b]
        psi[a]=c*x-s*y;psi[b]=s*x+c*y
        layers[depth].append((a,b,c,s,pleft,pright))
        recurse(left,depth+1)
        recurse(right,depth+1)
    recurse(list(range(40)),0)
    assert sum(map(len,layers))==39
    assert np.max(abs(psi-np.sqrt(probs)))<1e-13
    negative=np.where(target<-1e-13)[0]
    psi[negative]*=-1
    assert np.max(abs(psi-target))<1e-13
    return layers,negative.tolist(),psi

def main(path=None):
    B,edges,G=build()
    A=B@B.T-4*np.eye(40)
    P=(8*np.eye(40)-4*A+np.ones((40,40)))/24
    i=0
    psi=P[:,i]/math.sqrt(3/8)
    assert np.max(abs(P@psi-psi))<1e-13
    assert np.linalg.norm(B.T@psi)<1e-13
    p=abs(psi)**2
    adj=A[:,i]>0
    selfmask=np.arange(40)==i
    non=(~adj)&(~selfmask)
    assert int(sum(adj))==12 and int(sum(non))==27
    assert max(abs(p[selfmask]-3/8))<1e-13
    assert max(abs(p[adj]-1/24))<1e-13
    assert max(abs(p[non]-1/216))<1e-13
    layers,phaseports,reconstructed=build_balanced_tree(psi)
    assert len(phaseports)==12
    assert [len(x) for x in layers]==[1,2,4,8,16,8]
    n=40
    H0=np.block([[np.zeros((n,n)),B],[B.T,np.zeros((n,n))]])
    start=np.r_[psi,np.zeros(n)]
    for t in (.05,.25,1.):
        out=expm(-1j*t*H0)@start
        assert np.max(abs(out-start))<1e-12

    theta=math.pi/5
    a,b=edges[0]
    T=B.astype(complex);T[a,b]=np.exp(1j*theta)
    Hphi=np.block([[np.zeros((n,n)),T],[T.conj().T,np.zeros((n,n))]])
    out_phi=[]
    coeff=(3/2)*math.sin(theta/2)**2
    for t in (.005,.02,.05,.1):
        u=expm(-1j*t*Hphi)@start
        actual=float(np.linalg.norm(u[n:])**2)
        predicted=coeff*t*t
        out_phi.append({"time_dimensionless":t,"exact_line_click_probability":actual,
                        "leading_t2_prediction":predicted,
                        "relative_t4_correction":float(actual/predicted-1)})
    assert max(abs(x["relative_t4_correction"]) for x in out_phi)<.04

    eta=.90
    D=np.eye(n);D[0,0]=math.sqrt(eta)
    atten=D@psi
    source_survival=float(atten@atten)
    line_norm=float(np.linalg.norm(B.T@atten)**2)
    predicted_loss=(3/2)*(1-math.sqrt(eta))**2
    assert abs(line_norm-predicted_loss)<1e-13
    assert abs(source_survival-(1-(3/8)*(1-eta)))<1e-13
    normed=atten/math.sqrt(source_survival)
    Ht=.02
    propagated=expm(-1j*Ht*H0)@np.r_[normed,np.zeros(n)]
    actualclick=float(np.linalg.norm(propagated[n:])**2)
    predictedclick=Ht**2*line_norm/source_survival
    assert abs(actualclick/predictedclick-1)<.002
    out={
      "status":"PASS_W33_DARK_FRAME_39_COUPLER_SIX_LAYER_PREP_AND_NULL_FALSIFIERS",
      "selected_point":0,
      "target_state_dimensionality":40,
      "target_intensities":{
        "central":{"count":1,"per_mode":"3/8","total":"3/8"},
        "12_collinear":{"count":12,"per_mode":"1/24","total":"1/2"},
        "27_noncollinear":{"count":27,"per_mode":"1/216","total":"1/8"}},
      "signed_amplitude_formula":"psi = P_dark[:,0]/sqrt(3/8); negative real phases on precisely the 12 collinear neighbors",
      "balanced_binary_split_layers":[len(x) for x in layers],
      "two_mode_tunable_splits":sum(len(x) for x in layers),
      "max_split_depth":len(layers),
      "required_pi_phase_corrections":len(phaseports),
      "phase_corrected_ports":phaseports,
      "max_state_preparation_amplitude_error":float(np.max(abs(reconstructed-psi))),
      "unperturbed_H_exact_no_line_leakage_at_tested_times":True,
      "incident_edge_phase_detuning":{"point":a,"line":b,"theta":theta,
               "leading_line_click_probability_coefficient":coeff,
               "finite_time_controls":out_phi},
      "differential_preparation_loss":{
          "central_port_intensity_survival":eta,
          "unconditional_total_photon_survival":source_survival,
          "exact_t2_raw_line_leakage_coefficient":line_norm,
          "exact_t2_formula":"(3/2)(1-sqrt(eta))²",
          "conditional_survival_t2_coefficient":line_norm/source_survival,
          "finite_time":Ht,
          "conditional_line_probability":actualclick,
          "leading_conditional_prediction":predictedclick},
      "physical_implementation_caveats":"The six-layer 39-coupler construction assumes arbitrary two-mode pairing by layer; actual photonic layout requires routing, coherent single-photon injection, coupler calibration, phase masks, memory, 80-mode unitary Hamiltonian synthesis and detector efficiency. Source total throughput and reference photons not modeled. Exact interference null alone does not demonstrate TOE, quantum advantage or any new physical law.",
      "prior_art_scope":"Balanced binary linear-optical state preparation, strongly regular graph tight frames, dark states and first-order perturbation theory are established mathematics; this is one explicit W33 test target."
      }
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("W33_DARK_PREP",json.dumps({"split_depth":len(layers),"splits":sum(map(len,layers)),
            "phase_ports":len(phaseports),"center":p[0],
            "leakage_theta":coeff,"loss_conditional_t2":line_norm/source_survival}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
