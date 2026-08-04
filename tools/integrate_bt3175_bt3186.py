#!/usr/bin/env python3
"""Idempotently integrate Passes 3175-3186 into canonical front doors.

The canonical manuscripts contain a small amount of legacy non-UTF-8 data.  Use
surrogateescape so every untouched byte round-trips exactly while the inserted block
remains ordinary UTF-8 text.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = [ROOT / 'w33_paper.tex', ROOT / 'photonic_holonet.tex', ROOT / 'holonet_machine_blueprint.tex']
HTML = ROOT / 'docs/index.html'
TB = '% BEGIN BT3175-BT3186 CURVATURE ROUTED INFERENCE'
TE = '% END BT3175-BT3186 CURVATURE ROUTED INFERENCE'
HB = '<!-- BEGIN BT3175-BT3186 CURVATURE ROUTED INFERENCE -->'
HE = '<!-- END BT3175-BT3186 CURVATURE ROUTED INFERENCE -->'
TEX_BLOCK = f"\n{TB}\n\\input{{analysis/BT3175_BT3186_curvature_routed_inference_insert}}\n{TE}\n"
HTML_BODY = (ROOT / 'analysis/BT3175_BT3186_curvature_routed_inference_index_insert.html').read_text(encoding='utf-8').strip()
HTML_BLOCK = f"\n{HB}\n{HTML_BODY}\n{HE}\n"


def read_preserving_bytes(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='surrogateescape')


def write_preserving_bytes(path: Path, text: str) -> None:
    path.write_text(text, encoding='utf-8', errors='surrogateescape')


def splice(text: str, begin: str, end: str, block: str, anchor: str) -> str:
    if begin in text:
        a = text.index(begin)
        b = text.index(end, a) + len(end)
        return text[:a] + block.strip('\n') + text[b:]
    p = text.rfind(anchor)
    if p < 0:
        raise RuntimeError(f'missing anchor {anchor}')
    return text[:p] + block + text[p:]


def main() -> None:
    for path in TEX:
        write_preserving_bytes(
            path,
            splice(read_preserving_bytes(path), TB, TE, TEX_BLOCK, '\\end{document}'),
        )
    write_preserving_bytes(
        HTML,
        splice(read_preserving_bytes(HTML), HB, HE, HTML_BLOCK, '</body>'),
    )
    print('BT3175-BT3186 integrated')


if __name__ == '__main__':
    main()
