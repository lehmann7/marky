########################################################################

.PHONY: help
help:
	#
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
	# * make quiet [...]     - build with `./marky --quiet [...]`
	# * make list            - list all scanned files and targets
	#
	# marky BUILD ALL
	#################
	# * make rescan          -> `build/*.make`, overwrite all
	# * make scan            -> `build/*.make`, only new files
	# * make build           -> `build/*.{html,pdf}.md`
	# * make tex             -> `build/*.tex`
	# * make html            -> `html/*.html`
	# * make pdf             -> `pdf/*.pdf`
	# * make tex             -> `build/*.tex`
	# * make aux             -> run all aux commands
	# * make all             -> `html/*.html`, `pdf/*.pdf`
	#
	# marky BUILD FILE
	##################
	# * make scan/file       -> `build/file.make`, overwrite
	# * make build/file      -> `build/file.{html,pdf}.md,py`
	# * make tex/file        -> `build/file.tex`
	# * make html/file       -> `html/file.html`
	# * make pdf/file        -> `pdf/pdf.pdf`
	# * make aux/file        -> run aux commands for file
	# * make clean/file      -> clean, but keep `make,pdf,html,tex`
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
	# 3. run `make scan; make list`: list all targets
	# 4. run `make rescan`: clear all aux file make deps
	#

.PHONY: tree
tree:
	#
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

.PHONY: httpd
httpd:
	cd html && python -m http.server

.PHONY: scan
scan:
	./marky.py --scan

.PHONY: rescan
rescan:
	./marky.py --scan --force

all_quiet := $(filter quiet,$(MAKECMDGOALS))
.PHONY: quiet
quiet:
	# enable ./marky --quiet [...]

all_auxcmd := $(filter auxcmd,$(MAKECMDGOALS))
.PHONY: auxcmd
auxcmd:
	# enable ./marky --auxcmd [...]

########################################################################

marky_alias:=
-include build/*.make build/**/*.make

########################################################################

.PHONY: link
build: $(foreach i,$(marky_alias),build/$(i))

.PHONY: html
html: $(foreach i,$(marky_alias),html/$(i))

.PHONY: pdf
pdf: $(foreach i,$(marky_alias),pdf/$(i))

.PHONY: tex
tex: $(foreach i,$(marky_alias),tex/$(i))

.PHONY: aux
aux: $(foreach i,$(marky_alias),aux/$(i))

.PHONY: clean
clean:
	rm -rf ./build/* ./html/* ./pdf/*

.PHONY: all
all: html pdf

.PHONY: list
list:
	#
	# marky TARGETS
	###############
	# make scan/<ALIAS>  - create Makefile `build/<ALIAS>.make`
	# make build/<ALIAS> - build `build/<ALIAS>.{html,pdf}.md,py`
	# make tex/<ALIAS>   - build `build/<ALIAS>.tex`
	# make html/<ALIAS>  - build `html/<ALIAS>.html`
	# make pdf/<ALIAS>   - build `pdf/<ALIAS>.pdf`
	# make aux/<ALIAS>   - run aux commands for <ALIAS>
	# make clean/<ALIAS> - clean files, keep:`make,html,pdf,tex`
	#
	# <ALIAS>
	#########
	#$(marky_alias)
