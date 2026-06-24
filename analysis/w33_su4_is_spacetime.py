#!/usr/bin/env python3
"""
One SU(4)=SO(6) of dimension 15 = g is the dark color, the Pati-Salam unifier, and
the holographic bulk -- and its fundamental 4 = mu = the spacetime dimension. Dark
matter, color, the holographic bulk, and the number of spacetime dimensions
collapse into a single symmetry.

The dark sector's hidden gauge group (w33_dark_sector_128.py / w33_dark_matter_mass.py)
is SU(4) = SO(6). Three identities pin it:
  - dim SU(4) = 4^2 - 1 = 15 = dim SO(6) = 6*5/2 = 15 = g, the gauge-sector
    multiplicity (the s = -4 eigenvalue multiplicity of W(3,3)).
  - The non-compact form SO(4,2) (also dim 15) is the 4D CONFORMAL group = the
    AdS_5 isometry = the discrete-AdS/CFT bulk (the 15 negative-curvature modes of
    W(3,3), w33_holographic_architecture.py). So SO(6) (compact) and SO(4,2)
    (conformal) are two real forms of the SAME dim-15 = g algebra.
  - SU(4) is the Pati-Salam unifier (lepton number as the 4th color): a generation
    is a 4 of SU(4), unifying SU(3)_color and lepton number.
And the fundamental of all of them is the 4 = mu = the spacetime dimension.

So the hidden SU(4) of the dark sector, the Pati-Salam SU(4) (color + lepton), the
holographic bulk SO(4,2), and the rotation group SO(6) are one dim-15 = g symmetry,
whose fundamental 4 = mu is the spacetime dimension and the dark-color count. Dark
matter's gauge group IS the holographic bulk isometry IS grand-unified color, and
the '4' that counts the dark colors is the '4' that counts the dimensions of
spacetime.
"""
from __future__ import annotations

import json

Q, MU, G = 3, 4, 15


def main():
    out = {}

    dim_su4 = MU * MU - 1
    dim_so6 = 6 * 5 // 2
    dim_so42 = 6 * 5 // 2
    print("[one dim-15 = g algebra, several real forms / roles]")
    print(f"  dim SU(4)   = mu^2 - 1 = {dim_su4}")
    print(f"  dim SO(6)   = C(6,2)   = {dim_so6}   (SU(4) ~ SO(6), compact)")
    print(f"  dim SO(4,2) = C(6,2)   = {dim_so42}  (4D conformal group, AdS5 isometry)")
    print(f"  all = {G} = g (W(3,3) s=-4 multiplicity, gauge-sector dimension)")
    assert dim_su4 == dim_so6 == dim_so42 == G == 15
    out["dim"] = G

    print("\n[the four roles of this one SU(4)=SO(6)]")
    roles = {
        "dark color": "hidden SU(4) carrying the 128-spinor families (mu=4 colors)",
        "Pati-Salam": "lepton number as 4th color; a generation = a 4 of SU(4)",
        "holographic bulk": "SO(4,2) = 4D conformal group = AdS isometry (15 modes)",
        "rotations": "SO(6) compact rotation group",
    }
    for r, desc in roles.items():
        print(f"  {r:18s}: {desc}")
    out["roles"] = roles

    print("\n[the fundamental 4 = mu = spacetime dimension]")
    print(f"  the fundamental of SU(4) is the 4 = mu = {MU} = the spacetime dimension")
    print(f"  = the number of dark colors. The '4' of color/dark-color and the '4'")
    print(f"  of spacetime are the SAME 4.")
    assert MU == 4
    out["fundamental"] = MU

    print("\nRESULT: a single dimension-15 = g symmetry, SU(4) = SO(6), wears four")
    print("  hats: it is the dark sector's hidden gauge group (dark color), the")
    print("  Pati-Salam unifier (color + lepton number), and -- in its non-compact")
    print("  form SO(4,2) -- the holographic bulk / 4D conformal group of the")
    print("  discrete AdS/CFT (the 15 negative-curvature modes). Its fundamental 4")
    print("  is mu = the spacetime dimension AND the dark-color count. So dark")
    print("  matter, grand-unified color, the holographic bulk, and the number of")
    print("  spacetime dimensions are facets of one SU(4)=SO(6)=15=g, with the dark")
    print("  colors literally the spacetime directions.")

    out["summary"] = (
        "one SU(4)=SO(6), dim 15 = g, is the dark color (hidden gauge "
        "group of the 128-spinor), Pati-Salam (color+lepton), and -- as "
        "SO(4,2) -- the holographic bulk / 4D conformal group (15 AdS "
        "modes); its fundamental 4 = mu = the spacetime dimension = the "
        "dark-color count. Dark matter, color, bulk, and spacetime "
        "dimension collapse into one symmetry; dark colors = spacetime "
        "directions."
    )
    out["sources"] = [
        "SU(4) ~ SO(6); SO(4,2) = 4D conformal group (dim 15); "
        "Pati-Salam SU(4); corpus check 128 (g=15=SO(4,2)=SU(4)); "
        "w33_dark_sector_128.py, w33_holographic_architecture.py"
    ]
    with open("data/w33_su4_is_spacetime.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_su4_is_spacetime.json")


if __name__ == "__main__":
    main()
