# All scalar harmonics in the D9 two-sphere flux background

This extends the [physical vector and first mixed scalar calculation](2026-11-16_D9_metric_maxwell_spectrum.md) to all angular levels in the classical two-derivative \(R-F^2/4\) theory. The general product-manifold stability theorem already applies to this flux background. The specialization below gives the actual scalar kernels, a proof of an even–odd spectral pairing, and the lightest scalar throughout the two-sphere branch. [Brown and Dahlen, general product-manifold spectrum](https://arxiv.org/abs/1310.6360)

Use AdS units, \(k_i=L^2/r_i^2>0\), \(k_1+k_2=20\), \(F_i=L^2 f_i^2=2k_i+8\), \(\lambda_i=k_i\ell_i(\ell_i+1)\), and \(\lambda=\lambda_1+\lambda_2\). The characteristic variable \(m\) denotes \(m_{\rm physical}^2 L^2\). The parity sectors are relative to the product scalar harmonic under simultaneous antipodal maps with Maxwell charge conjugation. This transformation preserves the magnetic background.

## Constraint-reduced scalar operators

For an active sphere write \(v_i=*_i dY_i\), \(d_i=\lambda_i/2-k_i\), and take as the trace-free even and odd tensors
\[
 S_i=\nabla_i dY_i+\tfrac12\lambda_i g_iY_i,\qquad
 T_i=\nabla_{(a} v_{i,b)} .
\]
Their divergences are \(-d_i dY_i\) and \(-d_i v_i\). Their internal Lichnerowicz eigenvalues are \(\lambda_i\), by commuting derivatives on the round sphere. Both vanish for \(\ell_i=1\). There are no independent transverse traceless tensors or harmonic one-forms on a round \(S^2\). With the product harmonics, the traces, these two tensor types, and the four gradient and coexact cross products exhaust the internal metric scalar profiles.

In the **even** sector use trace amplitudes \(U_i\), even tensor amplitudes \(E_i\) for \(\ell_i\ge2\), and the cross amplitudes \(C,D'\) of the previous calculation when both spheres are active. The external scalar Hessian and active external–internal gradients are removed by diffeomorphisms. The remaining external trace is \(H=-2(U_1+U_2)/3\). The external–internal Einstein constraints give the coexact Maxwell amplitudes \(s_i=f_i b_i=H-U_i+d_iE_i+\lambda_j C\) on active spheres, where \(j\ne i\). Set \(s_i=0\) on an inactive sphere and omit nonexistent tensor and cross amplitudes. Define \(P=\sum_i(\lambda_i s_i-F_i U_i)\). The scalar system is
\[
\begin{split}
 mU_i&=(\lambda+8+F_i)U_i-\lambda_i s_i+2P/7,\\
 mE_i&=(\lambda-2k_i)E_i-2s_i,\\
 mC&=(\lambda+8)C+D',\\
 mD'&=(\lambda+8)D'+F_1s_2+F_2s_1+F_1F_2 C .
\end{split}
\]
The tensor equation uses the trace-free Einstein projection and the fact that conjugation by the sphere's volume form reverses a symmetric trace-free tensor. Direct Maxwell projection gives \((m-\lambda-F_i)s_i+F_i(U_i+d_iE_i)-\lambda_j D'=0\). This and the external trace equation follow identically from the reduced block.

In the **odd** sector remove the scalar external shifts along coexact directions and use Maxwell gauge to remove the external longitudinal potential. Rescale the odd internal tensor and cross amplitudes by dividing by \(f_i\), and call them \(t_i,j_i\), respectively. The internal Maxwell amplitudes \(a_i\) along exact one-forms obey \(a_i=-d_i t_i-\lambda_j j_i\), and Maxwell imposes \(\sum_i\lambda_i a_i=0\). Thus a single active sphere has no odd scalar. For two active spheres use \(j_2=-j_1-\sum_i d_i t_i/\lambda_{3-i}\) and retain \(j_1\) and the available \(t_i\). The equations are
\[
 mt_i=(\lambda-2k_i)t_i+2a_i,\qquad
 mj_i=(\lambda+8)j_i+a_j-F_jj_j.
\]
These preserve the Maxwell constraint and imply the direct internal Maxwell projections \(ma_i=\lambda_j(a_i-a_j-F_i j_i+F_j j_j)\). This approach retains the mixing between the two spheres that the diagonal sphere profiles alone would miss. At a generic mixed harmonic the scalar counts are six even and three odd. Together with one massive spin two and four massive vectors this gives \(9+16+9=34\) polarizations, matching the nine-dimensional graviton and Maxwell field.

## Polynomial factorization and positivity

Set \(z=m-\lambda\) and \(p=k_1k_2\). With both harmonics at least two the odd characteristic polynomial is
\[
 O(z)=z[(z-8)^2-F_1F_2]-F_1\lambda_1(z+2k_2)-F_2\lambda_2(z+2k_1).
\]
The even characteristic polynomial is exactly \(O(z)R(z)\), where
\[
 R(z)=z^3-56z^2+
 \frac{3840+12p-12(F_1\lambda_1+F_2\lambda_2)}7z+
 \frac{16}{7}\sum_i F_i\lambda_i(10+k_j).
\]
Every odd eigenvalue therefore has an even partner. When a harmonic is one, \(d_i=0\) and the absent tensor removes the factor \(m-\lambda_j\) from both polynomials. With only one active sphere, the even polynomial is \(R\), with the zero factor removed for a dipole. For two constant harmonics it is the radion quadratic \(m^2-56m+(3840+12p)/7\). The factorization extends the paired \(m=96\) at \((1,1)\) to all mixed levels. A local symmetry operator exchanging the parity sectors has not been identified here.

For any nonconstant harmonic the cubic \(R\) has exactly one negative root in \(z\), by the coefficient signs of \(-R(-s)\). Its other two roots are positive: \(R(0)>0\), while at \(z_*=40-4\min(k_1,k_2)/3\) the coefficients of both \(\lambda_i\) in \(R\) are nonpositive and the zero-harmonic cubic is negative. Since \(R(z)\) rises to infinity, all three roots are real. At \(m=0\),
\[
 -7R(-\lambda)=\sum_i\lambda_i(\lambda_i-2k_i)(7\lambda_i+296-10k_i)
                +\lambda_1\lambda_2(21\lambda+112).
\]
This is strictly positive except for the removable single-sphere dipole root, proving that the lowest physical root is positive.

For \(O\), at \(z=-2k_i\) the value is \(2F_i(k_i-k_j)(\lambda_i-2k_i)\), so the signs at the two ordered \(-2k_i\), at zero, and at infinity give three real roots, including limiting cases by continuity. When both \(\ell_i\ge2\) one has \(\lambda\ge120\). If \(m\le8.1\), then \(s=\lambda-m\ge111.9\) and \(-O(-s)\ge s(s^2-32s-720-48m)>0\), excluding any such eigenvalue. If \(\ell_2=1,\ell_1\ge2\), the physical lower odd root is
\[
 \lambda+8+k_2-\sqrt{(8+k_2)^2+F_1\lambda_1+2k_1F_2}.
\]
At \(\lambda_1=2k_1\) it equals \(2k_2\), and its derivative with respect to \(\lambda_1\) is at least \(1/2\). Thus at the allowed \(\lambda_1\ge6k_1\) it is at least \(40\). Exchanging labels covers the other case. For two dipoles the only odd eigenvalue is \(96\). These analytic checks cover the unbounded harmonic tower, independently of a finite spectral scan.

## The global scalar gap and its anisotropic limit

Let \(k=\min(k_1,k_2)\), and put the larger sphere first. The lightest scalar is the lower of the lowest \(R\)-roots at \((2,0)\) and \((1,1)\). Three bounds give this reduction.

- For a single sphere of curvature \(k_i\), the negative-\(z\) root obeys
  \[
   m=\frac{s(s-2k_i)(7s+296-10k_i)}
           {F_i[12s+16(30-k_i)]},\qquad s=\lambda_i-m .
  \]
  This expression increases strictly for \(s\ge2k_i\), so the lowest mass among \(\ell_i\ge2\) is at \(\ell_i=2\). On the smaller sphere \(k_i\ge10\), assuming \(m\le8.1\) would give \(s\ge51.9\), \(s-2k_i\ge31.9\), and \(7s+296-10k_i\ge559.3\), while the denominator is at most \(76800\). The quotient would exceed \(8.1\). The physical radions and the single-sphere dipoles also exceed \(8.1\), by evaluating their quadratics at that value, below their vertices.
- The lowest \((1,1)\) root is below \(8.1\) over the entire branch by its [explicit cubic](2026-11-16_D9_metric_maxwell_spectrum.md). To compare against higher mixed levels, hold \(m\le8.1\) fixed and differentiate \(-7R(m-\lambda)\) with respect to \(\lambda_i\) for \(\lambda_i\ge2k_i\). Using \(F_1\lambda_1+F_2\lambda_2\le48\lambda-8p\), the derivative is at least
  \[
     21s^2-368s+3840-576m-7680
                  +k_j(24s+1712-76k_j)>0,
     \qquad s=\lambda-m\ge31.9 .
  \]
  The sign follows at the worst endpoints \(s=31.9,m=8.1\), with \(0<k_j<20\). The unique low root can therefore only increase when either mixed harmonic increases.
- The odd roots exceed the same budget by the preceding bounds. Their partners in the even sector obey those bounds as well.

The two global candidates cross once. Exact resultant isolation finds four possible common-root curvatures in \(0<k\le10\). Sign checks at separating trial masses discard three of them as coincidences involving higher roots. The physical crossing is at \(k\simeq2.6722\); the verifier records its precise curvature interval and the corresponding magnetic flux ratio. Its curvature has degree seven over the rationals, whereas any rational squared flux ratio would satisfy \( (20-k)^2(k+4)/[k^2(24-k)]\in\mathbb Q\) and give a nonzero polynomial in \(k\) of degree at most three. Therefore quantized fluxes select one side strictly. On the strongly unequal side the lightest scalar is the larger sphere's \(\ell=2\) mode. On the near-equal side it is the first mixed mode. This is separate from the vector crossover at \(k\simeq2.0834\).

The scalar gap is also the **first massive bosonic gap**. On a single sphere the vector's lower branch satisfies \(m=s(s-2k_i)/F_i\) at the same \(s=\lambda_i-m\). The corresponding scalar function multiplies this by \((7s+296-10k_i)/(12s+480-16k_i)<1\), with both functions increasing for \(s\ge2k_i\). Thus the single-sphere scalar root is lighter than its vector counterpart. In the \((1,1)\) sector the vector root \(v\) obeys \(v^2-88v+8p=0\). Inserting this into the mixed scalar cubic evaluated at \(v\) gives \(v(-13v^2+864v+7744)/14>0\), placing the first scalar root below \(v<11\). The minimum of the two scalar candidates is consequently below the vector gap. The first spin-two mass is \(2k\), and the mixed scalar cubic at \(2k\) equals \(160k(p+96)/7>0\). For \(2k\le16\) this puts the first scalar root below \(2k\), and for \(2k>16\) the \(8.1\) upper bound suffices.

For any fixed \(\ell\ge2\) on the larger sphere let \(n=\ell(\ell+1)\). The analytic low root has the expansion
\[
  m=\frac{37}{480}n(n-2)k^2+O(k^3).
\]
In particular \(m_{\rm gap}=37k^2/20+O(k^3)\) in the strongly unequal limit. In terms of the absolute magnetic flux ratio \(\rho\), this is asymptotic to \(370/(3\rho^2)\), below the vector's \(200/\rho^2\) in the same units. Thus taking a large flux ratio gives additional light scalar modes before the first massive spin-two mode enters. The conclusion concerns the classical spectrum with fixed flux integers and standard AdS fluctuation conditions. It does not determine nonlinear stability or the interactions of those modes.

The [verifier](toe_20261116_D9_scalar_spectrum.py) checks both reduced constraint systems, formal characteristic identities at unrestricted angular eigenvalues, exact resultant root isolation, and a finite numerical scan over independent harmonics through \(\ell_i=12\). See the [machine-readable certificate](../data/toe_20261116_D9_scalar_spectrum.json).
