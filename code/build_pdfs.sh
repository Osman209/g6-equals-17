#!/bin/sh
# Rebuild docs/papers/*.pdf from papers/*.md.  Needs pandoc and pdflatex.
# The papers are written for GitHub's KaTeX; the same source compiles under
# LaTeX because \lbrace, \rbrace and \cr are valid in both.  Run
# code/check_github_math.js first: a span whose closing $ is preceded by a
# space renders fine on GitHub and is invisible to pandoc.
set -e
cd "$(dirname "$0")/.."
mkdir -p docs/papers
for f in papers/*.md; do
  b=$(basename "$f" .md)
  pandoc "$f" -o "docs/papers/$b.pdf" --pdf-engine=pdflatex -H code/pdf_header.tex \
    -V fontsize=11pt -V colorlinks=true -V linkcolor=blue -V urlcolor=blue
  echo "docs/papers/$b.pdf"
done
