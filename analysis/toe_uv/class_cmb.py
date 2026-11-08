"""Full-spectrum likelihood for class_fading_patch.py: Planck 2018 plik-lite TTTEEE with the two low-l TT bins (planck-lite-py, Prince and Dunkley), a tau prior 0.0544 +- 0.0073 in place of low-l EE, A_planck 1 +- 0.0025, DESI DR2 BAO, one SN sample with M marginalised.
Lensed spectra with halofit (default CLASS precision; Delta chi2 numerical noise is measured in class_controls.py).  Unlike dark_like.py this sees ISW, lensing and the fifth force on CDM.  r_d, H and D_M all come from CLASS.
The chi2 is a sum of squares, so fits use Levenberg-Marquardt with a forward-difference Jacobian and Broyden updates: about 25 CLASS runs per fit instead of thousands.  The result is a local optimum from the start given."""
import os
import re
import subprocess
import tempfile
import numpy as np
import scipy.linalg
from scipy.io import FortranFile
import dark_like as L

HOME = os.path.expanduser("~/cosmo")
CLASSBIN = HOME + "/class_fading/class"
MONOBIN = os.path.expanduser("~/cosmo/class_mono/class")
KLTBIN = os.path.expanduser("~/cosmo/class_klt/class")
PL = HOME + "/planck-lite-py/data"
SND = HOME + "/snsdata"
TCMB = 2.7255e6
NAMES = ["wb", "wc", "h", "lnA", "ns", "tau", "A"]
STEP = dict(wb=1.2e-4, wc=8e-4, h=4e-3, lnA=0.012, ns=0.003, tau=0.006, A=0.002, c=0.04, cp=0.006, w0=0.02, wa=0.08)
# default CLASS jitter is about 0.1 in chi2 and its shooting tolerance of 1e-4 offsets scf from native Lambda by 0.3; measured in class_controls.py
PRECISION = """tol_shooting_deltax_rel=1e-9
tol_shooting_deltax=1e-9
tol_shooting_deltaF=1e-9
tol_perturbations_integration=1e-6
perturbations_sampling_stepsize=0.05
l_logstep=1.08
l_linstep=25
q_linstep=0.25
k_step_sub=0.04
k_step_super=0.002
k_step_transition=0.1
hyper_sampling_flat=12
k_min_tau0=0.5"""
START = dict(wb=0.02236, wc=0.1195, h=0.68, lnA=3.04, ns=0.966, tau=0.055, A=1.0)


def titles(path):
    line = [x for x in open(path) if x.startswith("#")][-1]
    return [x.strip() for x in re.findall(r"\d+:(.+?)(?=\s+\d+:|\s*$)", line)]


class Planck:
    def __init__(self):
        d = PL + "/planck2018_plik_lite/"
        low = PL + "/planck2018_low_ell/"
        _, x, _ = np.genfromtxt(d + "cl_cmb_plik_v22.dat", unpack=True)
        _, xl, sl = np.genfromtxt(low + "CTT_bin_low_ell_2018.dat", unpack=True)
        self.data = np.r_[xl, x]
        bmin, bmax, w = np.loadtxt(d + "blmin.dat").astype(int), np.loadtxt(d + "blmax.dat").astype(int), np.loadtxt(d + "bweight.dat")
        lmin, lmax, wl = np.loadtxt(low + "blmin_low_ell.dat").astype(int), np.loadtxt(low + "blmax_low_ell.dat").astype(int), np.loadtxt(low + "bweight_low_ell.dat")
        self.tt = [(a + 2, wl[a:b + 1]) for a, b in zip(lmin, lmax)] + [(bmin[i] + 30, w[bmin[i]:bmax[i] + 1]) for i in range(215)]
        self.pp = [(bmin[i] + 30, w[bmin[i]:bmax[i] + 1]) for i in range(199)]
        f = FortranFile(d + "c_matrix_plik_v22.dat", "r")
        cov = f.read_reals(dtype=float).reshape((613, 613))
        for i in range(613):
            for j in range(i, 613):
                cov[i, j] = cov[j, i]
        F = np.zeros((615, 615))
        F[:2, :2] = np.diag(1 / sl ** 2)
        F[2:, 2:] = scipy.linalg.cho_solve(scipy.linalg.cho_factor(cov), np.eye(613))
        self.U = np.linalg.cholesky(F).T

    def resid(self, cl, A):
        """cl: dict of C_l (microK^2) arrays indexed by l from 0."""
        b = lambda c, bins: np.array([np.sum(c[a:a + len(w_)] * w_) for a, w_ in bins])
        model = np.r_[b(cl["tt"], self.tt), b(cl["te"], self.pp), b(cl["ee"], self.pp)] / A ** 2
        return self.U @ (self.data - model)


