#!/usr/bin/env python3
"""Pass 396: lift Pluecker duality to the full incidence/Dirac complex."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_pass387():
    source = ROOT / "analysis" / "w33_pass387_pluecker_duality_certificate.py"
    if not source.exists():
        raise FileNotFoundError("Pass 387 Pluecker certificate module not found")
    spec = importlib.util.spec_from_file_location("w33_pass387", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Pass 387 module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P387 = load_pass387()


def gf2_rref(matrix: np.ndarray):
    A = np.array(matrix, dtype=np.uint8) & 1
    rows, cols = A.shape
    pivots = []
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if A[row, col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank,pivot]] = A[[pivot,rank]]
        for row in range(rows):
            if row != rank and A[row,col]:
                A[row] ^= A[rank]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return A,pivots


def gf2_rank(matrix):
    return len(gf2_rref(matrix)[1])


def gf2_nullspace(matrix):
    R,pivots = gf2_rref(matrix)
    free = [c for c in range(R.shape[1]) if c not in pivots]
    basis=[]
    for column in free:
        vector=np.zeros(R.shape[1],dtype=np.uint8)
        vector[column]=1
        for row,pivot in enumerate(pivots):
            vector[pivot]=R[row,column]
        basis.append(vector)
    return np.array(basis,dtype=np.uint8)


def column_basis(matrix):
    _,pivots=gf2_rref(np.array(matrix,dtype=np.uint8).T)
    return np.array(matrix,dtype=np.uint8)[:,pivots]&1 if pivots else np.zeros((matrix.shape[0],0),dtype=np.uint8)


def induced_homology_rank(ds,dt,chain_map):
    kernel_rows=gf2_nullspace(ds)
    mapped=(chain_map@kernel_rows.T)&1
    boundaries=column_basis(dt)
    return gf2_rank(np.hstack([boundaries,mapped]))-gf2_rank(boundaries)


def permutation_matrix(mapping):
    matrix=np.zeros((len(mapping),len(mapping)),dtype=np.uint8)
    for source,target in enumerate(mapping):
        matrix[target,source]=1
    return matrix


def incidence_matrix(points_count,lines):
    matrix=np.zeros((points_count,len(lines)),dtype=np.uint8)
    for j,line in enumerate(lines):
        matrix[list(line),j]=1
    return matrix


def stable_hash(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def build_certificate():
    w_points,_,w_lines=P387.build_w33()
    q_points,_,q_lines=P387.build_q43()
    q_point_index={p:i for i,p in enumerate(q_points)}
    q_line_index={line:i for i,line in enumerate(q_lines)}
    line_to_q_point=[q_point_index[P387.pluecker(w_points[line[0]],w_points[line[1]])] for line in w_lines]
    point_to_q_line=[]
    for point in range(40):
        incident=[i for i,line in enumerate(w_lines) if point in line]
        point_to_q_line.append(q_line_index[tuple(sorted(line_to_q_point[i] for i in incident))])

    M=incidence_matrix(40,w_lines)
    N=incidence_matrix(40,q_lines)
    R_line=permutation_matrix(line_to_q_point)
    R_point=permutation_matrix(point_to_q_line)
    dual=R_line@M.T@R_point.T
    zero=np.zeros((40,40),dtype=np.uint8)
    D_w=np.block([[zero,M],[M.T,zero]])
    D_q=np.block([[zero,N],[N.T,zero]])
    J=np.block([[zero,R_line],[R_point,zero]])

    M2=M&1
    A_w=(M2@M2.T)&1
    A_q=(M2.T@M2)&1
    D2=(D_w@D_w)&1
    D3=(D2@D_w)&1
    D4=(D2@D2)&1
    ranks={"M":gf2_rank(M2),"A_W":gf2_rank(A_w),"A_Q":gf2_rank(A_q),"D":gf2_rank(D_w),"D2":gf2_rank(D2),"D3":gf2_rank(D3),"D4":gf2_rank(D4)}
    homology={"H_W":40-2*ranks["A_W"],"H_Q":40-2*ranks["A_Q"]}
    induced={"M_transpose_H_W_to_H_Q":induced_homology_rank(A_w,A_q,M2.T),"M_H_Q_to_H_W":induced_homology_rank(A_q,A_w,M2)}
    sequence=[80,ranks["D"],ranks["D2"],ranks["D3"],ranks["D4"]]
    at_least=[sequence[i]-sequence[i+1] for i in range(4)]
    jordan={"J4":at_least[3],"J3":at_least[2]-at_least[3],"J2":at_least[1]-at_least[2],"J1":at_least[0]-at_least[1]}
    checks={
        "coordinate_maps_bijective":sorted(line_to_q_point)==list(range(40)) and sorted(point_to_q_line)==list(range(40)),
        "incidence_intertwiner_exact":np.array_equal(dual,N),
        "J_is_permutation":np.array_equal(J@J.T,np.eye(80,dtype=np.uint8)),
        "Dirac_intertwiner_exact":np.array_equal(J@D_w@J.T,D_q),
        "A_W_A_Q_square_zero":not np.any((A_w@A_w)&1) and not np.any((A_q@A_q)&1),
        "chain_maps_commute":np.array_equal((M2.T@A_w)&1,(A_q@M2.T)&1) and np.array_equal((M2@A_q)&1,(A_w@M2)&1),
        "ranks_25_16_10":(ranks["M"],ranks["A_W"],ranks["A_Q"])==(25,16,10),
        "homology_8_plus_20":homology=={"H_W":8,"H_Q":20},
        "incidence_zero_on_homology":induced=={"M_transpose_H_W_to_H_Q":0,"M_H_Q_to_H_W":0},
        "Dirac_ranks_50_26_2_0":[ranks["D"],ranks["D2"],ranks["D3"],ranks["D4"]]==[50,26,2,0],
        "Jordan_J4x2_J3x22_J1x6":jordan=={"J4":2,"J3":22,"J2":0,"J1":6},
    }
    payload={"pass":396,"status":"PASS" if all(checks.values()) else "FAIL","coordinate_duality":{"matrix_identity":"N_Q=R_line M_W^T R_point^T","dirac_identity":"D_Q=J D_W J^T","W_line_to_Q_point":line_to_q_point,"W_point_to_Q_line":point_to_q_line},"characteristic_two":{"ranks":ranks,"homology_dimensions":homology,"induced_incidence_map_ranks":induced,"Jordan_type":jordan},"checks":checks}
    payload["certificate_sha256"]=stable_hash(payload)
    return payload


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("data/w33_pass396_pluecker_chain_dirac_lift.json"))
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    payload=build_certificate()
    text=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    if args.check:
        if not args.output.exists() or args.output.read_text()!=text:
            raise SystemExit("Pass 396 certificate drift")
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status":payload["status"],"homology":payload["characteristic_two"]["homology_dimensions"],"Jordan":payload["characteristic_two"]["Jordan_type"],"certificate_sha256":payload["certificate_sha256"]}))


if __name__=="__main__":
    main()
