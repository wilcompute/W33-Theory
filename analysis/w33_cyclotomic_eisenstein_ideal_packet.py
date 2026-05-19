"""Eisenstein prime-ideal packet for the split-prime cyclotomic ladder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import eisenstein_ideal_witness, eisenstein_split_ideal_data



def build_payload() -> dict[str, object]:
    return {
        "split_packets": {
            "7": eisenstein_split_ideal_data(7, power=3),
            "13": eisenstein_split_ideal_data(13, power=2),
            "19": eisenstein_split_ideal_data(19, power=2),
        },
        "witnesses": {
            "Phi3_q18": eisenstein_ideal_witness(18, "Phi3"),
            "Phi6_q19": eisenstein_ideal_witness(19, "Phi6"),
            "Phi3_q30": eisenstein_ideal_witness(30, "Phi3"),
        },
        "summary": {
            "statement": (
                "For each split prime p congruent to 1 mod 3, the two roots of x^2+x+1 modulo p^n define the two prime ideals above p in Z[ω], "
                "symbolically (p, ω-r). The Phi3 packet records divisibility of q-ω by powers of one of these ideals, while the Phi6 packet records divisibility of q+ω by the same split packet with negated residue branches."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_eisenstein_ideal_packet.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) EISENSTEIN PRIME-IDEAL PACKET")
    print("=" * 88)
    for key, packet in payload["split_packets"].items():
        print(f"p={key}: {[row['ideal_generator'] for row in packet['packet']]}")
    for key, witness in payload["witnesses"].items():
        print(f"{key}: {[row['statement'] for row in witness['ideal_witnesses']]}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
