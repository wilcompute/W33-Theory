# Hyperplane + transport closure on a-space (Z3^4)

- Hyperplane functional v*a = a0-a1-a2+a3 (mod 3).
- Translation vectors t split by v*t: {0: 27, 1: 27, 2: 27}.
- Derived from translation/stabilizer structure (no brute-force enumeration).

## Translation subgroup sizes
- v*t=0 translations (hyperplane-preserving): 27
- full translations (Z3^4): 81

## Transport shift element
- shift c from (0 1 2) action on a: (1, 0, 0, 0)
- v*c = 1 (so it shifts hyperplanes by +1 mod 3)

## Closure size reasoning
- 1296 group = translations_v0 (27) semidirect stabilizer (48) -> 27*48 = 1296
- Adding the shift c generates all translations (81); stabilizer unchanged (A012 preserves v), so size = 81*48 = 3888
- Orbits on Z3^4: 1296 has three orbits of size 27 (v*a=0,1,2); extended closure is transitive on all 81.
