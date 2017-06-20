all: ejs_l6.pdf

%.pdf: %.tex
	pdflatex $<
	pdflatex $<

clean:
	rm -f *.dvi *.aux *.log *.pdf
