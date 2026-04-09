"""Small helpers for optional runtime dependencies.

The promoted theorem stack is large enough that some modules depend on heavier
scientific packages beyond the Python standard library. When those are absent,
we want a clear action item rather than a raw ``ModuleNotFoundError``.
"""

from __future__ import annotations


def require_networkx(context: str):
    try:
        import networkx as nx  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised in user envs
        error = ModuleNotFoundError(
            f"{context} requires the optional dependency 'networkx'. "
            "Install the repo environment with "
            "`python3 -m pip install -r requirements-dev.txt` or run "
            "`./scripts/bootstrap_repo_env.sh`."
        )
        # Preserve the missing module identity so higher-level fallbacks that
        # branch on ``exc.name == 'networkx'`` keep working.
        error.name = "networkx"
        raise error from exc
    return nx
