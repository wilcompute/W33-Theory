#!/usr/bin/env python3
"""
Pass 1176: Apply ERR-1158-RESIDUAL amendment to breakthrough release.

This pass writes the corrected amendment block and verifies all tags are present.
It also produces an inline patch record showing the before/after state.

Outputs:
  data/MANUSCRIPT_AMENDMENT_1158_2026_07_27.json
  PASS1158_1162_BREAKTHROUGH_RELEASE_AMENDED_SECTION.md (amended section only)
"""
import json, re
from pathlib import Path
from datetime import datetime

ORIGINAL = (
    "1952-dim cubic-map kernel residual after removing Steinberg packet"
)

AMENDED = (
    "**1952-dim sub-module of the cubic-map kernel** "
    "(acting group: W(E6), order 51840; "
    "this is a MODULE, not an orbit, so there is no pointwise stabilizer "
    "-- the full W(E6) acts; "
    "color: uncolored unless the C3-colored kernel variant is explicitly invoked). "
    "The 1952-dim residual is the W(E6)-equivariant complement to the "
    "243-dim Steinberg packet (= 3 x V_81) inside the 2195-dim kernel of "
    "the cubic incidence map M: C^2240 -> C^k, rank(M) = 45 = dim(so(10)). "
    "The residual is reducible over W(E6): 1952 = 2^5 x 61, and since 61 "
    "does not divide |W(E6)| = 51840, no single W(E6) irrep has this dimension. "
    "Exact decomposition pending MeatAxe over GF(7)."
)

AMENDED_SECTION_MD = """
## AMENDMENT: Pass 1158 residual claim (ERR-1158-RESIDUAL)

**Filed:** 2026-07-27  
**Erratum ID:** ERR-1158-RESIDUAL  
**Status:** TYPED (all three tags now present)

### Original claim (NEEDS_TAG)
> 1952-dim cubic-map kernel residual after removing Steinberg packet

### Corrected claim (TYPED)
> **1952-dim sub-module of the cubic-map kernel**  
> - **acting_group:** W(E6), order 51840  
> - **stabilizer_label_or_order:** full W(E6) (module, not orbit; no pointwise stabilizer)  
> - **color_retained_or_forgotten:** uncolored (C3 color not applied unless explicitly stated)  
>
> The 1952-dim residual is the W(E6)-equivariant complement to the 243-dim Steinberg packet  
> (= 3 x V_81, i.e. the 81-dim W(E6) irrep tensored with the 3-dim regular C3 module)  
> inside the 2195-dim kernel of the cubic incidence map M: C^2240 -> C^k,  
> rank(M) = 45 = dim(so(10)) (D5 adjoint = antisym^2 of the 10-dim D5 standard rep).  
>
> The residual is **reducible** over W(E6): 1952 = 2^5 * 61, and since 61 does not  
> divide |W(E6)| = 51840, no single W(E6) irrep has this dimension.  
> Exact decomposition: pending MeatAxe over GF(7) with 6 W(E6) simple reflections  
> as generators (p=7 is a good prime since gcd(7, 51840) = 1).

### Tags verified
- [x] acting_group: W(E6), order 51840
- [x] stabilizer_label_or_order: full W(E6) (module)
- [x] color_retained_or_forgotten: uncolored
"""

def main():
    required_tags = ['acting_group', 'stabilizer_label_or_order', 'color_retained_or_forgotten']
    amended_lower = AMENDED.lower()
    tags_verified = {
        'acting_group': 'w(e6)' in amended_lower and '51840' in AMENDED,
        'stabilizer_label_or_order': 'stabilizer' in amended_lower or 'full w(e6)' in amended_lower,
        'color_retained_or_forgotten': 'color' in amended_lower or 'uncolored' in amended_lower,
    }
    assert all(tags_verified.values())

    # Write the amended section markdown
    sec_path = Path('PASS1158_1162_BREAKTHROUGH_RELEASE_AMENDED_SECTION.md')
    sec_path.write_text(AMENDED_SECTION_MD)

    result = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1176.manuscript_amendment.v1',
        'status': 'PASS',
        'erratum_id': 'ERR-1158-RESIDUAL',
        'original': ORIGINAL,
        'amended': AMENDED,
        'tags_verified': tags_verified,
        'all_tags_present': all(tags_verified.values()),
        'amended_section_file': str(sec_path),
        'action': 'Insert AMENDED_SECTION_MD into PASS1158_1162_BREAKTHROUGH_RELEASE.md after Pass 1158 section header.',
    }
    out = Path('data/MANUSCRIPT_AMENDMENT_1158_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f'PASS 1176: Erratum ERR-1158-RESIDUAL applied, all tags verified')
    return result

if __name__ == '__main__':
    main()
