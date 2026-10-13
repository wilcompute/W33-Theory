"""TOE65 front4: independent Galerkin ladders in native 3-loop quantum matter.

Imports the published TOE62 sector builder (whose original four runs are
executed once on import) then tests genuinely new (depth,flux) pairs.
No claim that finite cutoffs establish the full 80-site QFT.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261013_toe62_three_loop_matter import sector, Ne, Nv, fermions, contained
from w33_20261013_toe62_three_loop_matter import runs as old_runs

def certificate():
    fresh=[]
    for depth,L in ((1,2),(2,3),(3,2)):
        sectors={}
        for charged in (False,True):
            row=sector(depth,L,charged)
            sectors["charged" if charged else "neutral"]=row
            print("TOE65",depth,L,charged,row["dimension"],row["ground"],
                  row["Fock_boundary_weight"],row["electric_flux_boundary_weight"],flush=True)
        fresh.append({"depth":depth,"L":L,"sectors":sectors,
                      "charge_cost":sectors["charged"]["ground"]-sectors["neutral"]["ground"]})
    both={(a["depth"],a["L"]):a for a in old_runs+fresh}
    pairs=[((1,1),(1,2)),((1,2),(2,2)),((2,1),(2,2)),((2,2),(2,3)),
           ((2,2),(3,2)),((3,1),(3,2))]
    for x,y in pairs:
        for name in ("neutral","charged"):
            assert both[y]["sectors"][name]["ground"] <= both[x]["sectors"][name]["ground"]+1e-7, (x,y,name)
    for row in fresh:
        for name in ("neutral","charged"):
            s=row["sectors"][name]
            assert s["eigensolver_residual"]<1e-5
            assert 0<=s["Fock_boundary_weight"]<=1
            assert 0<=s["electric_flux_boundary_weight"]<=1
    # H_E=g²/2 sum n²>=0; H_B=(beta/g²)sum_i(1-(U_i+U_i†)/2)>=0;
    # V_mass >=-m*Nferm; each link hopping term has norm<=kappa.
    kappa=.7;mass=.3
    coarse_full_lower=-kappa*Ne-mass*fermions
    assert coarse_full_lower==-13.0
    return {"status":"PASS_TOE65_INTERACTING_THREE_LOOP_EXTRA_CUTOFF_SWEEPS",
            "new_runs":fresh,"baseline_runs_from_TOE62":old_runs,
            "Galerkin_variational_nesting_checks":len(pairs)*2,
            "native_patch":{"sites":Nv,"links":Ne,"fermions":fermions,"contained_Wilson_rows":len(contained)},
            "coarse_rigorous_full_patch_lower_bound":coarse_full_lower,
            "full_untruncated_patch_upper_bounds":{
              name: min(x["sectors"][name]["ground"] for x in fresh)
                 for name in ("neutral","charged")
            },
            "scope":"E(d,L) are variational upper bounds for the full fixed finite native 14-site/16-link patch, not the 80-site W33 system. The -13 lower bound is rigorous but very loose and DOES NOT certify convergence. Charge cost differences of two upper bounds are NOT rigorous bounds on a true charge gap. Independent cutoffs matter."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261013_toe65_three_loop_cutoff_grid.json").write_text(json.dumps(c,indent=2)+"\n")