class SN:
    def __init__(self, ds):
        s = L.load_sn(ds, SND)
        self.s = s
        self.U = np.linalg.cholesky(s["IC"]).T

    def resid(self, zc, dc):
        s = self.s
        r = s["MU"] - 5 * np.log10((1 + s["ZH"]) * np.interp(s["ZC"], zc, dc))
        return self.U @ (r - (s["ones"] @ r) / s["sum"])


def bao_resid(z_, H, dc, rd):
    out = []
    for d in L.DATA:
        z = d[0]
        DM = float(np.interp(z, z_, dc)) / rd
        DH = 1 / float(np.interp(z, z_, H)) / rd
        if d[1] == "V":
            out.append(((z * DM ** 2 * DH) ** (1 / 3) - d[2]) / d[3])
        else:
            a, b, r = (DM - d[2]) / d[3], (DH - d[4]) / d[5], d[6]
            out += [a, (b - r * a) / np.sqrt(1 - r * r)]
    return np.array(out)


def run_class(p, kind="fading", extra="", binp=CLASSBIN, keep=None):
    tag = tempfile.mkdtemp(prefix="cl_", dir="/tmp")
    ini = [f"h={p['h']}", f"omega_b={p['wb']}", f"omega_cdm={p['wc']}", "N_ur=2.0328", "N_ncdm=1", f"m_ncdm={p.get('mnu', 0.06)}", "T_cmb=2.7255", f"ln10^{{10}}A_s={p['lnA']}", f"n_s={p['ns']}", f"tau_reio={p['tau']}", "output=tCl,pCl,lCl,mPk", "lensing=yes", "non_linear=halofit", "l_max_scalars=2600", "P_k_max_1/Mpc=10", f"root={tag}/o", "write_background=yes", "overwrite_root=yes", "thermodynamics_verbose=1", "fourier_verbose=1"]
    if kind == "fading":
        ini += ["Omega_Lambda=0", "Omega_fld=0", "Omega_scf=-1", "attractor_ic_scf=no", f"scf_parameters={p.get('c', 0.0)},{p.get('cp', 0.0)},2.0,0.0,0.0", "scf_tuning_index=2"]
    elif kind == "mono":
        # axion-monodromy running coupling (class_monodromy_patch.py): Fi = 1/F; Fi = 0 is the constant-c' fading model
        ini += ["Omega_Lambda=0", "Omega_fld=0", "Omega_scf=-1", "attractor_ic_scf=no", f"scf_parameters={p.get('c', 0.0)},{p.get('cp', 0.0)},2.0,{p.get('Fi', 0.0)},0.0,0.0", "scf_tuning_index=2"]
        if binp == CLASSBIN:
            binp = MONOBIN
    elif kind == "klt":
        # Khoury-Lin-Trodden-family model (class_klt_patch.py): s = sigma_N/m0 (ks), f in M_P (kf), initial angle theta_i (kth), phi_ini = theta_i f
        ini += ["Omega_Lambda=0", "Omega_fld=0", "Omega_scf=-1", "attractor_ic_scf=no", f"scf_parameters=0.0,{p['ks']},2.0,{p['kf']},{p['kth'] * p['kf']},0.0", "scf_tuning_index=2"]
        if binp == CLASSBIN:
            binp = KLTBIN
    elif kind == "cpl":
        ini += ["Omega_Lambda=0", f"w0_fld={p['w0']}", f"wa_fld={p['wa']}", "fluid_equation_of_state=CLP", "use_ppf=yes"]
    ini.append(PRECISION)
    over = {x.split("=")[0] for x in extra.splitlines() if "=" in x}
    ini = [x for x in ini if x.split("=")[0] not in over]
    ini.append(extra)
    open(tag + "/i.ini", "w").write("\n".join(ini) + "\n")
    r = subprocess.run([binp, tag + "/i.ini"], capture_output=True, text=True, cwd=tag)
    if r.returncode != 0:
        subprocess.run(["rm", "-rf", tag])
        raise RuntimeError(r.stdout[-500:])
    fcl = tag + "/o_cl_lensed.dat"
    d = np.loadtxt(fcl)
    cols = titles(fcl)
    ells = d[:, 0].astype(int)
    fac = TCMB ** 2 * 2 * np.pi / (ells * (ells + 1))
    cl = {}
    for n, k in (("tt", "TT"), ("ee", "EE"), ("te", "TE")):
        a = np.zeros(ells.max() + 1)
        a[ells] = d[:, cols.index(k)] * fac
        cl[n] = a
    fb = tag + "/o_background.dat"
    b = np.loadtxt(fb)
    bc = titles(fb)
    z = b[:, bc.index("z")][::-1]
    H = b[:, bc.index("H [1/Mpc]")][::-1]
    dc = b[:, bc.index("comov. dist.")][::-1]
    info = dict(rd=float(re.search(r"comoving sound horizon rs = ([\d.]+)", r.stdout).group(1)), s8=float(re.search(r"sigma8=([\d.]+) for total", r.stdout).group(1)), H0=float(H[0]))
    crit = b[-1, bc.index("(.)rho_crit")]
    info["om"] = float((b[-1, bc.index("(.)rho_cdm")] + b[-1, bc.index("(.)rho_b")] + (b[-1, bc.index("(.)rho_idm")] if "(.)rho_idm" in bc else 0.0)) / crit)
    info["S8"] = info["s8"] * (info["om"] / 0.3) ** 0.5
    if "phi_scf" in bc:
        ph = b[:, bc.index("phi_scf")][::-1]
        info["phi0"] = float(ph[0])
        info["phi_rec"] = float(np.interp(1090.0, z, ph))
    if keep is not None:
        keep.update(z=z, H=H, dc=dc, cols=bc, raw=b, tag=tag, stdout=r.stdout)
    else:
        subprocess.run(["rm", "-rf", tag])
    return cl, z, H, dc, info


