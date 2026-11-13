# Projected open-channel propagation on the monopole exterior

The existing full scattering producer replaces the residual scalar background by vacuum at radius 36. This control retains the same linearized scalar profile and continues its action on the eight vacuum light modes. Let F be the fixed radial flux form and let W contain the four outgoing and four incoming vacuum eigenmodes. The code checks W†FW = diag(I₄,−I₄) and projects the generator by W†GW. Each shell transfer preserves this indefinite flux form at real energy. Starting from the graph of the interior reflection matrix, the update multiplies its graph by the shell transfer and divides on the right by the incoming block. The updated reflection matrix remains unitary.

The control compares the projected shell against full radial scattering at two matching radii before extending the projected calculation farther. The open-to-closed leakage norm is reported separately. Eliminating closed channels exactly would add their feedback through a resolvent. The projected calculation omits that term and the closed components in the starting reflection graph. Its validation is numerical and local to the checked energies and shell. [Open and closed channel projection](https://www.rcnp.osaka-u.ac.jp/~hyodo/class/2020/Tokuron/)

All conversion probabilities use the same physical flavor frames as the earlier triplet scans. Replay with `py -3 analysis/toe_20261113_monopole_open_tail.py`. Use `--outer 5 --elements 100` for the alternate Robin background.

## Results

On the radius-9 Robin background, propagating the projected shell from 17.99 to 36 reproduces the full result at E = 0, 0.002 and 0.004 to within 5.6e−6 in Frobenius norm. The largest conversion discrepancy on that comparison shell is 1.7e−6. Starting from the full radius-36 matrix, the projected conversion at E=0.002 moves from 80.2151% to 80.6580%, 80.7381% and 80.7245% at radii 72, 144 and 288. The change from 144 to 288 reverses sign. The radius-5 Robin control reaches 80.7468% at 160. These values support a conversion around 80.7% at that specific energy in the projected model. The numbers do not give a rigorous tail error, an infinite-radius pole, or the location of a new global minimum.

The vacuum and constant-shell subdivision controls were checked separately. The first numerical attempt included an absolute flux-identity check on near-origin coefficients outside the projection's domain. Restricting the check to the shell and using logarithmic shell steps produced both certificates.
