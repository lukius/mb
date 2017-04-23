all: ejs_l2.pdf

%.pdf: %.tex
	pdflatex $<
	pdflatex $<

clean:
	rm -f *.dvi *.aux *.log *.pdf
