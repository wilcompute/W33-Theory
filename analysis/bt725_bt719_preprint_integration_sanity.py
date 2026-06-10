#!/usr/bin/env python3
"""BT725: sanity check for BT719 preprint integration.

This deliberately avoids rewriting the preprint itself.  The actual integration is
performed by tools/integrate_bt719.py.  This guard verifies the source section,
the integrator, and the insertion marker before/after the helper is run.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
section = ROOT/'paper/sections/sec_bt719_selector_classification.tex'
source = ROOT/'analysis/BT719_selector_uniqueness_tex_insert.tex'
integrator = ROOT/'tools/integrate_bt719.py'
preprint = ROOT/'paper/w33_preprint.tex'
line = r'\input{sections/sec_bt719_selector_classification}'
marker = r'\section{The TOE Singularity Theorem}'

text = preprint.read_text(encoding='utf-8')
result = {
    'theorem': 'BT725 BT719 Preprint Integration Sanity',
    'source_exists': source.exists(),
    'section_exists': section.exists(),
    'integrator_exists': integrator.exists(),
    'marker_exists': marker in text,
    'input_line_present': line in text,
    'safe_to_run_integrator': source.exists() and section.exists() and integrator.exists() and marker in text,
    'run_command': 'python tools/integrate_bt719.py',
    'postcondition': 'paper/w33_preprint.tex contains \\input{sections/sec_bt719_selector_classification} before the TOE Singularity section exactly once.'
}
assert result['safe_to_run_integrator']
print(json.dumps(result, indent=2, sort_keys=True))
