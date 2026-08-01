# Complete mixed trivariate enumerator payload

The full 7,355-bin enumerator is reconstructed exactly by running:

```bash
g++ -O3 -fopenmp -std=c++20 analysis/cpp/w33_pass1908_mixed_dense_shard.cpp -o /tmp/pass1908
# Run the 156 residual-orbit shards, then:
python analysis/w33_pass1908_merge_mixed_trivariate.py <shard-directory>
```

Canonical sparse-histogram SHA-256:

`88ebaaa26631c25df99336e1aba3ca38c2973e9fa2da7de9d5e036e27c67e936`

Canonical complete-enumerator SHA-256 without its hash field:

`6806257aff50237fe5c49a7b4cfb5b8254df36dcd24c1fe949e1dbefdcd30042`

The compact certificate records the complete marginals, complement subgroup, exact symmetries, ordinary-enumerator cross-check, and all payload hashes. The repository intentionally stores the deterministic generators and compact certificate rather than an opaque encoded binary blob.
