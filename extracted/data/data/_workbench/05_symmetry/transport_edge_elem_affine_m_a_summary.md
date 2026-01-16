# Transport edge elements: affine maps on m and a

- m tuple order: (m0,m1,m2,m3). a tuple order: (a0,a1,a2,a3).
- Hyperplane functional: v*a = a0-a1-a2+a3 (mod 3) = sum m (mod 3).

## (0 1 2)
- verified: True
- rank: 20
- m map (B m + d):
  - B0 = [1, 0, 0, 0]
  - B1 = [0, 0, 1, 0]
  - B2 = [0, 0, 0, 1]
  - B3 = [0, 1, 0, 0]
  - d = [1, 1, 1, 1]
- a map (A a + c):
  - A0 = [1, 0, 0, 0]
  - A1 = [0, 0, 1, 0]
  - A2 = [0, 1, 1, 1]
  - A3 = [0, 0, 1, 2]
  - c = [1, 0, 0, 0]
- v*A = [1, 2, 2, 1] (should equal v)
- v*c shift: 1

## (0 2 1)
- verified: True
- rank: 20
- m map (B m + d):
  - B0 = [1, 0, 0, 0]
  - B1 = [0, 0, 0, 1]
  - B2 = [0, 1, 0, 0]
  - B3 = [0, 0, 1, 0]
  - d = [2, 2, 2, 2]
- a map (A a + c):
  - A0 = [1, 0, 0, 0]
  - A1 = [0, 1, 1, 1]
  - A2 = [0, 1, 0, 0]
  - A3 = [0, 1, 0, 2]
  - c = [2, 0, 0, 0]
- v*A = [1, 2, 2, 1] (should equal v)
- v*c shift: 2
