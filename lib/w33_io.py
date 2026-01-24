from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class W33DataPaths:
    """Resolve canonical W33 data locations in this repo."""

    repo_root: Path

    @staticmethod
    def from_this_file(file: str | Path) -> "W33DataPaths":
        p = Path(file).resolve()
        # Find the enclosing `claude_workspace` directory and take its parent as repo root.
        for parent in [p] + list(p.parents):
            if parent.name == "claude_workspace":
                return W33DataPaths(repo_root=parent.parent)
        # Fallback: locate the git repo root if present.
        for parent in [p] + list(p.parents):
            if (parent / ".git").exists():
                return W33DataPaths(repo_root=parent)
        # Final fallback: assume the file lives under the repo root.
        return W33DataPaths(repo_root=p.parent)

    @property
    def claude_workspace(self) -> Path:
        candidate = self.repo_root / "claude_workspace"
        return candidate if candidate.exists() else self.repo_root

    @property
    def data_root(self) -> Path:
        return self.claude_workspace / "data"

    @property
    def rays_csv(self) -> Path:
        return self.data_root / "_toe" / "w33_orthonormal_phase_solution_20260110" / "W33_point_rays_C4_complex.csv"

    @property
    def lines_csv(self) -> Path:
        return self.data_root / "_workbench" / "02_geometry" / "W33_line_phase_map.csv"


def load_w33_rays(paths: W33DataPaths) -> np.ndarray:
    """Load the 40 rays as a (40,4) complex numpy array."""

    df = pd.read_csv(paths.rays_csv)
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, row in df.iterrows():
        pid = int(row["point_id"])
        for i in range(4):
            V[pid, i] = complex(str(row[f"v{i}"]).replace(" ", ""))
    return V


def load_w33_lines(paths: W33DataPaths) -> List[Tuple[int, int, int, int]]:
    """Load the 40 lines; each line is a 4-tuple of point ids."""

    df = pd.read_csv(paths.lines_csv)
    lines: List[Tuple[int, int, int, int]] = []
    for _, row in df.iterrows():
        pts = tuple(map(int, str(row["point_ids"]).split()))
        if len(pts) != 4:
            raise ValueError(f"Expected 4 points per line, got {pts}")
        lines.append(tuple(sorted(pts)))
    if len(lines) != 40:
        # Not fatal, but it *should* be 40 for W33.
        raise ValueError(f"Expected 40 lines, got {len(lines)}")
    return lines


def simplices_from_lines(lines: Sequence[Tuple[int, int, int, int]]) -> dict[int, List[Tuple[int, ...]]]:
    """Build a simplicial complex (flag on each line as a K4).

    0-simplices: vertices (0..39)
    1-simplices: collinear pairs
    2-simplices: triples on a line
    3-simplices: the line itself (4 vertices)

    Returns a dict dim -> list of oriented simplices as sorted tuples.
    """

    verts = list(range(40))
    edges_set = set()
    tri_set = set()
    tet_set = set()

    for a, b, c, d in lines:
        tet = (a, b, c, d)
        tet_set.add(tet)
        # edges
        pts = [a, b, c, d]
        for i in range(4):
            for j in range(i + 1, 4):
                edges_set.add(tuple(sorted((pts[i], pts[j]))))
        # triangles
        for i in range(4):
            tri = tuple(sorted([p for k, p in enumerate(pts) if k != i]))
            tri_set.add(tri)

    simplices: dict[int, List[Tuple[int, ...]]] = {
        0: [(v,) for v in verts],
        1: sorted(edges_set),
        2: sorted(tri_set),
        3: sorted(tet_set),
    }

    return simplices
