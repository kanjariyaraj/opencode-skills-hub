#!/usr/bin/env python3
"""Generate theme-aware SVG assets used by the README.

Usage:
  python3 scripts/generate_assets.py          # write assets
  python3 scripts/generate_assets.py --check  # fail if assets are stale

Exit codes:
  0  generated or up to date
  1  --check found stale or missing assets
  2  usage or IO error
"""

from __future__ import annotations

import argparse
import html
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_indexes as indexes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _chip_width(label: str) -> int:
    return int(len(label) * 7.6 + 30)


def banner_svg(theme: str, resources: int, collections: int, categories: int) -> str:
    light = theme == "light"
    if light:
        bg = ("#f8fafc", "#eef2ff", "#e0e7ff")
        border = "#c7d2fe"
        title = "#0f172a"
        subtitle = "#4338ca"
        muted = "#475569"
        chip_fill = "#ffffff"
        chip_stroke = "#c7d2fe"
        chip_text = "#3730a3"
        accent = "#6366f1"
        accent2 = "#06b6d4"
    else:
        bg = ("#0b1120", "#111827", "#1e1b4b")
        border = "#312e81"
        title = "#f8fafc"
        subtitle = "#a5b4fc"
        muted = "#94a3b8"
        chip_fill = "#0b1120"
        chip_stroke = "#3730a3"
        chip_text = "#c7d2fe"
        accent = "#818cf8"
        accent2 = "#22d3ee"

    chips = [
        f"{resources} RESOURCES",
        f"{collections} COLLECTIONS",
        f"{categories} CATEGORIES",
        "EVIDENCE-FIRST",
    ]
    chip_markup = []
    x = 64
    for label in chips:
        width = _chip_width(label)
        chip_markup.append(
            f'<rect x="{x}" y="230" width="{width}" height="30" rx="15" '
            f'fill="{chip_fill}" stroke="{chip_stroke}" stroke-width="1.2"/>'
        )
        chip_markup.append(
            f'<text x="{x + width / 2:.1f}" y="250" text-anchor="middle" '
            f'font-family="{FONT}" font-size="11.5" font-weight="700" '
            f'letter-spacing="0.8" fill="{chip_text}">{_escape(label)}</text>'
        )
        x += width + 10

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="OpenCode Skills Hub">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg[0]}"/>
      <stop offset="0.55" stop-color="{bg[1]}"/>
      <stop offset="1" stop-color="{bg[2]}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}"/>
      <stop offset="1" stop-color="{accent2}"/>
    </linearGradient>
    <clipPath id="frame">
      <rect width="1200" height="300" rx="28"/>
    </clipPath>
  </defs>
  <rect width="1200" height="300" rx="28" fill="url(#bg)"/>
  <g clip-path="url(#frame)">
    <circle cx="1080" cy="30" r="190" fill="{accent}" opacity="0.10"/>
    <circle cx="940" cy="320" r="150" fill="{accent2}" opacity="0.08"/>
    <path d="M0 268 L1200 268" stroke="{border}" stroke-width="1" opacity="0.6"/>
  </g>
  <rect x="1" y="1" width="1198" height="298" rx="27" fill="none" stroke="{border}" stroke-width="1.5"/>
  <text x="64" y="66" font-family="{FONT}" font-size="12" font-weight="700" letter-spacing="3.4" fill="{subtitle}">OPENCODE ECOSYSTEM</text>
  <text x="62" y="136" font-family="{FONT}" font-size="56" font-weight="800" letter-spacing="-1.6" fill="{title}">OpenCode Skills Hub</text>
  <text x="64" y="176" font-family="{FONT}" font-size="22" font-weight="600" fill="{subtitle}">Discover. Build. Create. Automate.</text>
  <text x="64" y="206" font-family="{FONT}" font-size="15" fill="{muted}">An evidence-first catalog of skills, agents, plugins, MCP servers and collections.</text>
  {''.join(chip_markup)}
  <g transform="translate(820,50)">
    <rect width="316" height="200" rx="18" fill="#0b1120" stroke="#312e81" stroke-width="1.5"/>
    <circle cx="24" cy="26" r="5" fill="#f87171"/>
    <circle cx="42" cy="26" r="5" fill="#fbbf24"/>
    <circle cx="60" cy="26" r="5" fill="#34d399"/>
    <text x="24" y="68" font-family="{MONO}" font-size="12" fill="#94a3b8">$ query_catalog.py</text>
    <text x="24" y="94" font-family="{MONO}" font-size="12" fill="#7dd3fc">--category image-generation</text>
    <text x="24" y="120" font-family="{MONO}" font-size="12" fill="#7dd3fc">--sort security --reverse</text>
    <rect x="24" y="144" width="210" height="8" rx="4" fill="#1e293b"/>
    <rect x="24" y="144" width="128" height="8" rx="4" fill="url(#accent)"/>
    <text x="24" y="178" font-family="{FONT}" font-size="11" font-weight="600" fill="#86efac">4 high-risk entries surfaced</text>
  </g>
