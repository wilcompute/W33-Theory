
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
