#!/usr/bin/env python3
"""Check local Markdown links and, optionally, external resource URLs.

Local mode is the default and is safe for pull requests. Network mode performs
HEAD requests with a GET range fallback and should be run on a schedule.

Exit codes:
  0  no broken links (or only soft failures)
  1  broken links detected
  2  usage or IO error
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".ruff_cache"}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
USER_AGENT = "opencode-skills-hub-link-checker/1.0 (+https://github.com/kanjariyaraj/opencode-skills-hub)"


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def extract_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in LINK_RE.finditer(text)]


def check_local(root: Path) -> list[str]:
    broken: list[str] = []
    for path in iter_markdown_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            broken.append(f"{path}: cannot read ({exc})")
            continue
        for raw in extract_links(text):
            if raw.startswith(EXTERNAL_PREFIXES) or raw.startswith("#") or raw.startswith("//"):
                continue
            target = urllib.parse.unquote(raw.split("#", 1)[0].strip())
            if not target:
                continue
            if target.startswith("/"):
                candidate = (root / target.lstrip("/")).resolve()
            else:
                candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                broken.append(f"{path.relative_to(root)}: link escapes repository: {raw}")
                continue
            if not candidate.exists():
                broken.append(f"{path.relative_to(root)}: missing target: {raw}")
    return broken


def collect_catalog_urls(root: Path) -> list[str]:
    urls: set[str] = set()
    for path in sorted((root / "catalog").glob("*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        stack = [document]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in {"url", "documentation"} and isinstance(value, str) and value.startswith(("http://", "https://")):
                        urls.add(value)
                    else:
                        stack.append(value)
            elif isinstance(node, list):
                stack.extend(node)
    return sorted(urls)


def probe(url: str, timeout: float) -> tuple[str, int | str]:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return ("ok", response.status)
    except urllib.error.HTTPError as exc:
        if exc.code in {400, 403, 405, 429}:
            get_request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"})
            try:
                with urllib.request.urlopen(get_request, timeout=timeout) as response:
                    return ("ok", response.status)
            except urllib.error.HTTPError as get_exc:
                return ("broken" if get_exc.code in {404, 410} else "soft", get_exc.code)
            except (urllib.error.URLError, TimeoutError) as exc2:
                return ("soft", str(exc2))
        return ("broken" if exc.code in {404, 410} else "soft", exc.code)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return ("soft", str(exc))


def check_network(urls: list[str], timeout: float, workers: int) -> tuple[list[str], list[str]]:
    broken: list[str] = []
    soft: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(probe, url, timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            state, detail = future.result()
            if state == "broken":
                broken.append(f"{url}: HTTP {detail}")
            elif state == "soft":
                soft.append(f"{url}: {detail}")
    return sorted(broken), sorted(soft)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    parser.add_argument("--network", action="store_true", help="also probe external URLs in catalog/")
    parser.add_argument("--all-links", action="store_true", help="with --network, probe every external link found in Markdown")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=8, help="network concurrency")
    parser.add_argument("--soft", action="store_true", help="treat network failures as warnings")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    broken_local = check_local(root)
    for item in broken_local:
        print(f"BROKEN {item}")

    broken_network: list[str] = []
    soft_network: list[str] = []
    if args.network:
        urls = collect_catalog_urls(root)
        if args.all_links:
            for path in iter_markdown_files(root):
                try:
                    text = path.read_text(encoding="utf-8")
                except OSError:
                    continue
                urls.extend(link for link in extract_links(text) if link.startswith(("http://", "https://")))
            urls = sorted(set(urls))
        broken_network, soft_network = check_network(urls, args.timeout, max(1, args.workers))
        for item in broken_network:
            print(f"BROKEN {item}")
        for item in soft_network:
            print(f"WARN   {item}")
        print(f"Probed {len(urls)} external URL(s).")

    failures = len(broken_local) + (0 if args.soft else len(broken_network))
    print(f"Local links checked. Broken local: {len(broken_local)}; broken external: {len(broken_network)}.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
