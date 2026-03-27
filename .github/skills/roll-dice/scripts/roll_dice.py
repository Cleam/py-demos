#!/usr/bin/env python3
"""简单骰子表达式解析与掷点脚本。

用法:
  python scripts/roll_dice.py "1d20+5"
  python scripts/roll_dice.py "adv 1d20+3"
  python scripts/roll_dice.py "seed=42 4d6kh3"
"""

from __future__ import annotations

import random
import re
import sys
from dataclasses import dataclass


PATTERN = re.compile(
    r"^(?P<n>\d+)d(?P<m>\d+)(?:(?P<keep>k[hl])(?P<keep_n>\d+))?(?P<mod>[+-]\d+)?$",
    re.IGNORECASE,
)


@dataclass
class DiceExpr:
    n: int
    m: int
    keep_type: str | None
    keep_n: int | None
    mod: int


def parse(raw: str) -> tuple[DiceExpr, int | None, str]:
    text = raw.strip().lower()

    seed = None
    seed_match = re.search(r"\bseed=(\d+)\b", text)
    if seed_match:
        seed = int(seed_match.group(1))
        text = re.sub(r"\bseed=\d+\b", "", text).strip()

    if text.startswith("adv"):
        rest = text[3:].strip()
        if not rest:
            text = "2d20kh1"
        elif re.fullmatch(r"[+-]\d+", rest):
            text = f"2d20kh1{rest}"
        else:
            m_adv = re.fullmatch(r"1d20([+-]\d+)?", rest)
            if not m_adv:
                raise ValueError("adv 仅支持 d20 检定，示例: adv 1d20+3 或 adv +3")
            text = f"2d20kh1{m_adv.group(1) or ''}"
    elif text.startswith("dis"):
        rest = text[3:].strip()
        if not rest:
            text = "2d20kl1"
        elif re.fullmatch(r"[+-]\d+", rest):
            text = f"2d20kl1{rest}"
        else:
            m_dis = re.fullmatch(r"1d20([+-]\d+)?", rest)
            if not m_dis:
                raise ValueError("dis 仅支持 d20 检定，示例: dis 1d20+3 或 dis +3")
            text = f"2d20kl1{m_dis.group(1) or ''}"

    text = re.sub(r"\s+", "", text)
    if not text:
        text = "1d20"

    m = PATTERN.match(text)
    if not m:
        raise ValueError("表达式不合法，示例: 1d20+5, 4d6kh3, adv 1d20")

    n = int(m.group("n"))
    sides = int(m.group("m"))
    keep_type = m.group("keep")
    keep_n = int(m.group("keep_n")) if m.group("keep_n") else None
    mod = int(m.group("mod")) if m.group("mod") else 0

    if n < 1 or n > 200:
        raise ValueError("骰子个数 N 必须在 1..200")
    if sides < 2 or sides > 1000:
        raise ValueError("面数 M 必须在 2..1000")
    if keep_type and (keep_n is None or keep_n < 1 or keep_n > n):
        raise ValueError("kh/kl 保留数量必须在 1..N")

    expr = DiceExpr(n=n, m=sides, keep_type=keep_type, keep_n=keep_n, mod=mod)
    return expr, seed, text


def run(expr: DiceExpr) -> tuple[list[int], list[int], int]:
    rolls = [random.randint(1, expr.m) for _ in range(expr.n)]

    if expr.keep_type == "kh":
        kept = sorted(rolls, reverse=True)[: expr.keep_n]
    elif expr.keep_type == "kl":
        kept = sorted(rolls)[: expr.keep_n]
    else:
        kept = rolls[:]

    total = sum(kept) + expr.mod
    return rolls, kept, total


def main() -> int:
    raw = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "1d20"
    try:
        expr, seed, normalized = parse(raw)
        if seed is not None:
            random.seed(seed)
        rolls, kept, total = run(expr)
    except ValueError as err:
        print(f"Error: {err}")
        return 2

    mod_text = f"{expr.mod:+d}" if expr.mod else "0"
    print(f"Expression: {normalized}")
    print(f"Rolls: {rolls}")
    print(f"Kept: {kept}")
    print(f"Modifier: {mod_text}")
    print(f"Total: {total}")
    if seed is not None:
        print(f"Seed: {seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
