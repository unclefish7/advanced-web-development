# 搜索与检索增强人工智能汇报

配套现有中文论文，内容包括研究综述与 CFVBench 案例分析。默认按 10–12 分钟设计：15 页正文、1 页参考资料附录，16:9 宽屏。

- `搜索与检索增强人工智能汇报.pptx`：可用 PowerPoint、WPS 或 LibreOffice 编辑；文字、流程图、条形图均为可编辑对象。每页含演讲备注。
- `逐页讲稿.md`：讲解内容、建议时间及常见问答。
- `build_presentation.py`：仅依赖 Python 标准库的生成脚本。
- `validate_presentation.py`：检查 ZIP/XML、内部引用、页数、备注及对象边界。

## 修改与生成

可直接编辑 PPTX；也可修改生成脚本，然后在仓库根目录执行：

```sh
python presentation/build_presentation.py
python presentation/validate_presentation.py
```

重新运行会覆盖生成的 PPTX 和 Markdown 讲稿；直接在 PPTX 中做过的修改不会自动回写到脚本。

字体使用 `Noto Sans CJK SC`。字体未嵌入 PPTX；换电脑前请先检查中文字体替换和换行。按用户要求，不导出 PDF。

实验数据来自 CFVBench 原文表 2–4；没有重新运行实验。软件导出案例为自编教学示例，不是数据集原题。参考资料与 AI 使用说明位于最后一页，完整文献见配套论文。
