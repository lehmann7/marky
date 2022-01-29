########################################################################

.PHONY: help
help:
	# marky DEPENDENCIES
	####################
	# * pandoc >= 2.10
	# * pip install pandoc-fignos
	# * pip install pandoc-eqnos
	# * pip install pandoc-secnos
	# * pip install pandoc-tablenos
	# * pip install pandoc-xnos
	# * pip install pyyaml
	#
	# ATTENTION
	###########
	# All files in `build/*.md` and `html/*.html` are auto-generated!
	# User files `*.md` have to be placed in `md/*.md`!
	# `make clean` deletes all files in `build/`, `html/` and `pdf/`.
	#
	# marky UTILS
	#############
	# * make help            - show this *Help Message*
	# * make tree            - show the *Project Tree*
	# * make httpd           - run python -m httpd.server in `html/`
	# * make clean           - delete: `build/*`, `html/*`, `pdf/*`
	# * make scan            - build make deps: `build/*.make`
	# * make list            - list all scanned files and targets
	#
	# marky BUILD ALL
	#################
	# * make build           -> `build/*.{html,pdf}.md`
	# * make tex             -> `build/*.tex`
	# * make html            -> `html/*.html`
	# * make pdf             -> `pdf/*.pdf`
	# * make all             -> `html/*.html`, `pdf/*.pdf`
	#
	# marky BUILD FILE
	##################
	# * make build/file      -> `build/file.{html,pdf}.md`
	# * make build/file.tex  -> `build/file.tex`
	# * make html/file       -> `html/file.html`
	# * make pdf/file        -> `pdf/pdf.html`
	#
	# EXAMPLE
	#########
	# 1. run `make scan; make html/file.html httpd`:
	#    * generate `build/file.make`
	#    * transform `md/file.md` -> `html/file.html`
	#    * start a python httpd server in `html`
	# 2. run `make scan; make pdf/file.pdf`
	#    * generate `build/file.make`
	#    * transform `md/file.md` -> `pdf/file.pdf`
	#

.PHONY: tree
tree:
	# PROJECT TREE
	##############
	# <working_dir>
	# |- marky.py            - marky executable
	# |- Makefile        (*) - marky Makefile
	# |- pandoc-run      (*) - pandoc wrapper
	# |- md/             (*) - user Markdown dir
	# |  |- *.md             - user Markdown text
	# |- data/           (*) - user data dir
	# |  |- *.*                user data files
	# |- build/          (*) - build Markdown dir
	# |  |- *.py         (*) - marky Python code
	# |  |- *.make       (*) - Makefile rules
	# |  |- *.html.md    (*) - Markdown for html format
	# |  |- *.pdf.md     (*) - Markdown for pdf format
	# |- html/*.html     (*) - rendered html dir
	# |- pdf/*.pdf       (*) - rendered pdf dir
	#
	# (*) directories/files are auto-generated using
	#    `./marky.py --init; make scan; make all´
	#

.PHONY: clean
clean:
	rm -rf ./build/* ./html/* ./pdf/*

.PHONY: httpd
httpd:
	cd html && python -m http.server

.PHONY: scan
scan:
	./marky.py --scan

########################################################################

all_md:=
all_build:=
all_html:=
all_pdf:=
all_tex:=

-include build/*.make build/**/*.make

########################################################################

.PHONY: link
build: $(all_build)

.PHONY: html
html: $(all_html)

.PHONY: pdf
pdf: $(all_pdf)

.PHONY: tex
tex: $(all_tex)

.PHONY: all
all: html pdf

.PHONY: list
list:
	# marky TARGETS
	###############
	# * `make scan` -- FILES:$(all_md)
	# * `make build` -- `make$(all_build)`
	# * `make html` -- `make$(all_html)`
	# * `make pdf` -- `make$(all_pdf)`
	# * `make tex` -- `make$(all_tex)`
	#
