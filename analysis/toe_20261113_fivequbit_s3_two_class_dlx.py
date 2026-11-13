#!/usr/bin/env python3
"""Independent exact S3 orbit check + bounded two-orbit five-qubit size-8
DLX search. A timeout is strictly UNDECIDED, never proof of nonexistence.
Does not overwrite earlier run certificates.
"""
from pathlib import Path
import os,json,time,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
os.environ["DLX_REPS"]="692,694"
import w33_five_qubit_size8_dlx as X
import w33_five_qubit_size6 as B
import numpy as np
OUT=ROOT/"data/toe_20261113_fivequbit_s3_two_class_dlx.json"

def inverse_binary(M):
    n=len(M)
    A=np.concatenate([M%2,np.eye(n,dtype=int)],axis=1)
    for j in range(n):
        k=next(i for i in range(j,n) if A[i,j])
        A[[j,k]]=A[[k,j]]
        for i in range(n):
            if i!=j and A[i,j]:A[i]^=A[j]
    assert np.array_equal(M@A[:,n:]%2,np.eye(n,dtype=int))
    return A[:,n:]

def check_s3():
    pos,sing,ns,I,cand,reps=X.prep(5)
    assert reps==[692,693,694,695,700,701,702,703]
    O=B.orthogonal_group(5)
    assert len(O)==720
    orbit={}
    for i,r in enumerate(reps):
        images={B.congr(5,pos,g,r) for g in O}
        assert len(images)==720
        for s in images:
            assert s not in orbit
            orbit[s]=i
    assert len(orbit)==5760
    def as_mat(code):
        M=np.zeros((5,5),dtype=int)
        for k,(i,j) in enumerate(pos):
            if (int(code)>>k)&1:M[i,j]=M[j,i]=1
        return M
    maps=[]
    for s in reps:
        inv=B.code_of(5,pos,inverse_binary(as_mat(s)).tolist())
        shifted=int(s)^I
        assert inv in orbit and shifted in orbit
        maps.append([orbit[inv],orbit[shifted]])
    assert maps==[[1,1],[0,0],[3,5],[2,4],[6,3],[7,2],[4,7],[5,6]]
    classes=[[0,1],[2,3,4,5,6,7]]
    return {"O5_order":720,"eight_orbit_reps":reps,
            "S3_on_reps_inverse_and_plusI":maps,
            "two_classes":classes,
            "verified_orbit_elements":len(orbit)}

def main():
    start=time.time()
    symmetry=check_s3()
    control5=X.run(3,5,1,60)
    control7=X.run(3,7,1,60)
    assert control5["status"]=="exists" and control7["status"]=="none"
    r=X.run(5,8,2,150)
    if r["status"]=="none":
        # 'none' only certifiable if *both* 2-class reps return no timeout,
        # and proven S3 symmetry preserves maximality.
        assert len(r["per_rep"])==2 and all(not z["timeout"] for z in r["per_rep"])
    elif r["status"]=="exists":
        assert r["example"] is not None
    else:
        assert r["status"]=="undecided" and any(z["timeout"] for z in r["per_rep"])
    out={"schema":"toe.five_qubit.s3_two_class_dlx.v1",
         "s3_symmetry_exact":symmetry,
         "search":r,
         "controls":{"n3_size5":control5["status"],"n3_size7":control7["status"]},
         "status":r["status"],
         "elapsed_s":round(time.time()-start,2),
         "limit_per_orbit_s":150,
         "boundary":"If either orbit times out, no conclusion on 8-versus-9; S3 reduces representative count only."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("FINAL_S3_DLX",json.dumps({k:out[k] for k in ["status","elapsed_s","limit_per_orbit_s"]}),flush=True)
    return out
if __name__=="__main__":main()
