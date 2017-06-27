PDFLATEX = TEXINPUTS=./packages/: pdflatex

all:
	$(PDFLATEX) slides_sde.tex
	bibtex slides_sde
	$(PDFLATEX) slides_sde.tex

clean:
	rm -rf *.toc *.aux *.nav *.pdf *.out *.snm *.log *.vrb *.bbl *.blg
