#!/usr/bin/env python3
"""Batch mobile-format updates for poker book chapters."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "chapters"

BOARD_KEYWORDS = ("rainbow", "two-tone", "monotone")


def is_board(content: str) -> bool:
    c = content.strip()
    if any(k in c for k in BOARD_KEYWORDS):
        return True
    if re.match(r"^[2-9TJQKA][shdc]$", c):
        return True
    parts = c.split()
    if len(parts) >= 3 and all(re.match(r"^[2-9TJQKA][shdc]$", p) for p in parts):
        return True
    if re.match(r"^[2-9TJQKA](\s+[2-9TJQKA]){2,}(\s|$)", c):
        return True
    clean = re.sub(r"\s", "", c)
    if re.match(r"^[2-9TJQKA]{3,}$", clean) and not re.match(
        r"^[2-9TJQKA]{2}[os]$", clean
    ):
        return True
    if re.match(r"^[2-9TJQKA]{3}\s", c):
        return True
    return False


def convert_texttt(text: str) -> str:
    text = text.replace("\\texttt{", "\\hand{")

    def repl(m):
        cmd = "\\board" if is_board(m.group(1)) else "\\hand"
        return f"{cmd}{{{m.group(1)}}}"

    return re.sub(r"\\hand\{([^}]+)\}", repl, text)


def convert_core_frameworks(text: str, chapter: str) -> str:
    frameworks = {
        "chapter01_excellent_player": [
            (
                "优秀牌手成长公式",
                "优秀牌手成长公式：稳定状态 $\\times$ 正确框架 $\\times$ 持续复盘 $\\times$ 长期执行",
            ),
            (
                "优秀牌手成长公式",
                "稳定状态 $\\times$ 正确框架 $\\times$ 持续复盘 $\\times$ 长期执行",
            ),
        ],
        "chapter02_preflop": [
            (
                "翻前四问",
                "我在什么位置？\\\\前面发生了什么行动？\\\\我的牌是否属于这个位置的可入池范围？\\\\我应该主动加注、3-bet、跟注，还是弃牌？",
            ),
        ],
        "chapter03_flop": [
            (
                "翻牌圈五步思考",
                "看牌面结构。\\\\判断谁有范围优势。\\\\判断自己的牌力类别。\\\\明确下注或过牌目的。\\\\提前规划转牌。",
            ),
        ],
        "chapter04_turn": [
            (
                "转牌三类出张",
                "强化我范围的牌：可以继续进攻。\\\\强化对手范围的牌：需要谨慎。\\\\空白牌：延续翻牌逻辑，但重新评估下注目的。",
            ),
        ],
        "chapter05_river": [
            (
                "河牌决策三问",
                "我有摊牌价值吗？\\\\我下注是价值还是诈唬？\\\\面对下注，我的牌能击败对手足够多的范围吗？",
            ),
        ],
        "chapter07_purpose_of_betting": [
            (
                "下注前必问",
                "如果我是价值下注，哪些更差牌会跟？\\\\如果我是诈唬，哪些更好牌会弃？\\\\如果两个问题都回答不了，就不要轻易下注。",
            ),
        ],
        "chapter08_aggressive_game": [
            (
                "有效激进三条件",
                "我的范围有优势。\\\\我的牌有合适的功能。\\\\对手有足够多可以弃掉的牌。",
            ),
        ],
        "chapter09_outs_equity_odds": [
            (
                "继续决策四步法",
                "先数 outs。\\\\再估胜率。\\\\计算跟注所需胜率。\\\\比较实际胜率与所需胜率。",
            ),
        ],
        "chapter10_fold_and_call": [
            (
                "跟注四问",
                "我需要多少胜率？\\\\对手有哪些价值牌？\\\\对手有哪些诈唬牌？\\\\我的牌能否击败足够多的下注范围？",
            ),
        ],
    }
    for title, inner in frameworks.get(chapter, []):
        # Match center block with optional line breaks in inner
        inner_pattern = inner.replace("\\\\", r"\\\\\s*\n?\s*")
        pattern = (
            r"\\begin\{center\}\s*\\textbf\{"
            + inner_pattern
            + r"\}\s*\\end\{center\}"
        )
        lines = inner.split("\\\\")
        body = " \\\\\n".join(lines)
        replacement = "\\begin{keybox}{" + title + "}\n" + body + "\n\\end{keybox}"
        text = re.sub(pattern, lambda _m, r=replacement: r, text)
    return text


def convert_tabular_3col(text: str) -> str:
    pattern = (
        r"\\begin\{center\}\s*\\begin\{tabular\}\{lll\}\s*"
        r"(\\toprule.*?\\bottomrule)\s*"
        r"\\end\{tabular\}\s*\\end\{center\}"
    )

    def repl(m):
        body = m.group(1)
        return (
            "\\begin{center}\n"
            "\\begin{tabularx}{\\textwidth}"
            "{>{\\raggedright\\arraybackslash}p{0.24\\textwidth}XX}\n"
            f"{body}\n"
            "\\end{tabularx}\n"
            "\\end{center}"
        )

    return re.sub(pattern, repl, text, flags=re.DOTALL)


def convert_tabular_4col(text: str) -> str:
    pattern = (
        r"\\begin\{center\}\s*\\begin\{tabular\}\{llll\}\s*"
        r"(\\toprule.*?\\bottomrule)\s*"
        r"\\end\{tabular\}\s*\\end\{center\}"
    )

    def repl(m):
        body = m.group(1)
        return (
            "\\begin{center}\n"
            "\\small\n"
            "\\begin{tabularx}{\\textwidth}"
            "{>{\\raggedright\\arraybackslash}p{0.22\\textwidth}"
            ">{\\raggedright\\arraybackslash}X"
            ">{\\raggedright\\arraybackslash}X"
            ">{\\raggedright\\arraybackslash}p{0.18\\textwidth}}\n"
            f"{body}\n"
            "\\end{tabularx}\n"
            "\\end{center}"
        )

    return re.sub(pattern, repl, text, flags=re.DOTALL)


def convert_tabular_2col(text: str) -> str:
    pattern = (
        r"\\begin\{center\}\s*\\begin\{tabular\}\{ll\}\s*"
        r"(\\toprule.*?\\bottomrule)\s*"
        r"\\end\{tabular\}\s*\\end\{center\}"
    )

    def repl(m):
        body = m.group(1)
        return (
            "\\begin{center}\n"
            "\\begin{tabularx}{\\textwidth}"
            "{>{\\raggedright\\arraybackslash}p{0.38\\textwidth}X}\n"
            f"{body}\n"
            "\\end{tabularx}\n"
            "\\end{center}"
        )

    return re.sub(pattern, repl, text, flags=re.DOTALL)


def wrap_hand_strength_table(text: str) -> str:
    pattern = (
        r"(\\begin\{center\}\s*\\begin\{tabularx\}\{\\textwidth\}"
        r"\{>\{\\raggedright\\arraybackslash\}p\{0\.24\\textwidth\}XX\}\s*"
        r"\\toprule\s*\\textbf\{牌力类型\}.*?\\bottomrule\s*"
        r"\\end\{tabularx\}\s*\\end\{center\})"
    )

    def repl(m):
        block = m.group(1)
        return f"\\begin{{keybox}}{{牌力功能表}}\n{block}\n\\end{{keybox}}"

    return re.sub(pattern, repl, text, flags=re.DOTALL)


def convert_action_boxes(text: str) -> str:
    pattern = (
        r"\\subsubsection\*\{推荐行动\}\s*\n\n(.*?)\n\n"
        r"\\subsubsection\*\{本手牌教训\}\s*\n\n(.*?)"
        r"(?=\n\\subsubsection|\n\\section|\n\\subsection|\n\\begin|\Z)"
    )

    def repl(m):
        action = m.group(1).strip()
        lesson = m.group(2).strip()
        return (
            f"\\begin{{keybox}}{{推荐行动}}\n{action}\n\\end{{keybox}}\n\n"
            f"\\begin{{summarybox}}{{本手牌教训}}\n{lesson}\n\\end{{summarybox}}\n"
        )

    return re.sub(pattern, repl, text, flags=re.DOTALL)


def add_ch09_formula_keybox(text: str) -> str:
    old = (
        "计算公式是：\n\n"
        "\\[\n"
        "\\text{所需胜率} = "
        "\\frac{\\text{跟注金额}}{\\text{跟注后总底池}}\n"
        "\\]"
    )
    new = (
        "\\begin{keybox}{底池赔率公式}\n"
        "\\[\n"
        "\\text{所需胜率} = "
        "\\frac{\\text{跟注金额}}{\\text{跟注后总底池}}\n"
        "\\]\n"
        "\\end{keybox}"
    )
    if old in text and "keybox{底池赔率公式}" not in text:
        text = text.replace(old, new, 1)
    return text


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    chapter = path.stem

    text = convert_texttt(text)
    text = convert_core_frameworks(text, chapter)
    text = convert_tabular_3col(text)
    text = convert_tabular_4col(text)
    text = convert_tabular_2col(text)

    if chapter == "chapter06_hand_strength_framework":
        text = wrap_hand_strength_table(text)

    if chapter == "chapter09_outs_equity_odds":
        text = add_ch09_formula_keybox(text)

    text = convert_action_boxes(text)

    path.write_text(text, encoding="utf-8")
    print(f"Updated: {path.name}")


if __name__ == "__main__":
    for tex in sorted(ROOT.glob("chapter*.tex")):
        process_file(tex)
