#!/usr/bin/env python3
"""Causal-set alternatives: 2D--5D sprinklings, Lorentz covariance, and
matched-density transitive-percolation null. Spacetime dimension is INPUT
through the sprinkling distribution: not inferred dynamically from raw order.
"""
from pathlib import Path
from math import gamma
import json,numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_causal_set_dimension_nulls.json"
N=192
def expected(d):
    return gamma(d+1)*gamma(d/2)/(2*gamma(1.5*d))
def sprinkled(d,n,seed):
    rng=np.random.default_rng(seed)
    timemag=rng.beta(1,d,size=n)
    t=timemag*np.where(rng.random(n)>.5,1.,-1.)
    u=rng.normal(size=(n,d-1))
    u/=np.linalg.norm(u,axis=1)[:,None]
    spatial=u*((1-timemag)*rng.random(n)**(1/(d-1)))[:,None]
    return np.column_stack((t,spatial))
def order(coords):
    delta=coords[:,None,0]-coords[None,:,0]
    squared=np.sum((coords[:,None,1:]-coords[None,:,1:])**2,axis=2)
    return (delta>0)&(delta*delta>=squared)
def longest(C):
    counts=C.sum(axis=1)
    # C[i,j]: j is causal past of i. topologically sort by each row's past count
    idx=np.argsort(counts)
    level=np.ones(len(C),dtype=int)
    for i in idx:
        prior=np.flatnonzero(C[i])
        if len(prior):level[i]=1+max(level[prior])
    return int(level.max())
def rstat(C):
    return float(np.count_nonzero(C)/(C.shape[0]*(C.shape[0]-1)/2))
def interval_census(C):
    # C[i,j] true when j is strictly in the causal past of i.
    paths=C.astype(np.int32)@C.astype(np.int32)
    interval=paths[C]
    return {str(k):int(np.sum(interval==k)) for k in range(4)}
def percolate_null(n,p,random_upper):
    C=np.zeros((n,n),dtype=bool)
    for i in range(n-1,-1,-1):
        links=np.flatnonzero(random_upper[i,i+1:]<p)+i+1
        for j in links:
            C[i,j]=True
            C[i]|=C[j]
    return C
def tuned_null(n,target,seed):
    rng=np.random.default_rng(seed)
    random_upper=rng.random((n,n))
    lo,hi=0.,1.
    for _ in range(20):
        m=(lo+hi)/2
        C=percolate_null(n,m,random_upper)
        if rstat(C)<target:lo=m
        else:hi=m
    C=percolate_null(n,(lo+hi)/2,random_upper)
    return C,(lo+hi)/2
