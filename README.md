# 告别凭感觉打牌：德州扑克新手系统入门课

本项目是一本德州扑克新手入门课程书稿的 LaTeX 工程骨架。当前版本用于搭建书稿结构、章节拆分、编译配置和占位内容，后续可在各章节文件中逐步扩展完整正文。

## 文件结构

```text
.
├── main.tex
├── preamble.tex
├── references.bib
├── chapters/
│   ├── chapter01_excellent_player.tex
│   ├── chapter02_preflop.tex
│   ├── chapter03_flop.tex
│   ├── chapter04_turn.tex
│   ├── chapter05_river.tex
│   ├── chapter06_hand_strength_framework.tex
│   ├── chapter07_purpose_of_betting.tex
│   ├── chapter08_aggressive_game.tex
│   └── chapter09_fold_and_call.tex
├── figures/
├── tables/
└── README.md
```

## 推荐编译方式

本项目使用 `ctexbook` 文档类，推荐使用 XeLaTeX 编译。由于参考文献使用 `biblatex` 和 `biber`，完整编译流程为：

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

如果使用 TeXstudio、VS Code LaTeX Workshop 或 Overleaf，请将主文件设置为 `main.tex`，编译引擎设置为 XeLaTeX，参考文献后端设置为 Biber。

## 如何新增章节

1. 在 `chapters/` 目录中新建章节文件，例如 `chapter10_review_system.tex`。
2. 在新文件中使用 `\chapter{章节标题}` 开始章节。
3. 在 `main.tex` 中按顺序加入：

```latex
\include{chapters/chapter10_review_system}
```

建议新章节继续沿用当前结构：

```latex
\section{本章导入}
\section{核心概念}
\section{新手常见误区}
\section{实战思考框架}
\section{牌例拆解}
\section{本章总结}
\section{课后训练}
```

## 如何插入图片和表格

图片建议放入 `figures/` 目录，在正文中使用：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{example-image}
  \caption{图片说明}
  \label{fig:example}
\end{figure}
```

表格可以直接写在章节文件中，也可以将较大的表格拆到 `tables/` 目录后用 `\input{}` 引入：

```latex
\begin{table}[htbp]
  \centering
  \caption{起手牌范围示例}
  \label{tab:preflop-range}
  \begin{tabular}{lll}
    \toprule
    位置 & 建议动作 & 示例手牌 \\
    \midrule
    BTN & Open raise & AA--22, AKs--A2s \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 后续写作建议

- 每章先补充核心概念，再补牌例，最后整理课后训练。
- 术语首次出现时建议使用“中文解释 + 英文术语”的形式，例如“起手牌范围（range）”。
- 避免用单手牌输赢评价策略，应强调决策质量、长期期望值（EV）和风险管理。
- 每个牌例建议固定记录位置、有效筹码、翻前行动、公共牌、下注尺度、对手类型和复盘结论。
- 后续可增加术语表、牌例索引、训练题答案和常见错误清单。
