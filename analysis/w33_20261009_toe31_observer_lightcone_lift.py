"""Round31 finite AdS tangent Minkowski cone: explicit spatial unwrapping.

Q(x,y,z,t)=x²+y²+z²-t² mod3 has 20 nonzero null rays.
Observer temporal orientation selects 6 of the 20 (t=+1),
rejects 8 null equal-time rays and six backward-time rays.
Lift Z3³ to Z³ -> L1 expanding cones; EXTENSION, not emergence.
"""
import itertools,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe31_observer_lightcone_lift.json'
def run():
 vectors=list(itertools.product((0,1,2),repeat=4))
 null=[v for v in vectors if v!=(0,0,0,0) and (sum(v[i]*v[i] for i in range(3))-v[3]*v[3])%3==0]
 assert len(null)==20
 grouped={str(t):[v for v in null if v[3]==t] for t in (0,1,2)}
 assert [len(grouped[str(i)]) for i in (0,1,2)]==[8,6,6]
 fwd=[tuple((int(x)+1)%3-1 for x in v[:3]) for v in grouped['1']]
 # canonical residues 2 -> -1
 assert set(fwd)=={(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)}
 neighbors={x for x in fwd}
 assert len(neighbors)==6
 shells=[]
 for radius in range(0,11):
  points={(a,b,c) for a in range(-radius,radius+1) for b in range(-radius,radius+1) for c in range(-radius,radius+1) if abs(a)+abs(b)+abs(c)<=radius}
  predicted=(4*radius**3+6*radius**2+8*radius+3)//3
  assert len(points)==predicted
  residues={tuple(x%3 for x in p) for p in points}
  shells.append(dict(r=radius,size=len(points),mod3_spatial_image_size=len(residues)))
 # The 20-ray finite null set cannot simultaneously be interpreted as
 # (unrestricted) x->x+v in a single causal orientation in Ztime:
 # 8 vectors have delta time0 but move finite spatially.
 # Lift and filter explicitly breaks finite Lorentz symmetry.
 assert shells[-1]['size']>1000
 rec=dict(status='PASS',
  finite_tangent_field='F3^4 with split nondegenerate Q=x²+y²+z²−t² mod3',
  finite_null_nonzero=20,exact_null_by_residue_time={'0':8,'1':6,'2':6},
  null_timelike_forward_mod3_vectors=[list(z) for z in grouped['1']],
  six_selected_integer_spatial_directions=[list(z) for z in fwd],
  selected_forward_rule='Replace time F3 coordinate with external Z clock; lift spatial coordinates F3³ to Z³. Only retain the 6 Q-null classes with temporal residue +1, mapped to spatial ±e_1, ±e_2, ±e_3. Discard the 8 finite null vectors of time-residue0 and 6 time-residue−1; this breaks the full finite Lorentz group.',
  exact_future_l1_ball_size='|B_r|=(4r³+6r²+8r+3)/3, polynomial ~4r³/3, not saturating at 81 after two ticks.',
  future_ball_samples=shells,
  finite_spatial_projection='Modulo3 quotient maps infinite Z³ spatial growth back into 27 finite classes and eventually saturates; the 81 total original points also include the time residue.',
  conclusion='An expanding 3-dimensional spatial causal ball IS constructible by lifting/choosing an observer and six rays, but all of its infinite spatial size, time orientation and anisotropic cubic locality are imposed via Z³ and Z. This is NOT derived physical Minkowski spacetime; isotropic Lorentz invariance, Einstein dynamics and 3+1D gravitational continuum are not established.',
  prior='Builds on parallel Pass11831–11838 finite tangent Q and Round30 external Z clock saturation obstruction.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('OBSERVER LIGHTCONE finite 8/6/6, r=10',shells[-1]['size'],flush=True)
 return rec
if __name__=='__main__':run()
