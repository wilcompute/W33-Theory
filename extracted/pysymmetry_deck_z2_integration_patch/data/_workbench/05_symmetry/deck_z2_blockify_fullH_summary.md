# Deck Z2 blockify: full 59x24 Hamiltonian

Inputs:
- /mnt/data/repo2/data/_toe/projector_recon_20260110/N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz
- /mnt/data/repo2/data/_toe/projector_recon_20260110/N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz
- /mnt/data/repo2/data/_toe/projector_recon_20260110/TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz
- /mnt/data/repo2/data/_toe/projector_recon_20260110/N12_58_orbit0_edges_with_2T_connection_20260109T043900Z.csv

Defect edges toggled (e* -> e):
- (0,20)
- (10,12)
- (26,27)
- (27,45)

Sanity checks (should be exact zeros in this dataset):
- ||Ke^T H Ko||_F = 0.000000e+00
- ||ΔH_even||_F    = 0.000000e+00
- ||ΔH_odd||_F     = 1.959592e+01
