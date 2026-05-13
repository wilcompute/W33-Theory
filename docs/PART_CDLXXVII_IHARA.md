# Part CDLXXVII — Ihara Zeta & Triangle Identities

## Edge and Ihara Structure

    Edges E = V*K/2 = u^3 = 216
    E - V = V*C_V = 189

## Ihara Zeta Function

    Z(u)^{-1} = (1-u^2)^{V*C_V} · (1-x^4*u+x^4*u^2)^1
                               · (1-x^2*u+x^4*u^2)^u
                               · (1+x*u+x^4*u^2)^20

All factors are pure power-of-x polynomials at x=2.

## Triangle Identity

    Tr(A^3) = K^3 + u*r^3 + 20*s^3
            = 4096 + 384 - 160 = 4320

    Triangles = Tr(A^3)/6 = 720 = u! = 6!

    720 / 3 = 240 = E8 roots  ✓

## Spectral Mult · log2 Dot Product

    1*log2(K) + u*log2(r) + 20*log2(|s|)
    = 1*4 + 6*2 + 20*1 = 36 = u^2 = log2(det A)
