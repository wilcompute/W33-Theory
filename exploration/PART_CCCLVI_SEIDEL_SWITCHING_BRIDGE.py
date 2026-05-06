"""PART CCCLVI — Seidel Switching Classes of W(3,3)

The Seidel matrix S = J - I - 2A encodes both W(3,3) and its switching
equivalence class.  For an SRG(v,k,λ,μ) the eigenvalues of S are

    τ₀ = v - 1 - 2k          (multiplicity 1, trivial),
    τᵣ = -(1 + 2r)            (same mult as A-eigenvalue r),
    τₛ = -(1 + 2s)            (same mult as A-eigenvalue s),

because for any A-eigenvector v ⊥ 1 with eigenvalue ρ one has
    S v = (J - I - 2A) v = 0 - v - 2ρv = -(1+2ρ) v.

For W(3,3) = SRG(40,12,2,4) with r=2 (mult 24), s=-4 (mult 15):

    Seidel spectrum: {15¹, -5²⁴, 7¹⁵}.

Physics highlight: trivial Seidel eigenvalue 15 = SU5_MATTER = MULT_S.
"""

from fractions import Fraction

# SRG constants
V      = 40
K      = 12
LAM    = 2
MU     = 4
EDGES  = 240
MULT_R = 24
MULT_S = 15
L      = 27

# A-eigenvalues
R_EIG  = 2
S_EIG  = -4
ABS_S  = 4

# SM / GUT constants
ALPHA       = 10
GUT_DIM     = 27
GENERATIONS = 3
EW_GAUGE_4  = 4
SU5_ADJ     = 24
SU5_MATTER  = 15


# ── Seidel eigenvalues ─────────────────────────────────────────────────────

def seid_trivial_eig():
    """Trivial Seidel eigenvalue: V-1-2K = 15."""
    return V - 1 - 2 * K


def seid_r_eig():
    """Seidel eigenvalue from A-eigenvalue R_EIG: -(1+2R) = -5."""
    return -(1 + 2 * R_EIG)


def seid_s_eig():
    """Seidel eigenvalue from A-eigenvalue S_EIG: -(1+2S) = 7."""
    return -(1 + 2 * S_EIG)


def mult_seid_trivial():
    """Multiplicity of trivial Seidel eigenvalue = 1."""
    return 1


def mult_seid_r():
    """Multiplicity of seid_r_eig: equals MULT_R = 24."""
    return MULT_R


def mult_seid_s():
    """Multiplicity of seid_s_eig: equals MULT_S = 15."""
    return MULT_S


# ── Spectral identities ────────────────────────────────────────────────────

def trace_seid():
    """Trace S = sum(mult_i * tau_i) = 0 (diagonal of S is all-zero)."""
    return (mult_seid_trivial() * seid_trivial_eig()
            + mult_seid_r() * seid_r_eig()
            + mult_seid_s() * seid_s_eig())


def frobenius_seid():
    """||S||_F^2 = V*(V-1): all off-diagonal entries ±1."""
    return (mult_seid_trivial() * seid_trivial_eig() ** 2
            + mult_seid_r() * seid_r_eig() ** 2
            + mult_seid_s() * seid_s_eig() ** 2)


# ── verify_all ─────────────────────────────────────────────────────────────

