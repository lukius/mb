all: ejs_l3.pdf

%.pdf: %.tex
	pdflatex $<
	pdflatex $<

clean:
	rm -f *.dvi *.aux *.log *.pdf
