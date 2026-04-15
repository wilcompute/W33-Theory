# Makefile for W(3,3) Theory Paper
# Usage: make        -> build PDF
#        make clean  -> remove auxiliary files
#        make arxiv  -> create arXiv submission tarball

TEX    = W36_PAPER
FIGS   = figures/fig1_spectral_diagram.pdf \
          figures/fig2_predictions_timeline.pdf \
          figures/fig3_spectral_decomposition.pdf

.PHONY: all clean arxiv figures

all: $(TEX).pdf

## ── Figures: SVG → PDF ──────────────────────────────────────────────────
figures/%.pdf: figures/%.svg
	@echo "Converting $< → $@"
	@inkscape $< --export-filename=$@

figures: $(FIGS)

## ── PDF compilation ─────────────────────────────────────────────────────
$(TEX).pdf: $(TEX).tex $(FIGS)
	pdflatex -interaction=nonstopmode $(TEX).tex
	bibtex $(TEX) || true
	pdflatex -interaction=nonstopmode $(TEX).tex
	pdflatex -interaction=nonstopmode $(TEX).tex
	@echo "Build complete: $(TEX).pdf"

## ── arXiv tarball ───────────────────────────────────────────────────────
arxiv: $(TEX).pdf
	@echo "Creating arXiv submission tarball..."
	tar -czf W33_Theory_arXiv_submission.tar.gz \
		$(TEX).tex \
		figures/fig1_spectral_diagram.pdf \
		figures/fig2_predictions_timeline.pdf \
		figures/fig3_spectral_decomposition.pdf
	@echo "Tarball ready: W33_Theory_arXiv_submission.tar.gz"
	@echo "Submit at: https://arxiv.org/submit"

## ── Clean ───────────────────────────────────────────────────────────────
clean:
	rm -f $(TEX).aux $(TEX).bbl $(TEX).blg $(TEX).log \
	       $(TEX).out $(TEX).toc $(TEX).lof $(TEX).lot \
	       $(TEX).synctex.gz
	@echo "Auxiliary files removed."

distclean: clean
	rm -f $(TEX).pdf
