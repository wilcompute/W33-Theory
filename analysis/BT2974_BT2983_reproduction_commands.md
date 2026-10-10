# Passes 2974–2983 reproduction commands

```bash
# Exact nonabelian, S6, receiver, R4/U6, scheduler, and A4/D4 closure
python analysis/bt2974_2981_nonabelian_golden_information_closure.py

# Fast deterministic sentinel for the general-isotropic search
python analysis/bt2977_general_isotropic_m36_search.py --quick 50000

# One exact duplicate-free RREF pivot shard; valid indices are 0..494
python analysis/bt2977_general_isotropic_m36_search.py --pivot-index 494

# Focused certificates and source boundaries
pytest -q tests/test_bt2974_bt2983_nonabelian_golden_information.py

# Idempotent promotion into both papers, the machine blueprint, and the live atlas
python tools/integrate_bt2974_bt2983.py
python tools/integrate_bt2974_bt2983.py --check
```

The complete M36 search is the union of the 495 `--pivot-index` jobs. Their outputs must be aggregated only after every shard completes and duplicate-free row counts sum to `213,648,435`.
