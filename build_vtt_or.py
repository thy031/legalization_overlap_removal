#!/usr/bin/env python3
"""Generate sentence-level English, Chinese, and Bilingual WebVTT files."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "captions"
SHORT_END = 165.83  # Total video duration in seconds

TS_RE = re.compile(r"^(\d+):(\d{2})\s+[—–-]\s+.+$")


def format_ts(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def parse_blocks(md: str, heading: str) -> list[tuple[float, str]]:
    m = re.search(heading, md)
    if not m:
        raise SystemExit(f"Missing heading: {heading}")
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    if nxt:
        rest = rest[:nxt.start()]

    blocks, t0, buf = [], None, []
    for line in rest.splitlines():
        hit = TS_RE.match(line.strip())
        if hit:
            if t0 is not None and buf:
                blocks.append((t0, " ".join(buf)))
            t0 = int(hit.group(1)) * 60 + int(hit.group(2))
            buf = []
        elif t0 is not None and line.strip():
            buf.append(line.strip())
    if t0 is not None and buf:
        blocks.append((t0, " ".join(buf)))
    return blocks


def with_ends(blocks: list[tuple[float, str]], end: float) -> list[tuple[float, float, str]]:
    return [
        (a, blocks[i + 1][0] if i + 1 < len(blocks) else end, txt)
        for i, (a, txt) in enumerate(blocks)
    ]


def split_sentences(text: str, zh: bool = False) -> list[str]:
    pat = r"(?<=[。！？])" if zh else r"(?<=[.!?])\s+"
    return [p.strip() for p in re.split(pat, text.strip()) if p.strip()]


def align_pairs(en: str, zh: str) -> list[tuple[str, str]]:
    e = split_sentences(en, zh=False)
    z = split_sentences(zh, zh=True)
    while len(e) > len(z) and len(e) > 1:
        i = min(range(len(e)), key=lambda k: len(e[k]))
        j = 0 if i == 0 else i - 1
        e[j] = f"{e[j]} {e[j + 1]}"
        del e[j + 1]
    while len(z) > len(e) and len(z) > 1:
        i = min(range(len(z)), key=lambda k: len(z[k]))
        j = 0 if i == 0 else i - 1
        z[j] = f"{z[j]}{z[j + 1]}"
        del z[j + 1]
    return list(zip(e, z))


def write_vtt(path: Path, cues: list[tuple[float, float, str]]) -> None:
    lines = [
        "WEBVTT\n\n",
        "STYLE\n",
        "::cue {\n",
        "  font-size: clamp(14px, 1.65vw, 32px);\n",
        "  line-height: 1.38;\n",
        "}\n",
    ]
    for idx, (a, b, text) in enumerate(cues, 1):
        safe = text.replace("-->", "→")
        lines.append(f"\n{idx}\n{format_ts(a)} --> {format_ts(b)}\n{safe}\n")
    path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {path} ({len(cues)} cues)")


def main() -> None:
    en_blocks = with_ends(parse_blocks((ROOT / "transcript_en.md").read_text("utf-8"), r"## Short clip"), SHORT_END)
    zh_blocks = with_ends(parse_blocks((ROOT / "transcript_zh.md").read_text("utf-8"), r"## 短片"), SHORT_END)

    en_cues, zh_cues, bi_cues = [], [], []
    for (a0, b0, en_txt), (_, _, zh_txt) in zip(en_blocks, zh_blocks):
        pairs = align_pairs(en_txt, zh_txt)
        weights = [max(len(u.split()) + len(v) // 2, 1) for u, v in pairs]
        total = sum(weights)
        t = a0
        for i, ((u, v), w) in enumerate(zip(pairs, weights)):
            nxt = b0 if i == len(pairs) - 1 else t + (b0 - a0) * (w / total)
            en_cues.append((t, nxt, u))
            zh_cues.append((t, nxt, v))
            bi_cues.append((t, nxt, f"{u}\n{v}"))
            t = nxt

    OUT.mkdir(parents=True, exist_ok=True)
    write_vtt(OUT / "or-short-en.vtt", en_cues)
    write_vtt(OUT / "or-short-zh.vtt", zh_cues)
    write_vtt(OUT / "or-short-bilingual.vtt", bi_cues)


if __name__ == "__main__":
    main()