#!/usr/bin/env bash
set -euo pipefail

bash tools/bt1340_run_extended_release_lock.sh
python tools/bt1378_verify_runtime_contract.py
python tools/bt1379_verify_s3_gauge_max2csp_spec.py
python tools/bt1380_verify_post_1377_bridge_index.py
python tools/bt1381_s3_gauge_global_solver_probe.py --restarts 20
python tools/bt1382_non_clifford_port_abi.py
python tools/bt1383_verify_runtime_frontier_integration.py
python tools/bt1384_export_s3_gauge_maxsat.py
python tools/bt1385_hesse_sic_t_port_abi.py
python tools/bt1388_hesse_sic_t_factory_model.py
python -m pytest -q tests/test_bt1378_bt1380_runtime_contracts.py tests/test_bt1381_bt1383_runtime_frontier.py tests/test_bt1384_bt1386_maxsat_port_paper.py tests/test_bt1387_bt1389_runtime_release_lock.py

echo "BT1389 runtime frontier release lock passed"