</svg>
'''


def coverage_svg(theme: str, ordered: list[dict], counts: Counter, date: str) -> str:
    light = theme == "light"
    if light:
        title_color = "#0f172a"
        subtitle_color = "#64748b"
        label_color = "#334155"
        track_color = "#e2e8f0"
        value_color = "#475569"
        zero_color = "#cbd5e1"
    else:
        title_color = "#f8fafc"
        subtitle_color = "#94a3b8"
        label_color = "#cbd5e1"
        track_color = "#1e293b"
        value_color = "#94a3b8"
        zero_color = "#334155"

    width = 1000
    top = 104
    step = 34
    height = top + len(ordered) * step + 52
    max_count = max(counts.values()) if counts else 1
    max_count = max(max_count, 1)
    bar_x = 330
    bar_max = 590

    rows = []
    for index, category in enumerate(ordered):
        count = counts.get(category["id"], 0)
        y = top + index * step
        baseline = y + 14
        if count:
            bar_width = max(6.0, round(count / max_count * bar_max, 1))
            rows.append(
                f'<rect x="{bar_x}" y="{y}" width="{bar_width}" height="18" rx="9" fill="url(#bar)"/>'
            )
        else:
            rows.append(
                f'<circle cx="{bar_x + 9}" cy="{y + 9}" r="3" fill="{zero_color}"/>'
            )
        rows.append(
            f'<text x="24" y="{baseline}" font-family="{FONT}" font-size="14" fill="{label_color}">{_escape(category["label"])}</text>'
        )
        rows.append(
            f'<text x="946" y="{baseline}" text-anchor="end" font-family="{FONT}" font-size="13" '
            f'font-weight="600" fill="{value_color}">{count}</text>'
        )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Catalog coverage by category">
  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6366f1"/>
      <stop offset="1" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <text x="24" y="40" font-family="{FONT}" font-size="23" font-weight="800" fill="{title_color}">Catalog coverage</text>
  <text x="24" y="66" font-family="{FONT}" font-size="13" fill="{subtitle_color}">Verified entries per category, sorted by coverage, as of {_escape(date)}.</text>
  <text x="946" y="40" text-anchor="end" font-family="{FONT}" font-size="13" font-weight="700" fill="{subtitle_color}">{sum(counts.values())} resources</text>
  {''.join(rows)}
  <text x="24" y="{height - 18}" font-family="{FONT}" font-size="11" fill="{subtitle_color}">Generated from catalog/*.json. Counts are entries, not popularity or quality.</text>
</svg>
'''


def render_outputs() -> dict[Path, str]:
    taxonomy, resources, collections = indexes.load_data()
    counts = Counter(resource.get("primary_category") for resource in resources)
    ordered = sorted(
        taxonomy["categories"],
        key=lambda item: (-counts.get(item["id"], 0), item["label"].casefold()),
    )
    date = max((resource.get("verification") or {}).get("date", "") for resource in resources)

    outputs: dict[Path, str] = {}
    for theme in ("light", "dark"):
        outputs[ASSETS_DIR / f"banner-{theme}.svg"] = banner_svg(
            theme, len(resources), len(collections), len(taxonomy["categories"])
        )
        outputs[ASSETS_DIR / f"coverage-{theme}.svg"] = coverage_svg(theme, ordered, counts, date)
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if generated assets differ from disk")
    args = parser.parse_args(argv)

    try:
        outputs = render_outputs()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        stale = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT))
        if stale:
            for path in stale:
                print(f"STALE {path}")
            return 1
        print(f"Checked {len(outputs)} asset(s); 0 stale.")
        return 0

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"Wrote or refreshed {len(outputs)} asset(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
