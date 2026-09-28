.PHONY: all watch count clean distclean

all: main.pdf

main.pdf: main.tex config/preamble.tex config/metadata.tex references.bib $(wildcard chapters/*.tex)
	latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex

watch:
	latexmk -xelatex -pvc -interaction=nonstopmode -file-line-error main.tex

count:
	./scripts/count-characters.sh

clean:
	latexmk -c main.tex

distclean:
	latexmk -C main.tex