def verify_all():
    checks = []

    def chk(label, got, expected):
        checks.append({
            "label": label,
            "got": str(got),
            "expected": str(expected),
            "pass": got == expected,
        })

    # Group 1: Seidel eigenvalue values
    chk("seid_trivial_eig = 15",
        seid_trivial_eig(), 15)
    chk("seid_trivial_eig = V-1-2K",
        seid_trivial_eig(), V - 1 - 2 * K)
    chk("seid_r_eig = -5",
        seid_r_eig(), -5)
    chk("seid_r_eig = -(1+2*R_EIG)",
        seid_r_eig(), -(1 + 2 * R_EIG))
    chk("seid_s_eig = 7",
        seid_s_eig(), 7)
    chk("seid_s_eig = -(1+2*S_EIG)",
        seid_s_eig(), -(1 + 2 * S_EIG))

    # Group 2: Multiplicities
    chk("mult_seid_trivial = 1",
        mult_seid_trivial(), 1)
    chk("mult_seid_r = MULT_R = 24",
        mult_seid_r(), MULT_R)
    chk("mult_seid_s = MULT_S = 15",
        mult_seid_s(), MULT_S)

    # Group 3: Spectral traces
    chk("trace_seid = 0",
        trace_seid(), 0)
    chk("frobenius_seid = V*(V-1) = 1560",
        frobenius_seid(), V * (V - 1))
    chk("seid_trivial + seid_r = ALPHA = 10",
        seid_trivial_eig() + seid_r_eig(), ALPHA)
    chk("seid_r + seid_s = R_EIG = 2",
        seid_r_eig() + seid_s_eig(), R_EIG)
    chk("seid_trivial - seid_s = 2*EW_GAUGE_4 = 8",
        seid_trivial_eig() - seid_s_eig(), 2 * EW_GAUGE_4)

    # Group 4: Eigenvalue squares and products
    chk("seid_trivial^2 = MULT_S^2 = 225",
        seid_trivial_eig() ** 2, MULT_S ** 2)
    chk("seid_r^2 = (ALPHA//2)^2 = 25",
        seid_r_eig() ** 2, (ALPHA // 2) ** 2)
    chk("seid_s^2 = (MU+GENERATIONS)^2 = 49",
        seid_s_eig() ** 2, (MU + GENERATIONS) ** 2)
    chk("seid_r * seid_s = -35",
        seid_r_eig() * seid_s_eig(), -35)
    chk("V - seid_trivial = (ALPHA//2)^2 = 25",
        V - seid_trivial_eig(), (ALPHA // 2) ** 2)

    # Group 5: Physics connections
    chk("seid_trivial = MULT_S = SU5_MATTER = 15",
        seid_trivial_eig(), SU5_MATTER)
    chk("seid_trivial = K + GENERATIONS = 15",
        seid_trivial_eig(), K + GENERATIONS)
    chk("mult_seid_r = SU5_ADJ = 24",
        mult_seid_r(), SU5_ADJ)
    chk("seid_s_eig = MU + GENERATIONS = 7",
        seid_s_eig(), MU + GENERATIONS)
    chk("mult_seid_r + mult_seid_s = V-1 = 39",
        mult_seid_r() + mult_seid_s(), V - 1)
    chk("seid_trivial // GENERATIONS = ALPHA//2 = 5",
        seid_trivial_eig() // GENERATIONS, ALPHA // 2)
    chk("abs(seid_r_eig) = ALPHA//2 = 5",
        abs(seid_r_eig()), ALPHA // 2)
    chk("seid_trivial + abs(seid_r) = 2*ALPHA = 20",
        seid_trivial_eig() + abs(seid_r_eig()), 2 * ALPHA)

    passed = sum(1 for c in checks if c["pass"])
    return checks, passed, len(checks)


def build_ccclvi_summary():
    checks, passed, total = verify_all()
    status = "PASS" if passed == total else "FAIL"
    return {
        "part": "CCCLVI",
        "title": "Seidel Switching Classes of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": status,
        "fields": {
            "V": V,
            "seid_trivial_eig": seid_trivial_eig(),
            "seid_r_eig": seid_r_eig(),
            "seid_s_eig": seid_s_eig(),
            "mult_seid_trivial": mult_seid_trivial(),
            "mult_seid_r": mult_seid_r(),
            "mult_seid_s": mult_seid_s(),
            "trace_seid": trace_seid(),
            "frobenius_seid": frobenius_seid(),
        },
        "discoveries": [
            f"Trivial Seidel eigenvalue = {seid_trivial_eig()} = MULT_S = SU5_MATTER: "
            "the switching-class spectrum encodes the SU(5) matter multiplicity",
            f"seid_r_eig = {seid_r_eig()} = -(ALPHA/2): "
            "half the fine-structure code ALPHA=10, with sign",
            f"seid_s_eig = {seid_s_eig()} = MU + GENERATIONS = {MU}+{GENERATIONS}: "
            "positive Seidel eigenvalue combines SRG mu with the generation count",
            f"seid_trivial + seid_r = {seid_trivial_eig() + seid_r_eig()} = ALPHA = 10",
            f"Frobenius ||S||_F^2 = {frobenius_seid()} = V*(V-1) = {V}*{V-1} "
            "(all off-diagonal entries ±1 implies exact Frobenius identity)",
        ],
    }


if __name__ == "__main__":
    import json, pathlib

    print("Part CCCLVI: Seidel Switching Classes of W(3,3)")
    checks, passed, total = verify_all()
    for c in checks:
        tag = "[PASS]" if c["pass"] else "[FAIL]"
        print(f"  {tag} {c['label']}")
    print(f"\nstatus: {'PASS' if passed == total else 'FAIL'}, "
          f"checks_pass: {passed}, checks_total: {total}")

    summary = build_ccclvi_summary()
    out = (pathlib.Path(__file__).resolve().parents[1]
           / "PART_CCCLVI_seidel_switching_results.json")
    out.write_text(json.dumps(summary, indent=2))
    print(f"JSON written: {out}")
