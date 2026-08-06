#!/usr/bin/env python3
"""Focused regression for Passes 4081-4088."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p4081",ROOT/"analysis/w33_pass4081_4088_deep_physics.py")
MOD=importlib.util.module_from_spec(SPEC); assert SPEC.loader
SPEC.loader.exec_module(MOD)


def result():
    return MOD.verify()


def test_all_checks_hold(): assert result()["all_checks_hold"]
def test_semantic_certificate(): assert len(result()["semantic_sha256"])==64
def test_dark_dimension(): assert result()["dark_dimension"]==3161
def test_pair_pump_chern(): assert abs(result()["pair_pump_chern"]-1)<1e-10
def test_marked_edge_commutant(): assert result()["marked_edge_commutant_dimension"]==45
