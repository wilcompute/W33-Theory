#!/usr/bin/env python3
"""Sub-100 mW piezoelectric/electro-optic compiler and deterministic layout package."""
from __future__ import annotations
from functools import lru_cache
import json, math, struct
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from w33_levi_next5_v5_common import ACTIVE, gds_library, sha256_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_2026_07_11_LEVI_NEXT5_V5_hybrid.json'
TAU=2*math.pi


def psd_sqrt(H):
    vals,vecs=eigh((H+H.T.conj())/2);vals=np.clip(vals,0,None)
    return (vecs*np.sqrt(vals))@vecs.T.conj()
def halmos(A):
    s=np.linalg.svd(A,compute_uv=False)[0];C=A/s;I=np.eye(8)
    U=np.block([[C,psd_sqrt(I-C@C.T)],[psd_sqrt(I-C.T@C),-C.T]]).astype(complex)
    return s,C,U
def givens_decompose(U):
    A=U.copy();rots=[];n=A.shape[0]
    for col in range(n):
      for row in range(n-1,col,-1):
        i,j=row-1,row;a,b=A[i,col],A[j,col];r=math.sqrt(abs(a)**2+abs(b)**2)
        c,s=(1+0j,0+0j) if r<1e-15 else (np.conj(a)/r,np.conj(b)/r)
        G=np.array([[c,s],[-np.conj(s),np.conj(c)]],complex);A[[i,j],:]=G@A[[i,j],:]
        rots.append((i,j,math.atan2(abs(s),abs(c)),float(np.angle(s)-np.angle(c)),float(np.angle(c))))
    return rots,np.angle(np.diag(A))
def build_rotation(theta,phi,alpha):
    c=math.cos(theta)*np.exp(1j*alpha);s=math.sin(theta)*np.exp(1j*(alpha+phi))
    return np.array([[c,s],[-np.conj(s),np.conj(c)]],complex)
def synthesize(pairs,theta,phi,alpha,out):
    A=np.diag(np.exp(1j*out))
    for k in reversed(range(len(pairs))):
        i,j=pairs[k];G=build_rotation(theta[k],phi[k],alpha[k]);A[[i,j],:]=G.conj().T@A[[i,j],:]
    return A
def fidelity(U,V):
    n=U.shape[0];return float(abs(np.trace(U.conj().T@V))**2/(n*n))
def encode_phase_words(x,bits,signed=True):
    if bits<2 or bits>31:raise ValueError('unsupported phase word width')
    values=np.asarray(x,dtype=float)
    if not np.all(np.isfinite(values)):raise ValueError('non-finite phase command')
    if signed:
        top=(1<<(bits-1))-1
        if np.any(values < -TAU) or np.any(values > TAU):raise ValueError('phase command outside signed full scale')
        words=np.rint(values*top/TAU).astype(np.int64)
        if np.any(words < -top) or np.any(words > top):raise ValueError('phase word outside signed range')
    else:
        top=(1<<bits)-1
        if np.any(values<0) or np.any(values>TAU):raise ValueError('phase command outside unsigned full scale')
        words=np.rint(values*top/TAU).astype(np.int64)
        if np.any(words<0) or np.any(words>top):raise ValueError('phase word outside unsigned range')
    return words
def decode_phase_words(words,bits,signed=True):
    top=(1<<(bits-1))-1 if signed else (1<<bits)-1;raw=np.asarray(words)
    if np.any(raw!=np.floor(raw)):raise ValueError('phase words must be integers')
    raw=raw.astype(np.int64)
    floor=-top if signed else 0
    if np.any(raw<floor) or np.any(raw>top):raise ValueError('phase word outside declared range')
    return raw.astype(float)*TAU/top
def quantize(x,bits):return decode_phase_words(encode_phase_words(x,bits,signed=True),bits,signed=True)
def phase_error(target,measured):return (target-measured+math.pi)%TAU-math.pi
def crosstalk(n,nearest=0.010,length=1.25):
    idx=np.arange(n);d=np.abs(idx[:,None]-idx[None,:]);K=np.exp(-d/length);np.fill_diagonal(K,0)
    K*=nearest/math.exp(-1/length);return np.eye(n)+K

def calibrate(target,C,Cinv,bias,bits,rng,iters=9):
    cmd=quantize(target,bits);hist=[]
    for _ in range(iters):
        measured=C@cmd+bias+rng.normal(0,4e-5,len(target));err=phase_error(target,measured)
        cmd=quantize(cmd+0.97*(Cinv@err),bits);hist.append(float(np.linalg.norm(err)/math.sqrt(len(err))))
    return cmd,C@cmd+bias,hist

