# BT1589 LG/OAM Radial-Shell Covariance Simulator

BT1589 models the OAM recenter ABI on three Laguerre-Gaussian radial shells. The leakage matrices form a commuting `L(eta)` channel family, so recentering and centered witness gates compose by `eta_total = eta_a + eta_b - 3 eta_a eta_b/2`. The worst symbolic case is `mixed_shift_phase + F3` with eta `0.18296`, below the recentered threshold `0.2`.
