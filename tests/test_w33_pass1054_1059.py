"""Regression tests for the six-way Pass-1054--1059 package."""
from __future__ import annotations

import importlib

import pytest

MODULES = [
    ("w33_pass1054_hessian_affine_isomorphism", 14),
    ("w33_pass1055_unsigned_equivariant_signed_obstruction", 10),
    ("w33_pass1056_two_648_class_fusions", 12),
    ("w33_pass1057_action_semantics_firewall", 8),
    ("w33_pass1058_central_c3_discriminator", 7),
    ("w33_pass1059_parallel_claim_audit", 24),
    ("w33_pass1059b_parallel_continue_audit", 9),
]


@pytest.mark.parametrize(("module_name", "expected_checks"), MODULES)
def test_pass(module_name: str, expected_checks: int) -> None:
    module = importlib.import_module(module_name)
    result = module.main()
    assert result["status"] == "PASS"
    assert result["check_count"] == expected_checks
    assert all(result["checks"].values())


def test_total_check_count() -> None:
    assert sum(expected for _, expected in MODULES) == 84