class Fitter:
    def __init__(self, ds, use_bao=True):
        self.pl = Planck()
        self.sn = SN(ds) if ds != "none" else None
        self.use_bao = use_bao
        self.n = 0

    def resid(self, p, kind):
        cl, z, H, dc, info = run_class(p, kind)
        self.n += 1
        parts = dict(cmb=self.pl.resid(cl, p["A"]), pri=np.array([(p["A"] - 1) / 0.0025, (p["tau"] - 0.0544) / 0.0073]))
        if self.use_bao:
            parts["bao"] = bao_resid(z, H, dc, info["rd"])
        if self.sn is not None:
            parts["sn"] = self.sn.resid(z, dc)
        return np.concatenate(list(parts.values())), {k: float(v @ v) for k, v in parts.items()}, info

    def fit(self, x0, free, fixed=None, kind="fading", tie=None, iters=10, log=print):
        """x0: dict, free: names varied, fixed: dict, tie(p) sets derived entries."""
        p0 = dict(x0, **(fixed or {}))

        def P(v):
            p = dict(p0)
            p.update(dict(zip(free, v)))
            if tie:
                tie(p)
            p["tau"] = max(p["tau"], 0.01)
            return p

        scale = np.array([STEP[n] for n in free])
        v = np.array([p0[n] for n in free], float)

        def jac(v, r0):
            J = np.zeros((len(r0), len(v)))
            for i in range(len(v)):
                v2 = v.copy()
                v2[i] += scale[i]
                r2, _, _ = self.resid(P(v2), kind)
                J[:, i] = (r2 - r0) / scale[i]
            return J

        r, parts, info = self.resid(P(v), kind)
        chi = r @ r
        J = jac(v, r)
        mu = 1e-3
        fresh = True
        for it in range(iters):
            g = J.T @ r
            H_ = J.T @ J
            D = np.diag(np.diag(H_))
            chi2 = np.inf
            for _ in range(6):
                dv = -np.linalg.solve(H_ + mu * D, g)
                try:
                    r2, parts2, info2 = self.resid(P(v + dv), kind)
                    chi2 = r2 @ r2
                except RuntimeError:
                    chi2 = np.inf
                if chi2 < chi:
                    break
                mu *= 5
            log(f"  it {it} chi2 {chi:.3f} -> {chi2:.3f} mu {mu:.1e} runs {self.n}", flush=True)
            if not chi2 < chi:
                if fresh:
                    break
                J = jac(v, r)
                fresh = True
                continue
            dr = r2 - r
            J = J + np.outer(dr - J @ dv, dv) / (dv @ dv)  # Broyden
            gain = chi - chi2
            v, r, chi, parts, info = v + dv, r2, chi2, parts2, info2
            mu = max(mu / 5, 1e-5)
            fresh = False
            if gain < 0.05:
                J = jac(v, r)
                fresh = True
                g2 = J.T @ r
                pred = g2 @ np.linalg.solve(J.T @ J, g2)
                log(f"  refresh: predicted further gain {pred:.3f}", flush=True)
                if pred < 0.1:
                    break
        return dict(chi2=float(chi), parts=parts, p={k: float(x) for k, x in P(v).items()}, info=info, runs=self.n)