def run():
    classes=[]
    for d in (2,3,4,5):
        rows=[]
        for rep in range(12):
            coords=sprinkled(d,N,20261103+d*1000+rep)
            C=order(coords)
            assert not np.any(np.diag(C))
            assert not np.any(C&C.T)
            # direct causal order is transitive: relation square must be subset.
            paths=C.astype(np.int32)@C.astype(np.int32)
            assert not np.any((paths>0)&(~C))
            rows.append({"seed":rep,"comparable_pair_fraction":rstat(C),
                         "longest_chain":longest(C)})
        mean=float(np.mean([x["comparable_pair_fraction"] for x in rows]))
        theory=expected(d)
        assert abs(mean-theory)<.02,(d,mean,theory)
        classes.append({"dimension_supplied":d,"theoretical_ordering_fraction":theory,
          "observed_mean":mean,
          "observed_sd":float(np.std([x["comparable_pair_fraction"] for x in rows],ddof=1)),
          "mean_longest_chain":float(np.mean([x["longest_chain"] for x in rows])),
          "replicates":rows})
    # Exact covariance of poset under a nontrivial Lorentz frame boost. Not
    # a proof that sprinkling is generated without a background Minkowski metric.
    coords=sprinkled(4,N,731)
    C=order(coords)
    beta=.55;G=(1-beta*beta)**(-.5)
    boosted=coords.copy()
    boosted[:,0]=G*(coords[:,0]-beta*coords[:,1])
    boosted[:,1]=G*(coords[:,1]-beta*coords[:,0])
    assert np.array_equal(C,order(boosted))
    rng=np.random.default_rng(117)
    perm=rng.permutation(N)
    assert np.array_equal(C[np.ix_(perm,perm)],order(coords[perm]))
    # Density-matched random DAG: geometry can be matched by ONE ordering
    # fraction without recovering its interval distribution.
    r=rstat(C)
    null,p=tuned_null(N,r,7843)
    nr=rstat(null)
    assert abs(nr-r)<.025
    ic=interval_census(C)
    ni=interval_census(null)
    geom_vs_null_chain={"geometry":longest(C),"null":longest(null)}
    # 4D Benincasa-Dowker-Glaser *combinatorial bracket*, in a
    # bounded diamond with substantial boundary contributions. NOT a
    # continuum scalar-curvature estimate or a physical action value.
    bdg_bracket=lambda counts: N-int(counts['0'])+9*int(counts['1'])-16*int(counts['2'])+8*int(counts['3'])
    bdg_geom=bdg_bracket(ic)
    bdg_null=bdg_bracket(ni)
    # Compare internal interval densities normalized to comparable pairs.
    norm=lambda c,v:v/max(1,np.count_nonzero(c))
    interval_gap=sum(abs(norm(C,ic[str(j)])-norm(null,ni[str(j)])) for j in range(4))
    assert interval_gap>.05,(interval_gap,ic,ni)
    out={
     "status":"PASS_2D_TO_5D_LORENTZ_POSETS_AND_MATCHED_RANDOM_DAG_NULL",
     "construction":"N uniform independent points in a finite Minkowski Alexandrov diamond in dimension d=2..5. Coordinates use dimension-dependent Beta time distribution and uniform spatial balls. Future relation from timelike/null Minkowski separation, then discard coordinates.",
     "ordering_fraction_formula":"Gamma(d+1)Gamma(d/2)/(2Gamma(3d/2))",
     "series":classes,
     "lorentz_boost_dimension":4,"boost_beta":beta,
     "boost_order_relation_exactly_invariant":True,
     "relabeling_invariant":True,
     "d4_geometry_comparable_fraction":r,
     "density_matched_random_transitive_percolation":{"link_probability":p,
       "null_comparable_fraction":nr,"geometry_interval_count_0to3":ic,
       "null_interval_count_0to3":ni,
       "sum_L1_difference_first_four_interval_frequency":interval_gap,
       "chains":geom_vs_null_chain,
       "bdg_4d_combinatorial_bracket_on_bounded_diamond":bdg_geom,
       "bdg_4d_combinatorial_bracket_on_density_matched_null":bdg_null,
       "bdg_action_boundary":"Only n-N0+9N1-16N2+8N3 bracket, ignoring overall scale 4sqrt6(l/lp)^2 and boundary terms; correct 4D curvature interpretation requires continuum-volume limit and fluctuation control."},
     "causal_dimensionality_boundary":"Successful ordering statistics validate known causal-set embedding diagnostics under an externally supplied d-dimensional Minkowski diamond. Causal order and fixed event density alone are insufficient to derive d=4, metric dynamics, Einstein equations, or Planck scale. A full dimension claim needs varied manifold geometries, scaling in N and likelihood against matched-degree/geometric nulls.",
     "literature":["https://doi.org/10.1103/qdst-yrh6","https://arxiv.org/abs/1903.11544"]
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("CAUSAL DIMENSION",[(x["dimension_supplied"],round(x["observed_mean"],4),round(x["theoretical_ordering_fraction"],4)) for x in classes])
    print("NULL",round(r,4),round(nr,4),round(interval_gap,3),geom_vs_null_chain)
    return out
if __name__=="__main__":run()
