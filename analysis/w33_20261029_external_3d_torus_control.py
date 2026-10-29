#!/usr/bin/env python3
"""External 3D cubic-lattice control on W33's 40-state internal Laplacian.

A spectral dimension near three is engineered by external lattice edges,
not derived from the diameter-two W33 geometry.
"""
import math,json

def bands():
    return ((0,1),(10,24),(16,15)) # W33 L=12I-A, known SRG spectrum

def row(m,t):
    assert m>=3 and t>0
    inside=sum(g*math.exp(-t*l) for l,g in bands())
    mean_inside=sum(g*l*math.exp(-t*l) for l,g in bands())/inside
    ext=[2*(1-math.cos(2*math.pi*j/m)) for j in range(m)]
    z=sum(math.exp(-t*x) for x in ext)
    mean_ext=sum(x*math.exp(-t*x) for x in ext)/z
    heat=(inside/40)*(z/m)**3
    ds=2*t*(mean_inside+3*mean_ext)
    return dict(t=t,linear_period=m,vertices=40*m**3,
                mean_return_probability=heat,spectral_dimension=ds)

def main():
    rows=[row(m,t) for m in (12,20,32,48,80) for t in (1,2,3,5,8)]
    control=[r for r in rows if r["linear_period"]==80]
    assert 3.0<control[-1]["spectral_dimension"]<3.1
    assert control[0]["spectral_dimension"]>3.6
    out=dict(status="PASS",model="L_W33 tensor I + I tensor L_cubic_3torus",
      W33_internal_L_spectrum={"0":1,"10":24,"16":15},rows=rows,
      result="External bounded-degree cubic lattice creates a 3D heat-kernel scaling window; W33 supplies one internal zero mode and 39 gapped internal modes.",
      limitation="Does NOT derive an emergent 3+1 Lorentzian spacetime, gauge interaction, Einstein equations or any continuum from W33 alone.")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__":main()
