# 告别凭感觉打牌：德州扑克新手系统入门课

本项目是一本德州扑克新手入门课程的 LaTeX 书稿工程。全书共 10 章，从翻前到河牌完整覆盖单手牌处理流程，并进一步讲解牌力分类、下注目的、基础计算、激进策略与弃牌纪律，帮助读者建立可复盘的决策框架。

**在线仓库：** [github.com/AlexNing98/poker-course-latex](https://github.com/AlexNing98/poker-course-latex)

## 全书结构

| 章 | 文件 | 主题 | 核心框架 |
|---|------|------|----------|
| 1 | `chapter01_excellent_player.tex` | 如何成为优秀的牌手 | 状态管理、决策质量、复盘习惯 |
| 2 | `chapter02_preflop.tex` | 翻前 | 翻前四问 |
| 3 | `chapter03_flop.tex` | 翻牌 | 翻牌圈五步思考 |
| 4 | `chapter04_turn.tex` | 转牌 | 转牌三类出张 |
| 5 | `chapter05_river.tex` | 河牌 | 河牌决策三问 |
| 6 | `chapter06_hand_strength_framework.tex` | 不同牌力的处理框架 | 牌力功能表 |
| 7 | `chapter07_purpose_of_betting.tex` | 下注的目的 | 下注前必问 |
| 8 | `chapter08_aggressive_game.tex` | 激进的游戏 | 有效激进三条件 |
| 9 | `chapter09_outs_equity_odds.tex` | 基础计算：Outs、胜率与赔率 | 继续决策四步法 |
| 10 | `chapter10_fold_and_call.tex` | 弃牌与跟注 | 跟注四问 |

每章统一包含：本章导入、核心概念、新手常见误区、实战思考框架、牌例拆解、本章总结、课后训练。

## 文件结构

```text
.
├── main.tex              # 主文档（含完整前言）
├── preamble.tex          # 宏包、样式与写作命令
├── references.bib        # 参考文献
├── chapters/             # 十章正文
├── figures/              # 图片目录
├── tables/               # 表格目录
├── scripts/              # 辅助脚本（如牌面格式转换）
└── README.md
```

## 编译方式

本项目使用 `ctexbook` 文档类，推荐 **XeLaTeX + Biber** 编译。完整流程：

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

在 TeXstudio、VS Code LaTeX Workshop 或 Overleaf 中，请将主文件设为 `main.tex`，编译引擎设为 XeLaTeX，参考文献后端设为 Biber。

编译成功后生成 `main.pdf`（当前完整书稿约 178 页）。若 `main.pdf` 被阅读器占用导致无法覆盖，请先关闭 PDF 阅读器后重新编译。

## 手牌与牌面格式

全书手牌、公共牌统一使用 `\hand{}` 命令排版，花色采用 Unicode 符号，例如：

```latex
\hand{A♠ 7♠}          % 底牌
\hand{K♠ 9♠ 2♦}        % 翻牌
\hand{A♠ 7♣ 2♦ rainbow} % 带牌面描述
\hand{KQo}             % 抽象起手牌记法（无具体花色）
```

`preamble.tex` 中通过 `newunicodechar` 将 ♠♥♦♣ 映射到系统符号字体（优先 `Segoe UI Symbol`），确保 XeLaTeX 编译后 PDF 能正确显示花色：

```latex
\newcommand{\hand}[1]{{\normalfont #1}}
```

批量转换脚本见 `scripts/convert_cards.py`（将字母花色记法转为 Unicode 格式）。

## 如何新增章节

1. 在 `chapters/` 中新建文件，例如 `chapter11_review_system.tex`。
2. 以 `\chapter{章节标题}` 开始。
3. 在 `main.tex` 中按顺序加入：

```latex
\include{chapters/chapter11_review_system}
```

建议沿用现有章节结构（导入 → 核心概念 → 误区 → 框架 → 牌例 → 总结 → 训练）。

## 如何插入图片和表格

图片放入 `figures/`，正文引用：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example}
  \caption{图片说明}
  \label{fig:example}
\end{figure}
```

较大表格可放入 `tables/` 后用 `\input{}` 引入。项目已加载 `booktabs`，推荐使用 `\toprule`、`\midrule`、`\bottomrule`。

## 写作与排版约定

- 术语首次出现建议使用 `\term{中文}{英文}` 或「中文解释 + 英文术语」，例如「起手牌范围（range）」。
- 手牌与公共牌使用 `\hand{}`，花色写作 ♠ ♥ ♦ ♣，多张牌之间用空格分隔。
- 数学公式使用 `\[...\]` 或 `$...$`；百分号写作 `\%`。
- `center` 环境内换行使用 `\\`。
- 牌例建议记录：位置、有效筹码、翻前行动、公共牌、下注尺度、对手类型与复盘结论。
- 强调决策质量与长期 EV，避免用单手牌输赢评价策略。

## 后续可扩展内容

- 术语表与牌例索引
- 课后训练参考答案
- 常见错误清单速查
- 附录：位置图、起手牌范围参考表
