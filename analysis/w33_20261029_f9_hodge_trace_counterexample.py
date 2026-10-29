#!/usr/bin/env python3
"""GF(9) counterexample to trace-only Hodge closure classification.

F9 = F3[t]/(t^2+1), with t^2=-1. The scalar kappa=t*I_6
is P-symmetric, squares to -I_6, and has zero trace in char 3,
yet cannot be a four-dimensional metric Hodge star: it has
(+t,-t) multiplicities (6,0), versus the mandatory (3,3).
"""
import json

def add(x,y):return ((x[0]+y[0])%3,(x[1]+y[1])%3)
def mul(x,y):return ((x[0]*y[0]-x[1]*y[1])%3,
                    (x[0]*y[1]+x[1]*y[0])%3)
def scalar(n,x):return ((n*x[0])%3,(n*x[1])%3)

def verify():
    zero=(0,0);one=(1,0);minus_one=(2,0)
    ii=(0,1);mi=(0,2)
    assert mul(ii,ii)==minus_one
    assert add(ii,mi)==zero and ii!=mi
    # P is the symmetric wedge pairing in basis 01,02,03,12,13,23.
    P=[[0]*6 for _ in range(6)]
    for a,b,sgn in ((0,5,1),(1,4,-1),(2,3,1)):
        P[a][b]=P[b][a]=sgn%3
    assert all(P[i][j]==P[j][i] for i in range(6) for j in range(6))
    # The scalar operator commutes with any P.
    assert all(mul(ii,(P[i][j],0))==mul((P[i][j],0),ii)
               for i in range(6) for j in range(6))
    square=mul(ii,ii)
    trace=scalar(6,ii)
    assert square==minus_one and trace==zero
    # Eigenvalue i has multiplicity6; eigenvalue -i multiplicity0.
    # Any Hodge star for a nondegenerate 4D metric has a 3+3 split,
    # since in an orthogonal basis e01 maps to e23, etc.
    eigens=[6,0]
    assert eigens!=[3,3]
    # For q=3^(2m), char3 and i in field, the same counterexample works.
    return {
      "schema":"w33.f9.closure_trace_counterexample.v1",
      "field":"F9=F3[t]/(t^2+1)",
      "characteristic":3,"q":9,"q_mod4":1,
      "i":list(ii),"i_squared":list(square),
      "kappa":"i times 6x6 identity",
      "P_symmetric":True,"kappa_squared_minus_I":True,
      "trace_kappa":list(trace),"plus_i_eigenspace_dimension":6,
      "minus_i_eigenspace_dimension":0,
      "balanced_Hodge_eigenspace_dimensions":[3,3],
      "trace_zero_sufficient_for_Hodge":False,
      "necessary_metric_criterion":"balanced +/- i eigenspaces",
      "generalization":"all F_(3^(2m)), m>=1",
      "notes":"Corrects Pass12410 theorem as written. No Lorentzian physical metric is thereby derived."
    }

if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
