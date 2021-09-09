########################################################################

# markdown extension list
MDEXT=\
all_symbols_escapable\
intraword_underscores\
escaped_line_breaks\
space_in_atx_header\
lists_without_preceding_blankline\
inline_code_attributes\
strikeout\
yaml_metadata_block\
pipe_tables\
line_blocks\
implicit_figures\
abbreviations\
inline_notes
MDEL=$(shell echo "$(MDEXT)" | tr " " "+")

# user source files
MDPY=$(shell find md/ -name "*.md")

# make dependencies
MK=$(patsubst md/%.md,build/%.md.mk,$(MDPY))

# preprocessed Markdown text
MD=$(patsubst md/%.md,build/%.md,$(MDPY))

# html linked Markdown text
MDHTML=$(patsubst md/%.md,build/%.html.md,$(MDPY))

# pdf linked Markdown text
MDPDF=$(patsubst md/%.md,build/%.pdf.md,$(MDPY))

# rendered html
HTML=$(patsubst build/%.md,html/%.html,$(MD))

# rendered pdf
PDF=$(patsubst build/%.md,pdf/%.pdf,$(MD))

########################################################################

.PHONY: help
help:
	#
	# marky HELP
	############
	#
	# TARGETS
	#
	# Tools:
	#  * help      - show this message
	#  * tree      - show the project tree
	#  * cheat     - show the marky *Cheat Sheet*
	#  * httpd     - run python -m httpd.server in `html/`
	#  * scan      - build make dependencies and targets
	#
	# Build:
	#  * all       - alias: `make all-html all-pdf`
	#  * all-html  - render html (`build/*.html.md`->`html/*.html`)
	#  * all-pdf   - render pdf (`build/*.pdf.md`->`pdf/*.pdf`)
	#  * clean     - delete: `build/*`, `html/*`, `pdf/*`
	#
	# Debug:
	#  * all-mk    - depend: `md/*.md`->`build/*.md.mk`
	#  * all-md    - marky: `md/*.md`->`build/*.md`
	#  * all-link  - link (`build/*.md`->`build/*.html.md/pdf`)
	#
	# Dependencies:
	#  * pandoc >= 2.10
	#  * pip install pandoc-fignos
	#  * pip install pandoc-eqnos
	#  * pip install pandoc-secnos
	#  * pip install pandoc-tablenos
	#  * pip install pandoc-xnos
	#  * pip install pyyaml
	#
	# ATTENTION
	#  files in `build/*.md` and `html/*.html` are auto-generated.
	#  user files `*.md(i)` have to be placed in `md/*.md(i)`.
	#  `make clean` deletes all files in `build/`, `html/` and `pdf/`.
	#
	# EXAMPLE
	#  1. run `make all-html httpd`:
	#     * transform `md/*.md`->`html/*.html`
	#     * start a python httpd server in `html`
	#  2. run `make all-pdf`
	#     * transform `md/*.md`->`pdf/*.pdf`
	#

.PHONY: tree
tree:
	# PROJECT TREE
	##############
	#
	# working_dir
	# |
	# |- marky.py            - marky executable
	# |- Makefile        (*) - marky Makefile
	# |
	# |- md/             (*) - user Markdown dir
	# |  |- marky.md(i)  (*) - marky documentation text
	# |  |- *.md             - user Markdown text files
	# |  |- *.mdi            - user Markdown include files
	# |
	# |- data/           (*) - pandoc resource directory
	# |  |- marky.bib    (*) - marky documentation bib
	# |  |- *.bib            - user bibliography files
	# |  |- *.png/jpg        - user image files
	# |  |- ...                etc...
	# |
	# |- build/          (*) - build Markdown dir
	# |  |- *.md         (*) - preprocessed Markdown text
	# |  |- *.md.mk      (*) - Makefile dependencies
	# |  |- *.html.md    (*) - linked Markdown for html format
	# |  |- *.pdf.md     (*) - linked Markdown for pdf format
	# |
	# |- html/           (*) - rendered html dir
	# |- pdf/            (*) - rendered pdf dir
	#
	# (*) directories/files are auto-generated using
	#    `./marky.py --init` and `make all´
	#

.PHONY: cheat
cheat: cheat-head cheat-block cheat-format cheat-inline cheat-meta cheat-include cheat-link cheat-code

.PHONY: cheat-block
cheat-head:
	#
	# marky CHEAT SHEET
	###################

.PHONY: cheat-block
cheat-block:
	#
	# CODE-BLOCK
	#
	#  ```!
	#  print("The code is shown in the document,")
	#  print("but printed text is shown in console.")
	#  _("This text is inserted into Markdown", _)
	#  _(_, "output and appended to prev line.")
	#  _(1, 2, 3, [4, 5,], "a", "b", sep=", ")
	#  __("""
	#     * This is cropped and shifted.
	#     * This is cropped and shifted.
	#     * This is cropped and shifted.
	#  """, crop=True, shift=)
	#  ```
	#
	#  ```!!
	#  print("The code is hidden in the document,")
	#  print("but printed text is shown in console.")
	#  import sys
	#  sys.path.append(".")
	#  import mymodule
	#  new_vars = {"a": 1, "b": 2}
	#  globals().update(new_vars)
	#  ```
	#

