"""
THE HEAWOOD FORMULA IS PARAMETERIZED BY W(3,3)

genus(K_n) = ceil((n-q)(n-q-1)/k) = ceil((n-3)(n-4)/12)

Shift = q = 3 (field order)
Modulus = k = 12 (valence)

W(3,3) → W(3,3) MAP:
  K_{Phi6=7}  → genus 1 (Csaszar torus)
  K_{k=12}    → genus q!=6 (KO-dimension!)
  K_{Phi3=13} → genus 2^q=8 (Bott period!)
  K_{q^3=27}  → genus v+q!=46 (Monster exponent! = 1/sin^2 theta_13!)
  K_{v=40}    → genus 111 = q×37
  K_{qg=45}   → genus k^2=144

The Heawood formula maps W(3,3) parameters to W(3,3) parameters.
It is an ENDOMORPHISM of the W(3,3) parameter set.

From Ringel-Jungerman (1980): minimal triangulations on orientable surfaces.
The mod-12 constraint on graph embeddings is the mod-k constraint of W(3,3).
The (n-3) shift in Heawood IS the (n-q) shift.

Csaszar (7 vertices, genus 1) and Szilassi (7 faces, genus 1):
both n=Phi6=7, self-dual at genus 1.
"""