def layout_manifest():
    rects=[];slots=[];pitch_y=22.0;stage_pitch=360.0;x0=200.0
    # Abstract placement rails, not routed foundry waveguides.
    for m in range(16): rects.append({'layer':1,'x0':50,'y0':m*pitch_y,'x1':6100,'y1':m*pitch_y+0.8})
    idx=0
    for stage in range(16):
        start=0 if stage%2==0 else 1
        for m in range(start,15,2):
            if idx>=120:break
            x=x0+stage*stage_pitch;y=(m+0.5)*pitch_y
            # PZT trim layer 20; EO electrode layer 30; monitor layer 40.
            rects += [
                {'layer':20,'x0':x,'y0':y-5,'x1':x+210,'y1':y+5},
                {'layer':30,'x0':x+25,'y0':y-8,'x1':x+190,'y1':y-6},
                {'layer':30,'x0':x+25,'y0':y+6,'x1':x+190,'y1':y+8},
            ]
            slots.append({'index':idx,'stage':stage,'modes':[m,m+1],'x_um':x,'y_um':y,'pzt_placement_length_um':210,'eo_placement_length_um':165})
            idx+=1
    assert idx==120
    for m in range(16):
        x=6000;y=m*pitch_y;rects.append({'layer':40,'x0':x,'y0':y-3,'x1':x+45,'y1':y+4})
    return {'units':'um','scope':'abstract deterministic placement sketch; no couplers, routed MZIs, ports, PDK layers, or DRC closure',
        'layers':{'SiN_reference_rail':1,'PZT_placement':20,'EO_placement':30,'monitor_placement':40},
        'interferometer_slots':slots,'rectangles':rects}

def validate_gds_records(data,expected_boundaries):
    i=0;boundaries=0;records=0
    while i<len(data):
        if i+4>len(data):raise ValueError('truncated GDS record header')
        n,rtype,_dtype=struct.unpack('>HBB',data[i:i+4])
        if n<4 or n%2 or i+n>len(data):raise ValueError('invalid GDS record length')
        boundaries+=rtype==0x08;records+=1;i+=n
    return {'full_parse':i==len(data),'records':records,'boundaries':boundaries,
        'expected_boundaries':expected_boundaries,'envelope_ok':i==len(data) and boundaries==expected_boundaries and data[:4]==bytes.fromhex('00060002') and data[-4:]==bytes.fromhex('00040400')}

def veriloga_contract():
    p=ROOT/'hardware/holonet_v5_hybrid_phase.va';text=p.read_text()
    need=['module holonet_v5_hybrid_phase','parameter real VPI = 2.5','parameter real C_EO = 55f','PZT_TAU','laplace_nd']
    return {'path':str(p.relative_to(ROOT)),'required_tokens':all(x in text for x in need),
        'scope':'static source contract only; no Verilog-A simulator or PDK compact-model validation'}

