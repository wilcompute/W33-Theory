"""TOE61 active magnetic rank/decoding audit in FULL Pass11969 Gauss compiler.

This checks ALL 1385 declared Wilson rows and all 160 matter hops for
one half-filled background configuration, not the full quantum spectrum.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_pass11969_full_native_gauss_compiler import NativeGaussCompiler
c=NativeGaussCompiler()
bits=sum(1<<i for i in range(80) if c.background[i])
state=(bits,tuple(0 for _ in range(81)))
flux=c.flux(state)
assert np.max(abs(c.B.T@flux+c.background-c.background))==0
zero_row=[];unique=[];seen={}
for j in range(len(c.P)):
 step=tuple(int(x) for x in c.P[j,c.chords])
 if not any(step):zero_row.append(j)
 else:
  canon=min(step,tuple(-x for x in step))
  seen[canon]=seen.get(canon,0)+1
  unique.append(j)
 assert c.plaquette(state,j,1)[0]==bits
 assert c.plaquette(state,j,-1)[0]==bits
 target=c.plaquette(state,j,1)
 assert np.array_equal(c.B.T@c.flux(target),c.B.T@flux)
 assert c.plaquette(target,j,-1)==state
assert len(zero_row)==3 and len(unique)==1382
assert max(seen.values())==1
print('TOE61 magnetic',len(unique),'identity rows',zero_row,flush=True)
# One staggered vacuum has exactly one occupied end per oriented edge,
# so ALL 160 single-link fermion hopping transitions exist.
transitions=[]
for j in range(len(c.edges)):
 hit=c.hop(state,j)
 assert hit is not None
 new,sign,direction=hit
 assert abs(sign)==1 and abs(direction)==1
 assert new[0].bit_count()==40
 assert np.array_equal(c.B.T@c.flux(new)+c.occupation(new[0])-c.background,
                       np.zeros(80,int))
 assert c.hop(new,j)[0]==state
 transitions.append(j)
assert len(transitions)==160
# Plaquette and fermion hop commute as transformations of occupation
# and chord link-flux vectors on a fixed compact gauge Hilbert space.
for j in (0,37,159):
 hop_state,*_=c.hop(state,j)
 for row in (0,186,164,1382,1384):
  first=c.plaquette(hop_state,row,+1)
  from_wilson=c.plaquette(state,row,+1)
  second,*_=c.hop(from_wilson,j)
  assert first==second
out={'status':'PASS_TOE61_FULL_DECLARED_GAUSS_OPERATOR_AUDIT',
'full_native_sites':80,'native_links':160,'chord_integer_flux_coordinates':81,
'declared_wilson_rows':1385,'nonidentity_native_wilson_flux_shifts':len(unique),
'exact_identity_rows':zero_row,'pairwise_unique_active_plaquette_shifts_up_to_sign':len(seen),
'tested_nonzero_fermion_hops':len(transitions),
'exact_gauss_invariance_of_all_plaquette_shifts':True,
'exact_local_gauss_invariance_of_all_160_fermion_hops':True,
'fermion_hopping_wilson_commutation_checks_pass':True,
'interpretation':"The three formally added TOE38 deck commutator 2-cells have ZERO signed native 160-link chain at k=0. Hence the Pass11969 full finite-graph Hamiltonian lists 1385 plaquette rows but only 1382 distinct NONTRIVIAL flux-shift operators; the last three rows are identity with zero magnetic excitation for the standard (1−cos P·A) term. In a nonzero Bloch representation they may carry additional holonomy structure; static k0 identities must not be counted as interacting plaquettes.",
'physical_limits':"Exact audit of operator actions at one checkerboard Fock state (all 160 legal hops) and all plaquette moves, not diagonalization of full 2^80 fermionic Hilbert, charge screening, a chiral Weyl theory, dynamical Lorentz continuum or a physical experimental prediction.",
'prior':"TOE38 constructed 1382 local octagons plus 3 formal commutators, and Pass11969 constructed the full Gauss compiler. This audits their physical active operator count, without claiming the earlier constructs as new."}
(R/'data/w33_20261013_toe61_full_gauss_audit.json').write_text(json.dumps(out,indent=2)+'\n')
