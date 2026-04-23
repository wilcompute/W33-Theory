#!/usr/bin/env python3
"""Browser audit for the public docs surfaces.

This is the browser/render companion to ``repo_doctor.py``:

- starts a local docs server automatically unless ``--base-url`` is provided
- audits every top-level public HTML page
- checks both desktop and mobile viewports
- opens the mobile navigator on the live paper and verifies the open state
- reports a repo-doctor style verdict in either human or JSON form

The audit is intentionally narrow. It is not a full visual-diff system; it is
an automated browser sanity pass for layout, navigation, and client-side
runtime failures.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
import argparse
import http.server
import json
import os
from pathlib import Path
import socketserver
import sys
import threading
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DEFAULT_PAGES = [
    "index.html",
    "qutrit_foundation.html",
    "repo_frontier_audit.html",
    "w33_busted_wide_open.html",
    "w33_complete_theory.html",
    "w33_monster_landauer.html",
    "w33_monster_landauer_final.html",
    "w33_q_integers_complete.html",
    "w33_the_apex.html",
    "w33_website.html",
]


try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - exercised in live environments
    sync_playwright = None


@dataclass
class Issue:
    page: str
    mode: str
    kind: str
    detail: str


class _DocsRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, directory: str, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:  # pragma: no cover
        return


@contextmanager
def _local_docs_server(docs_dir: Path) -> Any:
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

        def handle_error(self, request: object, client_address: tuple[str, int]) -> None:
            _, exc, _ = sys.exc_info()
            if isinstance(exc, (BrokenPipeError, ConnectionResetError)):
                return
            super().handle_error(request, client_address)

    server = ReusableTCPServer(
        ("127.0.0.1", 0),
        lambda *args, **kwargs: _DocsRequestHandler(
            *args, directory=str(docs_dir), **kwargs
        ),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


def _find_chromium_binary() -> str | None:
    env_path = os.environ.get("W33_PLAYWRIGHT_CHROME")
    if env_path and Path(env_path).exists():
        return env_path

    cache = Path.home() / ".cache" / "ms-playwright"
    candidates = sorted(cache.glob("chromium-*/chrome-linux*/chrome"), reverse=True)
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def _launch_env() -> dict[str, str]:
    env = dict(os.environ)
    lib_path = os.environ.get("W33_PLAYWRIGHT_LD_LIBRARY_PATH")
    fallback_candidates = [
        Path.home() / ".cache" / "w33-playwright-libs" / "usr" / "lib" / "x86_64-linux-gnu",
        Path("/tmp/pw-libs/usr/lib/x86_64-linux-gnu"),
    ]
    if not lib_path:
        for fallback in fallback_candidates:
            if fallback.exists():
                lib_path = str(fallback)
                break
    if lib_path:
        current = env.get("LD_LIBRARY_PATH")
        env["LD_LIBRARY_PATH"] = (
            lib_path if not current else f"{lib_path}:{current}"
        )
    return env


def _measure(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """
        () => {
          const nav = document.querySelector("nav.topnav");
          const sidebar = document.querySelector(".sidebar-toc");
          const hero = document.querySelector(".hero");
          const main = document.querySelector("main.page-content, main");
          const firstSection = document.querySelector("main section, section");
          const toggle = document.querySelector(".nav-toggle");
          const overlay = document.querySelector(".sidebar-overlay");
          const shell = document.querySelector(".snapshot-shell");
          const cs = getComputedStyle(document.documentElement);
          const bodycs = getComputedStyle(document.body);
          function box(el) {
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {
              top: r.top, left: r.left, right: r.right, bottom: r.bottom,
              width: r.width, height: r.height
            };
          }
          return {
            title: document.title,
            location: location.pathname,
            nav: box(nav),
            sidebar: box(sidebar),
            hero: box(hero),
            main: box(main),
            firstSection: box(firstSection),
            toggle: box(toggle),
            overlayOpen: Boolean(overlay && overlay.classList.contains("open")),
            navOpen: document.body.classList.contains("nav-open"),
            toggleExpanded: toggle ? toggle.getAttribute("aria-expanded") : null,
            toggleText: toggle ? toggle.innerText : null,
            bodyPaddingTop: bodycs.paddingTop,
            currentTopnavHeight: cs.getPropertyValue("--current-topnav-height").trim(),
            scrollPaddingTop: getComputedStyle(document.documentElement).scrollPaddingTop,
            snapshotShell: box(shell),
          };
        }
        """
    )


def _add_issue(issues: list[Issue], page: str, mode: str, kind: str, detail: str) -> None:
    issues.append(Issue(page=page, mode=mode, kind=kind, detail=detail))


def _check_live_index(metrics: dict[str, Any], mode: str, issues: list[Issue], page: str) -> None:
    nav = metrics["nav"]
    sidebar = metrics["sidebar"]
    hero = metrics["hero"]
    toggle = metrics["toggle"]
    if mode == "desktop":
        if not nav or not sidebar or not hero:
            _add_issue(issues, page, mode, "layout", "missing nav/sidebar/hero in desktop live shell")
            return
        if abs(sidebar["top"]) > 1:
            _add_issue(issues, page, mode, "layout", f"desktop sidebar top is {sidebar['top']}, expected 0")
        if abs(nav["left"] - sidebar["width"]) > 2:
            _add_issue(issues, page, mode, "layout", "desktop nav does not align to sidebar width")
        if hero["top"] + 1 < nav["bottom"]:
            _add_issue(issues, page, mode, "layout", "desktop hero overlaps sticky nav")
    else:
        if not nav or not sidebar or not hero or not toggle:
            _add_issue(issues, page, mode, "layout", "missing nav/sidebar/hero/toggle in mobile live shell")
            return
        nav_height = round(nav["height"])
        body_padding = round(float(metrics["bodyPaddingTop"].replace("px", "")))
        current_height = round(float(metrics["currentTopnavHeight"].replace("px", "")))
        if abs(nav["top"]) > 1:
            _add_issue(issues, page, mode, "layout", f"mobile nav top is {nav['top']}, expected 0")
        if abs(body_padding - current_height) > 2:
            _add_issue(issues, page, mode, "layout", "mobile body padding-top does not track measured nav height")
        if abs(nav_height - current_height) > 2:
            _add_issue(issues, page, mode, "layout", "mobile measured nav height drifted from CSS var")
        if sidebar["left"] > -1 and not metrics["navOpen"]:
            _add_issue(issues, page, mode, "layout", "mobile sidebar is visible even though nav is closed")


def _check_live_index_open(metrics: dict[str, Any], issues: list[Issue], page: str) -> None:
    nav = metrics["nav"]
    sidebar = metrics["sidebar"]
    if not nav or not sidebar:
        _add_issue(issues, page, "mobile-open", "layout", "missing nav/sidebar in mobile open state")
        return
    if not metrics["navOpen"] or not metrics["overlayOpen"]:
        _add_issue(issues, page, "mobile-open", "state", "mobile drawer did not enter open state")
    if metrics["toggleExpanded"] != "true":
        _add_issue(issues, page, "mobile-open", "state", "mobile toggle aria-expanded is not true")
    if sidebar["left"] < -1:
        _add_issue(issues, page, "mobile-open", "layout", "mobile sidebar is still off-canvas when open")
    if abs(sidebar["top"] - nav["bottom"]) > 2:
        _add_issue(issues, page, "mobile-open", "layout", "mobile sidebar top does not align to nav bottom")
    if "Close" not in (metrics["toggleText"] or ""):
        _add_issue(issues, page, "mobile-open", "state", "mobile toggle label did not switch to Close")


def _check_snapshot_page(metrics: dict[str, Any], mode: str, issues: list[Issue], page: str) -> None:
    if not metrics["title"]:
        _add_issue(issues, page, mode, "document", "snapshot page is missing a title")
    if not metrics["snapshotShell"]:
        _add_issue(issues, page, mode, "document", "snapshot shell wrapper is missing")


def run_audit(base_url: str) -> dict[str, Any]:
    if sync_playwright is None:
        return {
            "status": "error",
            "verdict": "missing_playwright",
            "detail": (
                "Playwright is not installed. Install it with "
                "`python -m pip install playwright` and then run "
                "`playwright install chromium`."
            ),
        }

    chrome = _find_chromium_binary()
    if not chrome:
        return {
            "status": "error",
            "verdict": "missing_browser",
            "detail": (
                "No Playwright Chromium binary was found. Set "
                "`W33_PLAYWRIGHT_CHROME` or run `playwright install chromium`."
            ),
        }

    issues: list[Issue] = []
    page_reports: list[dict[str, Any]] = []
    launch_env = _launch_env()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=chrome,
            args=["--disable-dev-shm-usage", "--no-sandbox"],
            env=launch_env,
        )
        try:
            for page_name in DEFAULT_PAGES:
                for mode, viewport in (
                    ("desktop", {"width": 1440, "height": 1200}),
                    ("mobile", {"width": 390, "height": 844}),
                ):
                    page = browser.new_page(viewport=viewport)
                    errors: list[dict[str, str]] = []
                    failed: list[dict[str, str]] = []
                    page.on(
                        "console",
                        lambda msg, errs=errors: errs.append(
                            {"type": msg.type, "text": msg.text}
                        )
                        if msg.type == "error"
                        else None,
                    )
                    page.on(
                        "pageerror",
                        lambda exc, errs=errors: errs.append(
                            {"type": "pageerror", "text": str(exc)}
                        ),
                    )
                    page.on(
                        "requestfailed",
                        lambda req, fails=failed: fails.append(
                            {"url": req.url, "failure": str(req.failure)}
                        ),
                    )
                    page.goto(f"{base_url}/{page_name}", wait_until="networkidle")
                    metrics = _measure(page)

                    if errors:
                        for err in errors:
                            _add_issue(
                                issues,
                                page_name,
                                mode,
                                "console",
                                f"{err['type']}: {err['text']}",
                            )
                    if failed:
                        for req in failed:
                            _add_issue(
                                issues,
                                page_name,
                                mode,
                                "request",
                                f"{req['url']} :: {req['failure']}",
                            )

                    if page_name == "index.html":
                        _check_live_index(metrics, mode, issues, page_name)
                        open_metrics = None
                        if mode == "mobile" and page.locator(".nav-toggle").count():
                            page.locator(".nav-toggle").click()
                            page.wait_for_timeout(300)
                            open_metrics = _measure(page)
                            _check_live_index_open(open_metrics, issues, page_name)
                        page_reports.append(
                            {
                                "page": page_name,
                                "mode": mode,
                                "metrics": metrics,
                                "open_metrics": open_metrics,
                            }
                        )
                    else:
                        _check_snapshot_page(metrics, mode, issues, page_name)
                        page_reports.append(
                            {
                                "page": page_name,
                                "mode": mode,
                                "metrics": metrics,
                            }
                        )
                    page.close()
        finally:
            browser.close()

    verdict = "healthy" if not issues else "issues_found"
    return {
        "status": "ok",
        "verdict": verdict,
        "page_count": len(DEFAULT_PAGES),
        "desktop_and_mobile_checked": True,
        "issues": [asdict(issue) for issue in issues],
        "page_reports": page_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Browser audit of docs pages at desktop and mobile widths."
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--base-url",
        default=None,
        help="existing docs base URL; if omitted the tool serves docs/ automatically",
    )
    args = parser.parse_args()

    if args.base_url:
        report = run_audit(args.base_url.rstrip("/"))
    else:
        with _local_docs_server(DOCS_DIR) as base_url:
            report = run_audit(base_url)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"browser_docs_audit verdict: {report['verdict']}")
        if report["status"] == "error":
            print(report["detail"])
        else:
            print(
                f"checked {report['page_count']} pages at desktop and mobile widths"
            )
            if report["issues"]:
                for issue in report["issues"]:
                    print(
                        f"- {issue['page']} [{issue['mode']}] {issue['kind']}: {issue['detail']}"
                    )

    return 0 if report.get("verdict") == "healthy" else 1


if __name__ == "__main__":
    raise SystemExit(main())