@lru_cache(maxsize=1)
def analyze(seed=20260711):
    rng=np.random.default_rng(seed);_s,_C,U=halmos(ACTIVE);rots,out=givens_decompose(U)
    pairs=[(i,j) for i,j,*_ in rots];theta=np.array([x[2] for x in rots]);phi=np.array([x[3] for x in rots]);alpha=np.array([x[4] for x in rots])
    target=np.concatenate([theta,phi,alpha,out]);n=len(target);Cx=crosstalk(n);Cinv=np.linalg.inv(Cx+1e-10*np.eye(n))
    bias=rng.normal(0,0.006,n);cmd,eff,hist=calibrate(target,Cx,Cinv,bias,16,rng)
    m=len(theta)
    def unitary(vec,wavelength=1550.0,dyn=None):
        t=vec[:m].copy();p=vec[m:2*m].copy();a=vec[2*m:3*m].copy();o=vec[3*m:].copy();ratio=1550.0/wavelength
        t*=1+0.018*(ratio-1);p*=ratio;a*=ratio;o*=ratio
        if dyn is not None:t+=dyn[:m];p+=dyn[m:2*m];a+=dyn[2*m:3*m];o+=dyn[3*m:]
        return synthesize(pairs,t,p,a,o)
    nominal=fidelity(U,unitary(eff));waves=np.linspace(1530,1565,15);waveF=[fidelity(U,unitary(eff,float(w))) for w in waves]
    dies=[]
    for _ in range(128):
        die_bias=bias+rng.normal(0,0.0025,n);_c,e,_h=calibrate(target,Cx,Cinv,die_bias,16,rng,iters=6)
        dies.append(fidelity(U,unitary(e,1550,rng.normal(0,0.00045,n))))
    drift=np.zeros(n);tracked=[];openloop=[];tracked_cmd=cmd.copy()
    for _ in range(256):
        drift += rng.normal(0,0.00018,n)+rng.normal(0,0.0005)*np.exp(-np.arange(n)/180)
        openloop.append(fidelity(U,unitary(Cx@cmd+bias+drift)))
        meas=Cx@tracked_cmd+bias+drift+rng.normal(0,5e-5,n);err=phase_error(target,meas)
        tracked_cmd=quantize(tracked_cmd+0.96*(Cinv@err),16)
        tracked.append(fidelity(U,unitary(Cx@tracked_cmd+bias+drift)))
    arr=np.array(dies)

    # Explicit electrical assumptions; actuator dynamic term is derived from CV^2f.
    N=n;cap_f=55e-15;vrms=2.5;update_hz=20_000
    eo_dynamic_mw=N*cap_f*vrms**2*update_hz*1e3
    power={
        'pzt_static_leakage_mw':N*12e-9*1e3,
        'pzt_refresh_average_mw':4.0,
        'eo_capacitive_switching_mw':eo_dynamic_mw,
        'driver_quiescent_mw':25.6,
        'monitor_tia_mw':20.0,
        'digital_servo_mw':28.0,
        'clock_reference_mw':8.0,
    }
    power['total_mw']=sum(power.values())
    manifest=layout_manifest();gds=gds_library(manifest['rectangles'])
    gds_validation=validate_gds_records(gds,len(manifest['rectangles']));va=veriloga_contract()
    words=encode_phase_words(cmd,16,signed=True)
    rejects_invalid=True
    for bad,signed in [([32768],True),([-32768],True),([-1],False),([65536],False)]:
        try:decode_phase_words(bad,16,signed=signed);rejects_invalid=False
        except ValueError:pass
    checks={
        'mesh_unitary':np.linalg.norm(U.conj().T@U-np.eye(16))<1e-7,
        'calibration_converges':hist[-1]<hist[0]/100,
        'nominal_above_0_9999':nominal>0.9999,
        'wavelength_p05_above_0_997':float(np.quantile(waveF,0.05))>0.997,
        'synthetic_phase_p05_above_0_999':float(np.quantile(arr,0.05))>0.999,
        'tracked_min_above_0_999':min(tracked)>0.999,
        'tracking_beats_open_loop':np.mean(tracked)>np.mean(openloop),
        'power_below_100mW':power['total_mw']<100,
        'signed16_phase_words_valid':len(words)==n and int(words.min())>=-32767 and int(words.max())<=32767 and rejects_invalid,
        'reference_manifest_has_120_slots':len(manifest['interferometer_slots'])==120,
        'gds_record_envelope_valid':gds_validation['envelope_ok'],
        'veriloga_static_contract_present':va['required_tokens'],
    }
    return {
        'status':'PASS' if all(checks.values()) else 'FAIL','checks':{k:bool(v) for k,v in checks.items()},
        'compiler':{'modes':16,'mathematical_givens_rotations':120,'controls':n,'phase_bits':16,
            'phase_word_encoding':'signed symmetric 16-bit, full scale +/-2pi, -32768 reserved','command_word_min':int(words.min()),'command_word_max':int(words.max()),
            'nominal_fidelity':nominal,'calibration_rms':hist,'command_digest':sha256_json(words.tolist())},
        'synthetic_phase_corners':{'draws':128,'model':'fixed-seed Gaussian phase bias/noise with full inverse-crosstalk recalibration; no PDK, loss, yield, or measured device distribution','mean':float(arr.mean()),'p05':float(np.quantile(arr,0.05)),'min':float(arr.min())},
        'wavelength':{'band_nm':[1530,1565],'p05':float(np.quantile(waveF,0.05)),'min':float(min(waveF))},
        'drift':{'epochs':256,'tracked_mean':float(np.mean(tracked)),'tracked_min':float(min(tracked)),'open_loop_mean':float(np.mean(openloop))},
        'power_budget':power,
        'layout':{'kind':'record-valid abstract placement sketch','manifest_digest':sha256_json(manifest),'gds_sha256':__import__('hashlib').sha256(gds).hexdigest(),'gds_bytes':len(gds),'layers':manifest['layers'],'validation':gds_validation,'generator':'analysis/w33_levi_next5_v5_gds.py','scope':manifest['scope']},
        'veriloga':va,
        'design_assumptions':{
            'platform':'Si3N4 passive mesh with PZT piezo-optomechanical coarse trim and capacitive Pockels fine control',
            'pzt_leakage_per_control_w':12e-9,'eo_capacitance_f':cap_f,'eo_vrms_v':vrms,'servo_update_hz':update_hz,
            'boundary':'Electrical driver, TIA, servo and clock powers are allocations, not measurements. Monte Carlo values are synthetic phase-model samples. The GDS is a placement sketch, not a functional photonic layout; the Verilog-A file has only a static source-contract check.'
        },
        'theorem':(
            'Under explicit architectural allocations, replacing the v4 thermo-optic model by PZT/EO controls gives an '
            '85.607097 mW modeled budget and >0.999 fidelity in fixed-seed phase-error simulations. Commands are validated '
            'signed 16-bit phase words with explicit full scale. The supplied GDSII is a record-valid deterministic placement sketch and the '
            'Verilog-A file is a separate static compact-model interface; neither is PDK, DRC, or measurement evidence.'
        )
    }

def emit_gds(path:Path):
    path.write_bytes(gds_library(layout_manifest()['rectangles']))

def main():
    out=analyze();text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    OUT.write_text(text,encoding='utf-8');print(text,end='')
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
