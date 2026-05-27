#!/usr/bin/env python3
"""MCCCLXXXIV: measured and derived constant substrate witnesses.

This packet extends the SI defining-constant chain, but keeps the boundary
explicit: these are unit-scaled decimal witnesses.  Some entries are exact
by SI definition or convention; some are exact SI-derived constants rounded
to a displayed mantissa; and the genuinely measured constants are rounded
CODATA mantissas, not new exact definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


R = 2
Q = 3
MU = 4
QFACT = 6
F5 = 5
PHI3 = 13
PHI4 = 10
PHI6 = 7
PHI12 = 73
P_IH = 11
ALPHA_INT = 137
P10 = 29
P11 = 31
LEFF_ALPHA = P_IH * ((12 - 2) ** 2 + 1)  # 1111


def factorint(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


@dataclass(frozen=True)
class ConstantWitness:
    name: str
    class_name: str
    source_value: str
    scaled_integer: int
    decimal_reading: str
    substrate_form: str
    computed: int
    exponent_witness: str
    status: str

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "class": self.class_name,
            "source_value": self.source_value,
            "scaled_integer": self.scaled_integer,
            "decimal_reading": self.decimal_reading,
            "substrate_form": self.substrate_form,
            "computed": self.computed,
            "match": self.computed == self.scaled_integer,
            "factorization": factorint(self.scaled_integer),
            "exponent_witness": self.exponent_witness,
            "status": self.status,
        }


def build_witnesses() -> list[ConstantWitness]:
    g_inner = PHI12 * P10 + QFACT**2
    standard_g_inner = PHI12 * (Q**Q * PHI3 + 2**F5) + QFACT * PHI4
    atm_inner = 2**PHI6 + F5 * PHI3
    proton_inner_a = PHI4**2 + Q**2
    proton_inner_b = MU**4 + PHI3
    faraday_inner_minus = MU * ALPHA_INT - 1
    faraday_inner_plus = MU * ALPHA_INT + Q * PHI6
    gas_factor_a = F5 * PHI3 + R * PHI6 * PHI12
    gas_factor_b = PHI6 * LEFF_ALPHA - 2**PHI6

    return [
        ConstantWitness(
            name="Newtonian constant G",
            class_name="CODATA measured rounded mantissa",
            source_value="G = 6.67430(15)e-11 m^3 kg^-1 s^-2",
            scaled_integer=667430,
            decimal_reading="6.67430e-11 = 667430e-16",
            substrate_form="r*F5*p11*(Phi12*p10+(q!)^2)",
            computed=R * F5 * P11 * g_inner,
            exponent_witness="scientific exponent -11 = -p_Ih; integer scale -16 = -mu^2",
            status="measured value; substrate claim is for the CODATA displayed mantissa",
        ),
        ConstantWitness(
            name="standard gravity g0",
            class_name="conventional exact",
            source_value="g0 = 9.80665 m s^-2 exactly",
            scaled_integer=980665,
            decimal_reading="9.80665 = 980665e-5",
            substrate_form="F5*Phi6*(Phi12*(q^q*Phi3+2^F5)+q!*Phi4)",
            computed=F5 * PHI6 * standard_g_inner,
            exponent_witness="integer scale -5 = -F5",
            status="exact conventional standard, not a measured constant",
        ),
        ConstantWitness(
            name="standard atmosphere",
            class_name="conventional exact",
            source_value="1 atm = 101325 Pa exactly",
            scaled_integer=101325,
            decimal_reading="101325 Pa",
            substrate_form="q*F5^2*Phi6*(2^Phi6+F5*Phi3)",
            computed=Q * F5**2 * PHI6 * atm_inner,
            exponent_witness="integer exponent 0 = now",
            status="exact conventional standard, not a measured constant",
        ),
        ConstantWitness(
            name="proton mass energy equivalent",
            class_name="CODATA measured rounded mantissa",
            source_value="m_p c^2 = 938.27208943(29) MeV",
            scaled_integer=938272,
            decimal_reading="938.27208943 MeV rounds to 938272 keV = 9.38272e5 keV",
            substrate_form="2^F5*(Phi4^2+q^2)*(mu^4+Phi3)",
            computed=2**F5 * proton_inner_a * proton_inner_b,
            exponent_witness="keV scientific exponent 5 = F5; MeV scale -3 = -q",
            status="measured value; substrate claim is for nearest-keV rounded mantissa",
        ),
        ConstantWitness(
            name="Faraday constant",
            class_name="SI-derived exact rounded mantissa",
            source_value="F = N_A e = 96485.33212... C mol^-1",
            scaled_integer=9648533,
            decimal_reading="96485.33212... rounds to 9648533e-2 = 9.648533e4",
            substrate_form="p11*(mu*alpha_int-1)*(mu*alpha_int+q*Phi6)",
            computed=P11 * faraday_inner_minus * faraday_inner_plus,
            exponent_witness="scientific exponent 4 = mu; rounded-integer scale -2 = -r",
            status="exact SI-derived value; substrate claim is for displayed rounded mantissa",
        ),
        ConstantWitness(
            name="molar gas constant",
            class_name="SI-derived exact rounded mantissa",
            source_value="R = N_A k_B = 8.314462618... J mol^-1 K^-1",
            scaled_integer=8314463,
            decimal_reading="8.314462618... rounds to 8314463e-6",
            substrate_form="(F5*Phi3+r*Phi6*Phi12)*(Phi6*L_eff-2^Phi6)",
            computed=gas_factor_a * gas_factor_b,
            exponent_witness="micro-scale exponent -6 = -q!",
            status="exact SI-derived value; substrate claim is for 1e6-rounded mantissa",
        ),
    ]


def generate_payload() -> dict:
    witnesses = [w.as_dict() for w in build_witnesses()]
    exact_count = sum("exact" in item["class"] for item in witnesses)
    measured_count = sum(item["class"].startswith("CODATA measured") for item in witnesses)
    rounded_count = sum("rounded" in item["status"] or "rounded" in item["class"] for item in witnesses)

    checks = {
        "all_scaled_integers_match": all(item["match"] for item in witnesses),
        "classification_boundary_present": {
            item["class"] for item in witnesses
        }
        == {
            "CODATA measured rounded mantissa",
            "conventional exact",
            "SI-derived exact rounded mantissa",
        },
        "newton_G_mantissa": witnesses[0]["computed"] == 667430,
        "standard_gravity_exact": witnesses[1]["computed"] == 980665,
        "standard_atmosphere_exact": witnesses[2]["computed"] == 101325,
        "proton_keV_rounded": witnesses[3]["computed"] == 938272,
        "faraday_rounded": witnesses[4]["computed"] == 9648533,
        "molar_gas_rounded": witnesses[5]["computed"] == 8314463,
        "gas_constant_factorization": factorint(8314463) == {1087: 1, 7649: 1},
        "gas_factor_a": F5 * PHI3 + R * PHI6 * PHI12 == 1087,
        "gas_factor_b": PHI6 * LEFF_ALPHA - 2**PHI6 == 7649,
        "leff_alpha": LEFF_ALPHA == 1111,
        "not_all_entries_are_measured": measured_count < len(witnesses),
        "exact_or_derived_entries_present": exact_count >= 4,
        "rounded_boundary_present": rounded_count >= 4,
    }

    return {
        "theorem": "MCCCLXXXIV_MEASURED_DERIVED_CONSTANTS_SUBSTRATE_WITNESSES",
        "claim": (
            "Six non-SI-defining or derived constants have substrate-clean "
            "unit-scaled decimal witnesses when their exact/conventional/"
            "measured status is kept explicit."
        ),
        "boundary": (
            "This is a decimal unit-system witness layer, not a dimensionless "
            "prediction layer.  G and proton mass use rounded CODATA mantissas; "
            "g0 and atm are conventional exact values; Faraday and R are exact "
            "SI-derived constants but the promoted integers are rounded display "
            "mantissas."
        ),
        "sources": {
            "CODATA": "NIST CODATA 2022 values; G=6.67430(15)e-11, proton mass energy equivalent=938.27208943(29) MeV, Faraday=96485.33212..., R=8.314462618...",
            "SI": "NIST SI 2019 for exact defining constants; standard gravity and standard atmosphere are conventional exact standards.",
        },
        "witnesses": witnesses,
        "checks": checks,
        "verified": sum(value is True for value in checks.values()),
        "total_checks": len(checks),
        "all_verified": all(value is True for value in checks.values()),
    }


def main() -> None:
    payload = generate_payload()
    out = Path("data") / "w33_MCCCLXXXIV_measured_derived_constants_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("MCCCLXXXIV: MEASURED/DERIVED CONSTANT SUBSTRATE WITNESSES")
    print(f"verified: {payload['verified']}/{payload['total_checks']}")
    for item in payload["witnesses"]:
        print(f"  {item['name']}: {item['computed']} match={item['match']} [{item['class']}]")
    if not payload["all_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
