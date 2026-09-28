# 中文课程论文 LaTeX 模板

本模板用于“高级 Web 开发”课程论文，满足当前作业的核心要求：中文、5000 字以上、单栏、不设置摘要和关键词，并预留 Track 综述、代表论文介绍及 AI 使用说明。

## 开始写作

1. 在 `config/metadata.tex` 中填写题目、姓名、学号、学院、班级和教师信息。
2. 按顺序填写 `chapters/` 中的正文文件。
3. 在 `references.bib` 中维护参考文献，并用 `\parencite{文献键}` 引用。
4. 图片放进 `figures/`，通过 `\includegraphics` 插入。
5. 提交前把 `config/metadata.tex` 中的 `\draftmodetrue` 改成 `\draftmodefalse`，隐藏蓝色写作提示。
6. 根据实际使用情况更新“人工智能工具使用说明”。

模板有意省略摘要和关键词，不要自行添加，除非教师后续修改要求。

## 编译 PDF

在项目根目录执行：

```bash
make
```

生成文件为 `main.pdf`。也可以直接执行：

```bash
latexmk -xelatex main.tex
```

`latexmk` 会自动按正确顺序运行 XeLaTeX 和 Biber；不要只运行一次 `xelatex`，否则目录、交叉引用和参考文献可能不完整。

持续监听文件变化并自动编译：

```bash
make watch
```

清理中间文件：

```bash
make clean
```

## 估算正文长度

```bash
make count
```

统计脚本会跟随 `\input` 读取各章，并近似统计中文汉字。它只用于写作过程自查，最终字数认定以课程要求和教师采用的方法为准。

## 常用写法

引用文献：

```latex
已有研究提出了检索增强生成框架\parencite{lewis2020rag}。
```

插入图片：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{example.pdf}
  \caption{图片标题}
  \label{fig:example}
\end{figure}
```

正文引用图片时写 `图~\ref{fig:example}`。图片文件建议使用 PDF、PNG 或 JPG；截图应保证文字清晰，并在标题或正文中注明来源。

## 目录结构

```text
.
├── main.tex                 # 论文入口
├── config/
│   ├── metadata.tex        # 论文基本信息与 AI 声明
│   └── preamble.tex        # 字体、版式和宏包配置
├── chapters/               # 正文章节
├── figures/                # 图片目录
├── references.bib          # 参考文献数据库
├── latexmkrc               # 自动编译配置
├── Makefile                # 常用命令
└── scripts/                # 辅助脚本
```

字体配置使用服务器已有的 Noto Serif/Sans CJK SC，因此不依赖 Windows 的宋体或黑体。英文正文使用 TeX Gyre Termes，它是适合论文排版的 Times 风格字体。
