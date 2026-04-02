"""Small helpers for optional runtime dependencies.

The repo's promoted theorem stack is large enough that some modules depend on
heavier scientific packages that are not part of the bare Python standard
library. When those dependencies are absent, we want a clear action item rather
than a raw ``ModuleNotFoundError`` with no context.
"""

from __future__ import annotations


def require_networkx(context: str):
    try:
        import networkx as nx  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised in user envs
        raise ModuleNotFoundError(
            f"{context} requires the optional dependency 'networkx'. "
            "Install the repo environment with "
            "`python3 -m pip install -r requirements-dev.txt` or run "
            "`./scripts/bootstrap_repo_env.sh`."
        ) from exc
    return nx