.PHONY: cheat-inline
cheat-inline:
	#
	# INLINE-EXPRESSION
	#
	#  This is a Paragraph with an `!<expression>`.
	#  This `\!<expression>` is not parsed.
	#
	#  The alphabet: `![chr(ord("A")+i for i in range(7)]`.
	#  The alphabet: ['A', 'B', 'C', 'D', 'E', 'F', 'G'].
	#
	#  A nice list: `!", ".join(list(range(1, 11)))`.
	#  A nice list: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
	#

.PHONY: cheat-format
cheat-format:
	#
	# FORMATTED OUTPUT
	#
	#  ```!!
	#  value = float(1.2345)
	#  ```
	#  The number `!value` is not formatted.
	#  The number 1.2345 is not formatted.
	#
	#  The number `!value:.2f` is formatted.
	#  The number 1.23 is formatted.
	#
	#  This `\!<variable>` is not parsed.
	#

.PHONY: cheat-include
cheat-include:
	#
	# INCLUDE-STATEMENT
	#
	#  !!! path/incl.mdi FLAGS
	#  \!!! This is not parsed as include statement.
	#
	# Flags:
	#  * aux      only Makefile dependency, no include
	#  * nodep    include without Makefile dependency
	#  * raw      do not parse file, include as-is
	#  * nometa   ignore and skip all meta data
	#  * nobody   ignore and skip Markdown body
	#  * nomarky  no processing of marky markup
	#  * !        include only code blocks
	#  * !!       include only hidden code blocks
	#  * #+N      increase level of ATX headings by N
	#  * >>N      increase indentation level by N tabs
	#  * >N       increase indentation level by N spaces
	#

.PHONY: cheat-meta
cheat-meta:
	#
	# META DATA
	#
	#  ---
	#  title: Document
	#  date: Today
	#  author: Name
	#  link-citations: true
	#  bibliography: bibl.bib
	#  fontsize--pdf: 11pt
	#  fontsize--html: 10pt
	#  header-includes--pdf: >
	#     \usepackage{...}
	#     \usepackage{...}
	#  header-includes--html: >
	#     <script ...>
	#     <link ...>
	#     <style ...>
	#  xnos-cleveref: true
	#  xnos-capitalise: true
	#  -hidden_field: text
	#  ---
	#

.PHONY: cheat-link
cheat-link:
	#
	# FORMAT LINK
	#
	#  [Link to Document](path/to/file.html)
	#  [Link to Document](path/to/file.pdf)
	#  [Format Link to Document](path/to/file.???)
	#  This is not parsed as format link .\???
	#

.PHONY: cheat-code
cheat-code:
	#
	# FORMAT CODE
	#
	#   ```!
	#   def test1_html():
	#       _("This is HTML1!")
	#   def test1_pdf():
	#       return "This is \{PDF1\}!"
	#   def test2_html():
	#       __("""
	#           This is HTML2!
	#           This is HTML2!
	#           This is HTML2!
	#       """)
	#   def test2_pdf():
	#       return """
	#           This is \{PDF2\}!
	#           This is \{PDF2\}!
	#           This is \{PDF2\}!
	#       """
	#   ```
	#   Run Format Code `?test1()` and `?test2()`.
	#   `\?test1()` and `\?test2()` are not parsed.
	#

########################################################################

.PHONY: all
all: $(HTML) $(PDF)

.PHONY: all-mk
all-mk: $(MK)

.PHONY: all-md
all-md: $(MD)

.PHONY: all-link
all-link: $(MDHTML) $(MDPDF)

.PHONY: all-html
all-html: $(HTML)

.PHONY: all-pdf
all-pdf: $(PDF)

.PHONY: clean
clean:
	rm -rf ./build/* ./html/* ./pdf/*

.PHONY: httpd
httpd:
	cd html && python -m http.server

.PHONY: scan
scan: all-mk

########################################################################

build/%.md.mk: md/%.md
	mkdir -p $(shell dirname "$@")
	./marky.py --mkdep --marky="$<"

build/%.md: build/%.md.mk
	mkdir -p $(shell dirname "$@")
	./marky.py --md="$@"

build/%.html.md: build/%.md
	mkdir -p $(shell dirname "$@")
	./marky.py --link html --md="$<"

build/%.pdf.md: build/%.md
	mkdir -p $(shell dirname "$@")
	./marky.py --link pdf --md="$<"

html/%.html: build/%.html.md
	ln -snf ../data build/data
	mkdir -p $(shell dirname "$@")
	ln -snf ../data html/data
	pandoc "$<" --filter pandoc-xnos --citeproc --from=markdown+raw_html+$(MDEL) --to=html5 --output="$@" --resource-path="./build/" --self-contained --table-of-contents --number-sections --columns=1

pdf/%.pdf: build/%.pdf.md
	mkdir -p $(shell dirname "$@")
	ln -snf ../data build/data
	ln -snf ../data pdf/data
	pandoc "$<" --filter pandoc-xnos --citeproc --from=markdown+raw_tex+$(MDEL) --to=latex --output="$@" --resource-path="./build/" --table-of-contents --number-sections --columns=1 --pdf-engine=xelatex

########################################################################

PSEUDO=help tree cheat clean httpd scan

INCFLAG=0

define LOOPBODY
  ifeq ($$(filter $$(PSEUDO),$$(G)),)
    INCFLAG=1
  endif
endef

ifneq ($(MAKECMDGOALS),)
  $(foreach G,$(MAKECMDGOALS),$(eval $(LOOPBODY)))
endif

ifeq ($(INCFLAG),1)
  -include $(MK)
endif

########################################################################
