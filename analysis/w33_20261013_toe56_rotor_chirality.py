"""TOE56 physics II: native W33 compact quantum-rotor block and chirality index firewalls.

A *truncated one-plaquette invariant subspace*, not a full quantum gauge theory.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(np.int64)
loop=octs[0]
c=np.rint(cycle_row(loop,ed,volts,look,np.zeros(3)).real).astype(np.int64)
assert int(np.dot(c,c))==8
assert np.array_equal(B.T@c,np.zeros(80,dtype=np.int64))
# Local flux sectors: closed magnetic loop n=m*c, plus a unit
# oriented open edge string q=e_j with charged endpoints.
op=np.zeros(160,dtype=np.int64);op[0]=1
Gopen=B.T@op
assert sorted(Gopen[Gopen!=0].tolist())==[-1,1]
assert int(Gopen.sum())==0
mmax=4;ms=np.arange(-mmax,mmax+1)
spectra={}
for g in (.3,.7,1.1):
 for name,q in (("neutral",np.zeros(160,dtype=np.int64)),("open",op)):
  flux=np.array([m*c+q for m in ms])
  gauss=flux@B
  assert np.max(abs(gauss-gauss[0]))==0
  expected=Gopen if name=="open" else np.zeros(80,dtype=np.int64)
  assert np.array_equal(gauss[0],expected)
  # Polarization E=g n: rotor electric kinetic g²/(2w) * n², here w=1.
  electric=np.sum(flux**2,axis=1)*g*g/2
  # Wilson cosine acts as nearest flux-ladder hopping in this sector.
  mat=np.diag(electric+1/(g*g))
  for j in range(len(ms)-1):
   mat[j,j+1]=mat[j+1,j]=-1/(2*g*g)
  eig=np.linalg.eigvalsh(mat)
  assert np.min(eig)>0 and np.max(abs(mat-mat.T))==0
  spectra[f"{name}_{g}"]={"lowest_energy":float(eig[0]),
    "first_excited_gap":float(eig[1]-eig[0]),
    "flux_sector_endpoint_charge":expected.tolist(),
    "electrically_generated_flux_norm_at_m1":int(np.sum((c+q)**2))}
assert abs(spectra["neutral_0.3"]["lowest_energy"]-spectra["neutral_1.1"]["lowest_energy"])>.01
# Genuine canonical compact angle has theta=g A periodic 2pi and
# conjugate n=E/g integer. Graph alone fixes integer relative charges,
# but cannot fix continuous positive bare g.
# Chiral incidence square-root at the *same native* B(k):
# Q=[[0,B†],[B,0]], gamma=diag(+I80,-I160).
# index(kernel B) - index(kernel B†) = 80-160 = -80
# by finite rank-nullity, irrespective of Bloch twist.
index_rows=[]
for k in ([0.,0.,0.],[.13,.21,-.08]):
  BB=gradient(ed,volts,np.array(k))
  sv=np.linalg.svd(BB,compute_uv=False)
  rank=int(np.count_nonzero(sv>1e-8))
  kp=80-rank;km=160-rank
  assert kp-km==-80
  index_rows.append({"Bloch_k":k,"rank_incidence":rank,
    "vertex_positive_chiral_zero_modes":kp,
    "edge_negative_chiral_zero_modes":km,
    "index":kp-km})
# Index -80 is an unavoidable artifact of having 80 vs 160 basis
# orbitals. This cannot be interpreted as 80 Weyl families.
out={"status":"PASS_TOE56_FINITE_NATIVE_QUANTUM_ROTOR_AND_CHIRAL_INDEX_GATES",
"selected_native_local_plaquette_length":int(np.dot(c,c)),
"int_boundary_of_native_loop_zero":int(np.max(abs(B.T@c))),
"quantum_plaquette_flux_basis":"States |m c + q>, m=-4..4, c signed native 8-link octagon; q=0 vacuum or one oriented open edge flux. Each sector remains in one fixed Gauss-charge eigenspace.",
"quantum_truncated_H":"H=g²/2 sum_links n²/w + (1/g²)[I-(S+S†)/2] for the selected plaquette only, with w=1 and open-end finite flux truncation.",
"quantum_sector_spectra":spectra,
"quantum_coupling_gate":"Electric energy scales g²; Wilson magnetic hopping scales g^-2. Flux compactness quantizes relative U1 charge, but a continuum of bare positive g remains. The full 1385-plaquette lattice with all link/matter rotor sectors has not been diagonalized.",
"native_bloch_chiral_index":index_rows,
"chiral_theorem":"The 240x240 local incidence Dirac operator Q=[[0,B†],[B,0]] has block-chiral index dim(ker B)-dim(ker B†)=80-160=-80 for ANY B of size 160x80, regardless of k, gauge phase or interactions that preserve off-diagonal dimensions. This is orbital-sublattice imbalance, not a 3+1D Weyl-fermion generation count, gauge anomaly, or spectral-flow index on a growing 4D lattice.",
"physics_limits":"No dynamical 4D spinor regulator, overlap/Ginsparg-Wilson operator, chiral Standard Model matter, physical electric charge or full quantized interacting W33 compact gauge Hilbert space is established.",
"prior_art":"Kogut-Susskind 1975 compact electric flux gauge Hamiltonian; standard finite bipartite Dirac rank-nullity and Nielsen-Ninomiya/Ginsparg-Wilson lattice chirality distinction."}
(R/"data/w33_20261013_toe56_rotor_chirality.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"energies":{k:round(v["lowest_energy"],7) for k,v in spectra.items()},
"chiral":index_rows},indent=2))
