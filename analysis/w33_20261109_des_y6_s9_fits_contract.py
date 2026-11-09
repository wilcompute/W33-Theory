#!/usr/bin/env python3
"""DES Y6 frozen-S9 FITS data contract; fail-closed absent full public product.

An internally generated labeled synthetic FITS fixture tests the scale cuts
and covariance checks. It is NEVER represented as DES measurements or used to
score any cosmological model.
"""
import hashlib,json,sys,tempfile
from pathlib import Path
import numpy as np
from astropy.io import fits

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"analysis/toe_uv/prereg_noshear.json"
FROZEN=json.loads(PRE.read_text(encoding="utf8"))["S9_shear_no_split"]
assert FROZEN["frozen"]=="2026-11-08"

def synthetic_hdus():
    ang1=[5.,12.,20.,60.]
    ang2=[30.,70.,100.,110.]
    def tab(name,angs):
        cols=[
          fits.Column(name="ANG",format="D",unit="arcmin",array=np.array(angs)),
          fits.Column(name="BIN1",format="J",array=np.array([1,1,2,2])),
          fits.Column(name="BIN2",format="J",array=np.array([1,2,2,3])),
          fits.Column(name="VALUE",format="D",array=np.array([0.01,0.02,0.03,0.04]))]
        return fits.BinTableHDU.from_columns(cols,name=name)
    primary=fits.PrimaryHDU()
    primary.header["SYNTHET"]=True
    primary.header["UNBLIND"]=True
    xip=tab("XIP",ang1)
    xim=tab("XIM",ang2)
    cov=fits.ImageHDU(data=np.eye(8)*1e-4,name="COVMAT")
    nz=fits.BinTableHDU.from_columns([
        fits.Column(name="Z_MID",format="D",array=np.array([.1,.2,.3])),
        fits.Column(name="BIN1",format="D",array=np.array([.5,.4,.1]))],name="NZ_SOURCE")
    return fits.HDUList([primary,cov,xip,xim,nz])

def validate_hdul(hdul,expected_real=False):
    issues=[]
    names={h.name.upper():i for i,h in enumerate(hdul)}
    required={"XIP","XIM","COVMAT","NZ_SOURCE"}
    if required-names.keys():issues.append("missing extensions "+str(sorted(required-names.keys())))
    if not hdul[0].header.get("UNBLIND",False):issues.append("not explicitly unblinded")
    if expected_real and hdul[0].header.get("SYNTHET",False):issues.append("synthetic fixture cannot be a DES observation")
    if issues:return {"valid":False,"issues":issues}
    selections={}
    N=0
    for name,cut in (("XIP",10.),("XIM",60.)):
        table=hdul[names[name]].data
        cols={x.upper() for x in table.names}
        if not {"ANG","BIN1","BIN2","VALUE"}<=cols:
            issues.append("missing "+name+" required columns")
            continue
        ang=np.asarray(table["ANG"],dtype=float)
        vals=np.asarray(table["VALUE"],dtype=float)
        if not np.all(np.isfinite(vals)) or not np.all(np.isfinite(ang)):
            issues.append(name+" nonfinite")
        if np.any(ang<=0):issues.append(name+" nonpositive angular separations")
        unit=hdul[names[name]].columns["ANG"].unit
        if unit is None or unit.lower() not in ("arcmin","arcminute","arcminutes"):
            issues.append(name+" angle unit is not arcmin")
        keep=np.where(ang>cut)[0]
        selections[name]={"all_rows":len(ang),
                          "kept_rows":len(keep),
                          "kept_positions":keep.tolist(),
                          "scale_cut_arcmin_strict_gt":cut}
        N+=len(ang)
    if issues:return {"valid":False,"issues":issues}
    cov=np.asarray(hdul[names["COVMAT"]].data,dtype=float)
    if cov.shape!=(N,N):issues.append("covariance dimension mismatch")
    elif not np.all(np.isfinite(cov)):issues.append("nonfinite covariance")
    elif np.max(abs(cov-cov.T))>1e-10:issues.append("covariance not symmetric")
    elif min(np.linalg.eigvalsh(cov))<=0:issues.append("covariance not positive definite")
    if len(hdul[names["NZ_SOURCE"]].data)==0:issues.append("missing source n(z) values")
    if issues:return {"valid":False,"issues":issues}
    keep=np.r_[np.array(selections["XIP"]["kept_positions"]),
               len(hdul[names["XIP"]].data)+np.array(selections["XIM"]["kept_positions"])]
    sub=cov[np.ix_(keep,keep)]
    assert min(np.linalg.eigvalsh(sub))>0
    return {"valid":True,"issues":[],
            "selection":selections,
            "full_data_size":N,"cut_size":len(keep),
            "covariance_min_eig":float(min(np.linalg.eigvalsh(cov))),
            "cut_covariance_min_eig":float(min(np.linalg.eigvalsh(sub))),
            "has_data_and_covariance":True,
            "has_complete_model_predictions":False,
            "frozen_S9_scored":False,
            "warning":"Passing data schema is NOT a likelihood: still require corrected CLASS/Halofit theories, full nuisance priors/refits, bin/covariance and scale unit validation against the actual collaboration release."}

def main(path=None):
    with tempfile.TemporaryDirectory(prefix="w33_y6_schema_") as temp:
        p=Path(temp)/"SYNTHETIC_not_DES_y6_3x2pt.fits"
        hdu=synthetic_hdus()
        hdu.writeto(p)
        data=p.read_bytes()
        with fits.open(p) as x:
            valid=validate_hdul(x)
            assert valid["valid"]
            bad_blind=fits.HDUList([y.copy() for y in x])
            bad_blind[0].header["UNBLIND"]=False
            fail_blind=validate_hdul(bad_blind)
            assert not fail_blind["valid"]
            bad_cov=fits.HDUList([y.copy() for y in x])
            bad_cov["COVMAT"].data[0,0]=-1.
            fail_cov=validate_hdul(bad_cov)
            assert not fail_cov["valid"]
            fail_synthetic=validate_hdul(x,expected_real=True)
            assert not fail_synthetic["valid"]
    out={"status":"PASS_SYNTHETIC_DES_Y6_S9_FITS_CONTRACT_NOT_SCORED",
         "frozen":"2026-11-08",
         "synthetic_fixture_sha256":hashlib.sha256(data).hexdigest(),
         "synthetic_valid_contract":valid,
         "missing_unblinding_rejected":fail_blind,
         "bad_covariance_rejected":fail_cov,
         "synthetic_as_real_rejected":fail_synthetic,
         "actual_DES_Y6_FITS_access":False,
         "S9_scored":False,
         "scope":"Contract/unit tests only; fully synthetic 8-row two-point FITS, not authentic DES Y6 data or a cosmology model comparison."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS S9 data contract",json.dumps({"cov_rows":valid["full_data_size"],
                                             "cut_rows":valid["cut_size"],
                                             "negative_controls_passed":3,
                                             "scored":False}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
