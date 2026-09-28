#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_file="$(mktemp)"
plain_file="$(mktemp)"
trap 'rm -f "$source_file" "$plain_file"' EXIT

cd "$project_dir"

# 只统计六个正文章节，并排除模板的写作提示、占位行和草稿图。
awk '
  /\\ifdraftmode/ { in_draft = 1; next }
  in_draft && /\\fi/ { in_draft = 0; next }
  in_draft { next }
  /\\writingguide|\\placeholder/ { next }
  { print }
' chapters/0[1-6]-*.tex > "$source_file"

detex -l -e table,figure,equation,align,lstlisting,thebibliography "$source_file" > "$plain_file"

chinese_chars="$(grep -oP '\p{Han}' "$plain_file" | wc -l || true)"
latin_words="$(grep -oE "[[:alpha:]][[:alpha:]'-]*" "$plain_file" | wc -l || true)"

echo "中文汉字数（近似，不含图表、公式和参考文献）：$chinese_chars"
echo "拉丁文字词数（近似）：$latin_words"
echo "课程要求为 5000 字以上，建议正文汉字数保留一定余量。"
