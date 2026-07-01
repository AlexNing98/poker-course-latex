#!/usr/bin/env python3
"""Convert poker card notation to Unicode suit format: K♠ 9♠ 2♦"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "chapters"
RANK = r"[2-9TJQKA]"
SUITS = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}


def assign_rainbow_suits(ranks: list[str]) -> list[str]:
    """Assign distinct suits for rainbow-style abstract boards."""
    cycle = ["♠", "♣", "♦", "♥", "♠", "♣"]
    return [f"{r}{cycle[i % len(cycle)]}" for i, r in enumerate(ranks)]


def assign_two_tone(ranks: list[str]) -> list[str]:
    if len(ranks) < 2:
        return assign_rainbow_suits(ranks)
    out = [f"{ranks[0]}♠", f"{ranks[1]}♠"]
    for r in ranks[2:]:
        out.append(f"{r}♦")
    return out


def assign_monotone(ranks: list[str]) -> list[str]:
    return [f"{r}♠" for r in ranks]


def convert_suited_hand(two_rank: str) -> str:
    return f"{two_rank[0]}♠ {two_rank[1]}♠"


def convert_explicit_segment(seg: str) -> str:
    """Convert rank+letter suit sequences; preserve modifiers and punctuation."""
    seg = seg.strip()

    # Single rank only (outs / Broadway / bare turn rank): keep as-is
    if re.fullmatch(RANK, seg):
        return seg

    modifier = ""
    m = re.search(r"\s+(rainbow|two-tone|monotone)\s*$", seg, re.I)
    if m:
        modifier = " " + m.group(1).lower()
        seg = seg[: m.start()].strip()

    # Wildcard combos like AsXs, QsJs stay pattern-based
    if "X" in seg.upper() and re.search(r"[2-9TJQKA]X[shdc]", seg, re.I):
        seg = re.sub(
            rf"({RANK})X([shdc])",
            lambda m: f"{m.group(1).upper()}♠",
            seg,
            flags=re.I,
        )
        seg = re.sub(rf"({RANK})([shdc])", lambda m: m.group(1) + SUITS[m.group(2)], seg)
        return re.sub(r"\s+", " ", seg).strip() + modifier

    # Spaced explicit cards: As 7s, Ks 9s 2d
    if re.search(rf"{RANK}[shdc]", seg, re.I):
        tokens = re.findall(rf"{RANK}[shdc]|[^ \t]+", seg, re.I)
        cards = []
        rest = []
        for tok in tokens:
            if re.fullmatch(rf"{RANK}[shdc]", tok, re.I):
                cards.append(tok[0] + SUITS[tok[1].lower()])
            elif re.fullmatch(rf"({RANK}[shdc]){{2,}}", tok, re.I):
                i = 0
                while i < len(tok):
                    cards.append(tok[i] + SUITS[tok[i + 1].lower()])
                    i += 2
            else:
                rest.append(tok)
        if cards:
            spaced = " ".join(cards)
            if rest:
                return spaced + " " + " ".join(rest) + modifier
            return spaced + modifier

    # Concatenated: As7s2d, Qh7s2h
    if re.fullmatch(rf"({RANK}[shdc]){{2,}}", seg, re.I):
        cards = []
        i = 0
        while i < len(seg):
            cards.append(seg[i] + SUITS[seg[i + 1].lower()])
            i += 2
        return " ".join(cards) + modifier

    # Spaced ranks only: J T 9, A 7 2
    rank_tokens = re.findall(RANK, seg)
    if rank_tokens and re.fullmatch(rf"({RANK}\s*)+", seg):
        low = seg.lower()
        if "two-tone" in modifier:
            return " ".join(assign_two_tone(rank_tokens)) + modifier
        if "monotone" in modifier:
            return " ".join(assign_monotone(rank_tokens)) + modifier
        return " ".join(assign_rainbow_suits(rank_tokens)) + modifier

    # Compact rank board: A72, KQ7, 987
    if re.fullmatch(rf"{RANK}+", seg) and len(seg) >= 2:
        ranks = list(seg)
        low_mod = modifier.lower()
        if "two-tone" in low_mod:
            return " ".join(assign_two_tone(ranks)) + modifier
        if "monotone" in low_mod:
            return " ".join(assign_monotone(ranks)) + modifier
        return " ".join(assign_rainbow_suits(ranks)) + modifier

    # A72 rainbow attached
    m2 = re.fullmatch(rf"({RANK}+)\s*(rainbow|two-tone|monotone)", seg, re.I)
    if m2:
        ranks = list(m2.group(1))
        mod = " " + m2.group(2).lower()
        if "two-tone" in mod:
            return " ".join(assign_two_tone(ranks)) + mod
        if "monotone" in mod:
            return " ".join(assign_monotone(ranks)) + mod
        return " ".join(assign_rainbow_suits(ranks)) + mod

    # Single card with suit: 4h, As
    m3 = re.fullmatch(rf"{RANK}[shdc]", seg, re.I)
    if m3:
        return seg[0] + SUITS[seg[1].lower()]

    # Pocket pair: AA, KK, 77
    m_pp = re.fullmatch(rf"({RANK})\1", seg)
    if m_pp and len(seg) == 2:
        return f"{seg[0]}♠ {seg[0]}♦"

    # Offsuit: AKo, KQo - keep
    if re.fullmatch(rf"{RANK}{{2}}o", seg, re.I):
        return seg

    # Suited hand suffix: T9s, AQs, KJs, 98s
    if re.fullmatch(rf"{RANK}{{2}}s", seg, re.I):
        return convert_suited_hand(seg[:2])

    # Two rank shorthand: AK, KQ, QJ, JT, T9
    if re.fullmatch(rf"{RANK}{{2}}", seg):
        return seg

    # Fallback: convert any embedded rank+suit
    return re.sub(
        rf"({RANK})([shdc])",
        lambda m: m.group(1) + SUITS[m.group(2).lower()],
        seg,
        flags=re.I,
    )


def convert_content(content: str) -> str:
    # Preserve Chinese enumeration顿号 lists: As、7s、Ks
    if "、" in content:
        parts = content.split("、")
        return "、".join(convert_explicit_segment(p.strip()) for p in parts)

    return convert_explicit_segment(content.strip())


def add_street_card_suits(text: str) -> str:
    """Add default suit to bare turn/river cards in game examples."""
    return re.sub(
        r"(转牌为|河牌为) \\hand\{([2-9TJQKA])\}",
        r"\1 \\hand{\2♠}",
        text,
    )


def fix_wildcards(text: str) -> str:
    return text.replace("Xs", "X♠").replace("Xh", "X♥").replace("Xd", "X♦").replace("Xc", "X♣")


def process_text(text: str) -> str:
    def repl(m):
        body = convert_content(m.group(1))
        return f"\\hand{{{body}}}"

    text = re.sub(r"\\(?:hand|texttt)\{([^}]*)\}", repl, text)
    text = add_street_card_suits(text)
    text = fix_wildcards(text)
    return text


def process_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    updated = process_text(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"Updated: {path.name}")


if __name__ == "__main__":
    for tex in sorted(ROOT.glob("chapter*.tex")):
        process_file(tex)
