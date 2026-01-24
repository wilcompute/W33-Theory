#!/usr/bin/env python3
"""
Test script for SageMath + PySymmetry environment.
Run with: wsl -e bash run_sage.sh src/test_sage_pysymmetry.py
"""

import pytest

pytest.importorskip("sage")
pytest.importorskip("pysymmetry")

from sage.all import *
from pysymmetry import FiniteGroup, MapRepresentation
import numpy as np

print("=" * 60)
print("SAGE + PYSYMMETRY TEST")
print("=" * 60)

# Test 1: SageMath basics
print("\n1. SageMath basics:")
print(f"   Version: {version()}")
M = matrix(QQ, [[1, 2, 3], [4, 5, 6], [7, 8, 10]])
print(f"   3x3 matrix det: {M.det()}")
print(f"   Eigenvalues: {M.eigenvalues()}")

# Test 2: Group theory
print("\n2. Group theory:")
S3 = SymmetricGroup(3)
print(f"   S3 order: {S3.order()}")
print(f"   S3 conjugacy classes: {len(S3.conjugacy_classes())}")

# Test 3: PySymmetry integration
print("\n3. PySymmetry with Sage:")
G = FiniteGroup(S3)
print(f"   FiniteGroup(S3) created")
print(f"   Character table shape: {G.character_table().dimensions()}")

# Test 4: Symmetry reduction example
print("\n4. Symmetry reduction example:")
# Create a 6x6 S3-invariant matrix (S3 acts on indices 0,1,2 and 3,4,5)
n = 6
A = np.zeros((n, n))
# Fill with S3-symmetric pattern
for i in range(3):
    for j in range(3):
        A[i, j] = 1 if i == j else 0.5
        A[i+3, j+3] = 1 if i == j else 0.5
        A[i, j+3] = 0.3
        A[i+3, j] = 0.3

print(f"   Created 6x6 S3-symmetric matrix")
print(f"   Matrix:\n{A}")

# Test 5: Verify numpy integration
print("\n5. NumPy integration:")
eigenvalues = np.linalg.eigvalsh(A)
print(f"   Eigenvalues: {eigenvalues}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
