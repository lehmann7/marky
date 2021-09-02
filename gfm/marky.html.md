---
author: Henry Lehmann
bibliography: marky.bib
date: 1. August 2021
fontsize: 11pt
header-includes: '<style>* { box-sizing: border-box; }</style>

  '
included: 1
link-citations: true
title: marky Documentation
xnos-capitalise: true
xnos-cleveref: true

---

---

> **Abstract** -- `marky` is a preprocessor for Markdown using Python.
> `marky` is inspired by [pandoc](https://www.pandoc.org/),
> [RMarkdown](https://rmarkdown.rstudio.com/), [Quarto](https://quarto.org/).
> This document is created using `marky` (Version 0.1) and
> contains examples which illustrate the generation of
> document content for `html` and `pdf` and the dynamical adjustment
> of Markdown text during preprocessing based on `python` code.
> The full raw `marky` source code of this documentation appended at
> the end. The `marky` source code of this document can be read
> [here](markysource.html). For `marky` download please refer to the
> [`marky` repository](https://github.com/lehmann7/marky).

---

# Introduction

`marky` is a Markdown preprocessor which transforms a Markdown document
using python. `marky` implements new markup which controls the execution
of python code and the generation and manipulation of Markdown text.

`marky` only depends on `pandoc` and `pyyaml`. `pandoc` is used for rendering
the Markdown into `html` and `pdf`. `pandoc` supports various Markdown
extensions allowing for scientific writing using equations, figures,
tables, citations and corresponding referencing mechanism for the latter.
`pyyaml` is used for parsing meta data in the front matter of the
Markdown text if it is present.

Workflow for creating `html` or `pdf` using `marky`

1. user writes a Markdown text file and places it in `md/*.md`
directory with the extension `.md`. the Markdown text contains
special `marky` markup which executes python code and manipulates
the Markdown text.

2. `marky` transforms the files in `md/*.md` into regular Markdown text
and places the transformed files in `build/*.md`. The transformed text
only contains regular Markdown, and placeholders for format dependent
output for `html` and `pdf`.

3. before rendering `marky` replaces placeholders for format dependent
output with content creating a temporary file which only contains
regular Markdown text for `html` and `pdf` documents according to
`pandoc` Markdown specification.

4. the regular Markdown text in the files `build/*.md` is rendered into
`html` and `pdf` using `pandoc`.

The three steps are implemented in `marky.py` and a `Makefile`. The
following document describes the special `marky` markup and shows
how to use `marky.py` and the `Makefile`.

---

# Related Work {#sec:related}

For scientific reporting and writing usually typesetting systems or
complicted WYSIWYG editors are used. In order to simplify the writing
different approaches and frameworks have been developed.

* [`pandoc`](https://www.pandoc.org/),
* [RMarkdown](https://rmarkdown.rstudio.com/)
* [Quarto](https://quarto.org/)
* [Scientific Markdown](https://jaantollander.com/post/scientific-writing-with-markdown/)
* [Technical `pandoc`](https://lee-phillips.org/panflute-gnuplot/)

All of those approaches use `pandoc` as an underlying framework for document
conversion. `pandoc` is a powerful framework for conversion between different
document formats including `marky`, `html` and `pdf`. `pandoc` implements an
own internal AST, in which different document formats can be imported and
exported. Using this intermediate document representation, `pandoc` allows
to modify document using filters, which operate on the AST. Filters
can be written in [`haskell`](https://pandoc.org/filters.html),
[`lua`](https://pandoc.org/lua-filters.html) and
[`python`](https://pandoc.org/filters.html#but-i-dont-want-to-learn-haskell).

Where as RMarkdown and Quarto are integrated frameworks, which additionally
depend on `knitr`, `RStudio`, `Jupyter`, `marky` depends on `pandoc` and `pyyaml`
only. `marky` natively only supports executable python code blocks, however,
other languages can be executed using wrappers, which are available for
other languages.

---

# `marky` Features {#sec:features}

`marky` implements following features using an simple Markdown-style syntax.

1. read Markdown meta data from front matter,
see @sec:metadata
```md
	---
		<key>: <value>
	---
```

2. execute and hide/show python code blocks inside Markdown text,
see @sec:block
```md
	```!
		<python_code_shown>
	```

	```!!
		<python_code_hidden>
	```
```

3. generate Markdown text using python code, see @sec:mdprint
```md
	```!
		_("<markdown_text>")
		__("""
			<markdown_text>
			<markdown_text>
			<markdown_text>
		""")
	```
```

4. format output of python variables into Markdown text,
see @sec:format
```md
	Output into text: `!<python_variable>`
```

5. output the result of python expressions into Markdown text,
see @sec:inline
```md
	Output into text: `!<python_expression>`
```

6. include Markdown text, make dependencies and forward meta data,
see @sec:include and !@sec:incmeta.
```md
	!!! include_file.mdi
```

7. format links in `html` and `pdf` documents for
referencing external documents of the same format,
see @sec:formlink.
```md
	[Format Link to html/pdf document](path/to/file.???)
```

8. use format codes in order to inject format specific
code in `html` and `pdf` documents,
see @sec:formcode.
```md
	```!
		def code_html():
			_("<HTML_CODE>")
			return """
				<MORE_CODE>
				<MORE_CODE>
				<MORE_CODE>
			"""
		def code_pdf():
			__("""
				{TEX_CODE}
				{TEX_CODE}
				{TEX_CODE}
			""")
	```

	Format dependent output: `!code()`
```

---

# Scientific Writing in Markdown {#sec:panmd}

[Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown) is a markup
language for technical writing, with emphasis on readability. Markdown
can be rendered in many formats including `html` and `pdf` by using
[`pandoc`](https://pandoc.org/) for example.

Using various Markdown extensions of `pandoc` a sufficient structure for
writing scientific documents can be reflected using Markdown syntax.
`marky` uses the following `pandoc` Markdown extensions.
* parsing extensions
	* [all_symbols_escapable](https://pandoc.org/MANUAL.html#extension-all_symbols_escapable)
	* [intraword_underscores](https://pandoc.org/MANUAL.html#extension-intraword_underscores)
	* [escaped_line_breaks](https://pandoc.org/MANUAL.html#extension-escaped_line_breaks)
	* [space_in_atx_header](https://pandoc.org/MANUAL.html#extension-space_in_atx_header)
	* [lists_without_preceding_blankline](https://pandoc.org/MANUAL.html#extension-lists_without_preceding_blankline)
* styling extensions
	* [inline_code_attributes](https://pandoc.org/MANUAL.html#extension-inline_code_attributes)
	* [strikeout](https://pandoc.org/MANUAL.html#extension-strikeout)
* structuring extensions
	* [yaml_metadata_block](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block)
	* [pipe_tables](https://pandoc.org/MANUAL.html#extension-pipe_tables)
	* [line_blocks](https://pandoc.org/MANUAL.html#extension-line_blocks)
	* [implicit_figures](https://pandoc.org/MANUAL.html#extension-implicit_figures)
	* [abbreviations](https://pandoc.org/MANUAL.html#extension-abbreviations)
	* [inline_notes](https://pandoc.org/MANUAL.html#extension-inline_notes)
* code injection
	* [raw_html](https://pandoc.org/MANUAL.html#extension-raw_html)
	* [raw_tex](https://pandoc.org/MANUAL.html#extension-raw_tex)

`pandoc` supports
[equations](https://pandoc.org/MANUAL.html#extension-tex_math_dollars)
rendered inline and single-line in tex-style using `$...$` and `$$...$$`,
[bibliography](https://pandoc.org/MANUAL.html#citations)
using the `--citeproc` option,
[section numbering](https://pandoc.org/MANUAL.html#extension-header_attributes)
using the `--number-sections` option and
[table of contents](https://pandoc.org/MANUAL.html#option--toc)
using the `--table-of-contents` option.

`pandoc` supports [`xnos`](https://github.com/tomduck/pandoc-xnos) filters
for referencing document content like
[figures](https://github.com/tomduck/pandoc-fignos#usage),
[equations](https://github.com/tomduck/pandoc-eqnos#usage),
[tables](https://github.com/tomduck/pandoc-tablenos#usage),
[sections](https://github.com/tomduck/pandoc-secnos#usage)
by using the `--filter pandoc-xnos` option.
`xnos` integrates clever references, which means "Fig.", "Sec.", "Eq."
and "Tab." are added automatically to the corresponding element.
If the prefix is to be omitted, the reference can be written as
`!@ref:label`.

**Example**
```md
## Referenced Section {#sec:label}

This is a reference to @sec:label.

![This is the caption](data:image/png;base64,iVBORw0KGgoAAAANS
UhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DH
xgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==){#fig:label}

This is a reference to @fig:label.

A  |B  |C  |D
---|---|---|---
000|111|444|555
222|333|666|777

Table: This is the caption {#tbl:label}

This is a reference to @tbl:label.

$$\mbox{e}^{\mbox{i}\pi}+1=0$${#eq:label}

This is a reference to @eq:label.

This is a citation [@Muller1993].
```

The file `marky.bib` is specified in the meta data in the front
matter of the Markdown text and contains the following article.

```bibtex
@article{Muller1993,
    author  = {Peter Muller},
    title   = {The title of the work},
    journal = {The name of the journal},
    year    = {1993},
    number  = {2},
    pages   = {201-213},
    month   = {7},
    note    = {An optional note},
    volume  = {4}
}

```

**Output**

## Referenced Section {#sec:label}

This is a reference to @sec:label.

![This is the caption](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==){#fig:label}

This is a reference to @fig:label.

A  |B  |C  |D
---|---|---|---
000|111|444|555
222|333|666|777

Table: This is the caption. {#tbl:label}

This is a reference to @tbl:label.

$$\mbox{e}^{i\pi}+1=0$${#eq:label}

This is a reference to @eq:label.

This is a citation [@Muller1993].

---

# `marky.py` Command-Line Usage

## `marky.py` Script Usage

`marky` is supplied as a single-file script which contains the `marky`
`Makefile` as well as the `marky` documentation `marky.md`, `marky.mdi`
and `marky.bib`.

After downloading `marky.py` the script needs to be placed in a project
working directory `working_dir`. The script can be invoked using
a python interpreter `python` marky.py or it can be executed using a
shell:
```bash
> cd working_dir
> chmod +x marky.py
> ./marky.py
```

A new project is initialized in the `working_dir` using the `--init`
option. `marky` creates a directory tree for the project, which is
explained in detail in @sec:project. The `marky` `Makefile` and
documentation `marky.md`, `marky.mdi` and `marky.bib` are auto-generated
and placed inside the subdirs `md/` and `data/` in `working_dir`
accordingly.
```bash
> cd working_dir
> ./marky.py --init
WRITE ./Makefile
WRITE ./md/marky.md
WRITE ./md/marky.mdi
WRITE ./data/marky.bib
USAGE
1. `make help`
2. `make all-html httpd`
3. `make all-pdf`
```

`marky` renders the documentation using `pandoc` into `html` and
`pdf` using `make all`. `html` and `pdf` documents can be rendered after
installing the dependencies `python-pyyaml`, `pandoc` and `pandoc-xnos`
(`pandoc-fignos`, `pandoc-secnos`, `pandoc-eqnos`, `pandoc-tablenos`).
The details are shown in the `Makefile` help message in @sec:makefile.

## `marky` Project Structure {#sec:project}

A `marky` project has the following structure, which is auto-generated
in the project directory `working_dir` after invocation of
marky.py `--init`.

```
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

```

By invoking `make all` all files `md/*.md` are transformed
into corresponding `html/*.html` and `pdf/*.pdf` files. By
invoking `make httpd` a python web server is started in `html/`.

All user-generated project content goes into `md/*.md(i)` for
Markdown text and Markdown include files and `data/*` for images,
bibliography, videos, html frames, etc...

**ATTENTION:** The files in the directories `build/*.md` are
**auto-generated**. All user-generated content `*.md` and `*.mdi`
has to be placed inside the directory `md/`. Invoking `make clean`
will delete all files in `html/`, `build/` and `pdf/`.

## `marky` Makefile Usage {#sec:makefile}

By running `make` or `make help` in the project `working_dir` the
`Makefile` help is shown.

```
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

```

## `marky` Cheat Sheet

By running `make cheat` in the project `working_dir` the `marky` cheat
sheet is shown, which presents a quick overview of `marky` special
markup for execution of python code and manipulation of Markdown text,
according to the features describes in @sec:features.

```
#
# marky CHEAT SHEET
###################
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
#
# INCLUDE-STATEMENT
#
#  !!! path/incl.mdi FLAGS
#  \!!! This is not parsed as include statement.
#
# Flags:
#  * raw:     include without any parsing
#  * nometa:  include and ignore all meta data
#  * notext:  include and ignore all Markdown text
#  * nomarky: include but do not process marky markup
#  * #+N:     increase level of ATX headings by N
#  * >>N:     increase indentation level by N tabs
#  * >N:      increase indentation level by N spaces
#  * noref:   include without Makefile dependency
#  * aux:     only Makefile dependency but no parsing
#
#
# FORMAT LINK
#
#  [Link to Document](path/to/file.html)
#  [Link to Document](path/to/file.pdf)
#  [Format Link to Document](path/to/file.???)
#  This is not parsed as format link .\???
#
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

```

---

# `marky` Preprocessor Markup

## Yaml Meta Data in Front Matter {#sec:metadata}

Meta data is annotated in the front matter of a Markdown text document.
The front matter must start in the first line with `---` and precedes all
other text being fenced by `---`. The meta data is in `yaml` format.
The `yaml` block is parsed using `python-pyyaml`. By default all meta
data is imported into the preprocessed document. If a meta
data key starts with `-` the key is not imported into the resulting
meta data of the preprocessed document, however the key will be
exposed into the python scole as a local variable. In the following
exmample all keys except `figsize`, `figdpi` and `version` are copied
into the preprocessed Markdown document.

**Example**
```yaml

---
title: marky Documentation
date: 1. August 2021
author: Henry Lehmann
link-citations: True
bibliography: marky.bib
header-includes--pdf: >
  \hypersetup{
  colorlinks=false,
  allbordercolors={0 0 0},
  pdfborderstyle={/S/U/W 1}}
header-includes--html: >
  <style>* { box-sizing: border-box; }</style>
xnos-cleveref: True
xnos-capitalise: True
fontsize: 11pt
-version: 0.1
-figsize: [10, 8]
-figdpi: 300

---

```

The meta data fields
[`title`, `date`, `author`](https://pandoc.org/MANUAL.html#metadata-variables),
[`link-citations`](https://pandoc.org/MANUAL.html#other-relevant-metadata-fields),
[`bibliography`](https://pandoc.org/MANUAL.html#citation-rendering) and
[`header-includes`](https://pandoc.org/MANUAL.html#variables-set-automatically)
are processed by `pandoc` during document rendering. `fontsize` adjusts the
font size in [`html`](https://pandoc.org/MANUAL.html#variables-for-html)
and [`pdf`](https://pandoc.org/MANUAL.html#variables-for-latex) documents.
The `header-includes` field is used for underlining links in `pdf`
and `html` documents. The `xnos-cleveref` and `xnos-capitalise`
fields are used by the [`pandoc-xnos`](https://github.com/tomduck/pandoc-xnos)
extensions for referencing
[figures](https://github.com/tomduck/pandoc-fignos#customization),
[tables](https://github.com/tomduck/pandoc-tablenos#customization),
[sections](https://github.com/tomduck/pandoc-secnos#customization) and
[equations](https://github.com/tomduck/pandoc-eqnos#customization).

The field `header-includes` ends with `--pdf` and `--html`, which
specifies corresponding options for generation of `pdf` and `html`
documents. During make, `marky` scans all meta data fields, and
fields which end with `--pdf` and `--html` are selected and forwarded
to `pandoc` based on the format to be rendered. This was format dependent
meta data can be specified in `marky` Markdown text.

The `version` field is a user-defined field
which shows the version of this document: *0.1*. `figsize` and
`figdpi` are used in this document to control the figure size and
resolution in the `numpy` and `matplotlib` example, see @sec:examples. The font
size is 11pt and the @fig:figure1, !@fig:figure2_1,
!@fig:figure2_2, !@fig:figure2_3 and !@fig:figure2_4 have a size of
10x8cm. The font size applies to
both document text and figure text.

As the user-defined fields are preceeded with `-`, they are not copied
into the meta data of the preprocessed Markdown text. They are only
exposed into the python scope as variables for processing the `marky`
Markdown text, as described in @sec:incmeta.

## Python Code Blocks inside Markdown Text {#sec:block}

Python code can be executed during transformation of the Markdown text.
Python code is directly written inside the Markdown text and is fenced
using the `` ``` `` statement. The block needs to start with either
`!` or `!!`.
* `!`: The python code is executed and **shown** in the output.
* `!!`: The python code is executed and **hidden** in the output.

```md
	```!
		<python_code_shown>
	```

	```!!
		<python_code_hidden>
	```
```

Meta data from Markdown front matter can be used as local variables in
python code blocks. The `import` statement can be used in python code
blocks in order to access installed python packages. All code blocks
span one large scope for sharing functions and local variables.
Using the `print()` function the text will be printed to the console
and **not** inside the resulting Markdown text. In order to modify
the Markdown text using `marky` during preprocessing, the `_()` statement
has to be used, see @sec:mdprint.

**Example**
```python
	import numpy as np
	def get_x(a=0):
		return np.array([41 + a])
	y = 1
```

This is a paragraph.

```python
	x = get_x(y)
	print("Hello Console! x is", x)
```

## Generation of Markdown Text using Python Code {#sec:mdprint}

### The `_()` Statement

Using the `print()` statement the text will be printed to the console.
When using the `_()` and `__()` statements new Markdown text can be
inserted dynamically into the document during preprocessing.

**`_()` Statement**
* `_(*args, sep=" ")`:
	1. convert arguments to string
	2. join arguments using `sep`
* `_(_, *args   )`: append to previous output
* `_(_, *args, _)`: append to previous output and append next output
* `_(   *args, _)`: append next output to this output

**`__()` Statement**
* `__(arg, crop=True, shift="")`:
	1. convert `arg` to string
	2. crop and prepend `shift` string to each line
* `__(arg, _)`: append next output to this output

**Crop and Shift**
```py
def test():
	__("""
		* List Level 1
		* List Level 1
	""")
	__("""
		* List Level 2
		* List Level 2
		    * List Level 3
	""", shift=" "*4)
```

```md
* List Level 1
* List Level 1
    * List Level 2
    * List Level 2
        * List Level 3
```

**Example**
```python
	y += 1
	__(f"""
		* This is `marky` Version *{version}*.
		* This is `marky` Version *{version}*.
	""")
	__(f"""
		1. This is `marky` Version *{version}*.
		2. This is `marky` Version *{version}*.
	""", shift=" "*4)
```
* This is `marky` Version *0.1*.
* This is `marky` Version *0.1*.
    1. This is `marky` Version *0.1*.
    2. This is `marky` Version *0.1*.

```python
	_("This", _)
	_("is")
	_(_, " one", _)
	_("line! not ending with \\")
	_("this?")
```
Thisis oneline! not ending with \
this?

```python
	_(f"Hello Markdown! x is **{x}** and y is *{y}*")
```
Hello Markdown! x is **[42]** and y is *2*

### Indentation of the `_()` Statement

The `_()` statement needs to be indented according to the python program
flow (`for`, `while`, `if`, `else`, `try`, `with`, `def`, `class`) and
supports dynamic insertion of Markdown text into the document based
on loops and conditions.

**Example 1**

```python
	_("This is the **generated output**:")
	_("")
	_("> This is a *listing*:")
	text = ["zero", "one", "two", "three"]
	for i in range(10):
		if i < 2:
			_(f"> {i}")
		elif i == 2:
			j = text[i]
			_(f"> {j}")
		elif i == 3:
			_("")
		elif i < 7:
			_(f">> {'    '*(i-4)}* {i}")
		elif i == 7:
			_("")
		else:
			j = i - 7
			k = text[j]
			_(f"> {j}. {k}")
```
This is the **generated output**:

> This is a *listing*:
> 0
> 1
> two

>> * 4
>>     * 5
>>         * 6

> 1. one
> 2. two

**Example 2**

@tbl:table1 is generated using the following python clode block.

```python
	n = 13
	dec = ["*%s*", "**%s**", "~~%s~~", "`%s`",
		r"$\times^%s$", "$\infty_%s$"]
	_("|".join("X"*n) + "\n" + "|".join("-"*n))
	for i in range(n):
		fill = [chr(ord("A")+(2*i+3*k)%26) for k in range(i+1)]
		fill = [dec[(l+i)%len(dec)]%k for l, k in enumerate(fill)]
		text = list("0")*n
		text[(n>>1)-(i>>1):(n>>1)+(i>>1)] = fill
		_("|".join(text))
```
X|X|X|X|X|X|X|X|X|X|X|X|X
-|-|-|-|-|-|-|-|-|-|-|-|-
0|0|0|0|0|0|*A*|0|0|0|0|0|0|0
0|0|0|0|0|0|**C**|~~F~~|0|0|0|0|0|0|0
0|0|0|0|0|~~E~~|`H`|$\times^K$|0|0|0|0|0|0
0|0|0|0|0|`G`|$\times^J$|$\infty_M$|*P*|0|0|0|0|0|0
0|0|0|0|$\times^I$|$\infty_L$|*O*|**R**|~~U~~|0|0|0|0|0
0|0|0|0|$\infty_K$|*N*|**Q**|~~T~~|`W`|$\times^Z$|0|0|0|0|0
0|0|0|*M*|**P**|~~S~~|`V`|$\times^Y$|$\infty_B$|*E*|0|0|0|0
0|0|0|**O**|~~R~~|`U`|$\times^X$|$\infty_A$|*D*|**G**|~~J~~|0|0|0|0
0|0|~~Q~~|`T`|$\times^W$|$\infty_Z$|*C*|**F**|~~I~~|`L`|$\times^O$|0|0|0
0|0|`S`|$\times^V$|$\infty_Y$|*B*|**E**|~~H~~|`K`|$\times^N$|$\infty_Q$|*T*|0|0|0
0|$\times^U$|$\infty_X$|*A*|**D**|~~G~~|`J`|$\times^M$|$\infty_P$|*S*|**V**|~~Y~~|0|0
0|$\infty_W$|*Z*|**C**|~~F~~|`I`|$\times^L$|$\infty_O$|*R*|**U**|~~X~~|`A`|$\times^D$|0|0
*Y*|**B**|~~E~~|`H`|$\times^K$|$\infty_N$|*Q*|**T**|~~W~~|`Z`|$\times^C$|$\infty_F$|*I*|0

Table: Table is generated using code and the `_()` statement. {#tbl:table1}

## Formatted Output of Python Variables {#sec:format}

`marky` can output python variables inline into Markdown text using
the `` `!VARIABLE` `` statement. `VARIABLE` can be any python variable
from a python code block or meta data field. The output can be
formatted using the `` `!VARIABLE[:FORMAT]` `` statement according
to the python operator `{<variable>[:<format>]}` implemented in the
[`str.format()`](https://docs.python.org/3/library/string.html#formatstrings)
specification. The `` `!VARIABLE` `` statement is escaped
using `` `\!VARIABLE` ``.

**Example**
```python
	x = int(1)
	y = float(2.3)
	z = 0
	a = [1, 2, 3]
	b = (4, 5)
```

```md
This is a paragraph and x is `!x:03d` and y is `!y:.2f`.
Other content is: `!a`, `!b` and escaping works: `\!z`.
```

This is a paragraph and x is 001 and y is 2.30.
Other content is: [1, 2, 3], (4, 5) and escaping works: `!z`.

## Output Results of Python Expressions {#sec:inline}

`marky` outputs results of python expressions inline into Markdown text
using the `` `!EXPRESSION` `` statement. `EXPRESSION` can be any python
expression. The output can be formatted using the python
`` `!EXPRESSION[:FORMAT]` `` statement according to the python operator
`{<expression>[:<format>]}` implemented in the python
[`f`-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
specification. The `` `!EXPRESSION` `` statement is escaped
using `` `\!EXPRESSION` ``.

**Example**
```md
This is a list with the numbers `!", ".join([str(i) for i in a])`.
The result of the function `get_x` is `!get_x()` and escaping
works: `\!get_x(b[1])[0]`.
```

This is a list with the numbers 1, 2, 3.
The result of the function `get_x` is [41] and escaping
works: `!get_x(b[1])[0]`.

## Include Statement and Make Dependencies {#sec:include}

`marky` supports include of Markdown text using the `!!!` statement.
The `!!!` statement must be on a single line and follows the path
of the include file. The path of the include file is relative to
the root Markdown document which is processed. The paths of all
included files are collected and a `Makefile` rule is created and
stored in a file (path of output Markdown text appended with `.mk`).

The `!!!` statement is escaped using `\!!!`.
The include statement **cannot** be used in code blocks. `marky` Markdown
text must have the extension `.md` and include files must have the
extension `.mdi`

The include statement supports flags for parsing the include file.
```md
!!! PATH/FILE.mdi FLAGS
```

**Flags**
* `raw`: the file is included as is without any parsing
* `nometa`: meta data in front matter is skipped during parsing
* `notext`: all Markdown text is skipped during parsing
* `nomarky`: include the Markdown text without any `marky` processing
* `#+N`: increase the level of ATX headings `#`. The headings are
parsed according to `pandoc` extensions
([blank_before_header](https://pandoc.org/MANUAL.html#extension-blank_before_header),
[space_in_atx_header](https://pandoc.org/MANUAL.html#extension-space_in_atx_header))
* `>>N`: increase the indentation using `N` tabs
* `>N`: increase the indentation using `N` spaces
* `noref`: do not reference this file as Makefile dependency
* `aux`: reference as Makefile dependency, but do not process

**Example**
```md
!!! marky.mdi #+2
The file was included: `!included` and $x=`!x`$ and $y=`!y`$.
```

### Included Section
```python
	print("Hello Console!")
	_("Hello Markdown!")
	x = 123
	y = 4.567
```
Hello Markdown!

First|Second
-----|------
00123|4.5670

The file was included: 1 and $x=123$ and $y=4.567$.

The file `marky.mdi` was loaded with shifting ATX headings by 2 which
means `##` has been added to the included section. The file contains:
```md
	---
	included: 1
	---
	# Included Section
	```!
		print("Hello Console!")
		_("Hello Markdown!")
		x = 123
		y = 4.567
	```
	
	First|Second
	-----|------
	`?x:05d`|`?y:.4f`
	
```
The unmodified source was loaded using the flags `raw >>1`.

The file `marky.md.mk` contains:
```Makefile
build/marky.md: \
md/marky.mdi

.PHONY: md-marky
md-marky: build/marky.md

.PHONY: html-marky
html-marky: html/marky.html

.PHONY: pdf-marky
pdf-marky: pdf/marky.pdf
```

## Include Statement and Meta Data Import {#sec:incmeta}

The include statement `!!!` loads and parses an `*.mdi` include file.
The `yaml` meta data in the front matter of the document also is loaded
and parsed if the `nometa` flag is not specified in the include
statement. Assuming the root document and the included document have the
following meta data.

**Root Document**
```yaml

---
width: 10
height: 20

---
!!! include.mdi
```

**Included Document**
```yaml

---
depth: 30
volume: 6000
-serial: A56GHJ

---
```

By default all `yaml` meta data fields are copied to the meta data of
the root Markdown document which is processed. However, if a meta data
key is preceeded by `-` the key is not imported into the root document.
All `yaml` meta data keys which start with `-` are exposed to the
python scope and will appear as local variables, but they will not
appear in the meta data of the front matter in the preprocessed
Markdown text. Given the example above, the resulting meta data in
the front matter of the preprocessed Markdown text looks as follows.

**Preprocessed Document**
```yaml

---
width: 10
height: 20
depth: 30
volume: 6000

---
```

## Format Links for `html` and `pdf` Documents {#sec:formlink}

When writing multiple documents, often documents are referenced
between each other using links. In order to refer to external
`html` and `pdf` documents the Markdown link statement is used.
```md
[Link Caption](path/to/file.html)
[Link Caption](path/to/file.pdf)
```

When using relative paths in the URL, the documents can be referenced
according to the directory tree of the source `marky` Markdown text
`md/*/*.md`. However, the resulting link will be a path relative
to the directory `html/` for `html` documents and relative to `pdf/`
for `pdf` documents. As all `html` and `pdf` documents are kept in
separate directories, one link statement cannot be used for rendering
`html` and `pdf` with consistent paths in the link statement.

By using the `marky` format link statement `.???`, the file extension
in the links is replaced depending on the output format
resuling in consistent links for `html` and `pdf`
documents. The format link statement can be escaped using `.\???`.

**Example**
```md
[Link to this Document](marky.???)
```

[Link to this Document](marky.html)

## Format Codes for `html` and `pdf` Documents {#sec:formcode}

Often when writing markdown for `html` and `pdf` documents, the
format needs to be adjusted according to the format. `pandoc` Markdown
already renders all common Markdown into `html` and `pdf`.
`marky` supports format specific tweaking using format codes.

In order to inject format specific code, `html` code or `tex` code
for `pdf` documents, the format codes are used. A format code is
written as `` `?FMTCODE(ARGS)` `` which is translated in two python
function calls:
1. `FMTCODE_html(ARGS)`: format code for injection of raw `html`
code for rendering `html`-based documents in `pandoc`.
2. `FMTCODE_pdf(ARGS)`: format code for injection of raw `tex`
code in `pdf`-based documents in `pandoc`.

During preprocessing, `marky` processes all format codes for each
format `html` and `pdf` and caches the output. Before rendering
the Markdown in one particular format using `pandoc`, `marky` extracts
the results of the corresponding format codes and skips the others.
Additional `tex` packages have to be included using the meta data
field `header-includes`.

For returning the raw format code, either the `_()` statement can
be used @sec:mdprint **or** the `return` statement can be used.
If both statements are mixed, the output which had been returned
will be appended to the text generated with the `_()` statement.

**Example**
```python
	def test1_html():
		_("This is HTML1 and")
		return "it goes on here!"
	def test1_pdf():
		__("""
			This is \{PDF1\} and
		""")
	def test2_html():
		return """
			This is HTML2!
		"""
	def test2_pdf():
		pass
```

```md
The output of the format code `\?test1()` is "`?test1()`" and
`\?test2()` is "`?test2()`" (in HTML it is not empty).
```

The output of the format code `?test1()` is "This is HTML1 and
it goes on here!" and
`?test2()` is "This is HTML2!" (in HTML it is not empty).

---

# `marky` Markdown Examples {#sec:examples}

## JavaScript in `html` and Placeholder in `pdf`

When creating Markdown text for `html` output, the user often wants
interactivity using widgets like sliders, check boxes, drop down boxes
etc. However, when exporting into `pdf` those elements need to be
replaced with non-interactive placeholders. In order to develop a single
Markdown document, which can be rendered in `html` with interactive
elements and into `pdf` with placeholder, the `marky` format codes can be
used, see @sec:formcode. The following example defines a
`<input type="range">` and two `<spans>` with `id="myval"` and
`id="myres"`, in order to update the value of $y=sin(x)$ in `html`. For
`pdf` output the equation and the value range is shown.

**Example**
```python
	def range_html():
		__("""
			$x\in [0$ <input type='range' value='0' min='0' max='100'
			onchange="
			document.getElementById('myval').innerHTML = this.value;
			document.getElementById('myres').innerHTML =
			Math.sin(this.value);"> $100]$
		""")
	def range_pdf():
		return "$x\in[0,100]$"
	def formula_html():
		__("""
			$y=sin(x)=$ <span id="myres">0.000</span>
			with $x=$ <span id="myval">0</span>
		""")
	def formula_pdf():
		return "$y=sin(x)$"
```

```md
$x$ and $y$ are related to each other by `?formula()`.

$x$ must be in the range `?range()`.
```

$x$ and $y$ are related to each other by $y=sin(x)=$ <span id="myres">0.000</span>
with $x=$ <span id="myval">0</span>.

$x$ must be in the range $x\in [0$ <input type='range' value='0' min='0' max='100'
onchange="
document.getElementById('myval').innerHTML = this.value;
document.getElementById('myres').innerHTML =
Math.sin(this.value);"> $100]$.

## Generate a Figure on-the-fly during Preprocessing

This section illustrates how python modules can be used to create
document content. Document content is placed inside the `data/`
directory of the current project working directory (refer to `marky`
project structure, @sec:project)

![This Figure was generated using `numpy` and
`matplotlib`.](figure1.png){#fig:figure1}

[`numpy`](https://www.numpy.org) and [`matplotlib`](https://www.matplotlib.org)
are powerful python modules for mathematical computing and plot
generation. The following example shows how to generate @fig:figure1
using `numpy` and `matplotlib` and include it into the document.

**Example**

```python
	import numpy as np
	import matplotlib.pyplot as plt
	GREEK = lambda A: chr(ord(u"\u0391") + ord(A) - ord("A"))
	greek = lambda a: chr(ord(u"\u03b1") + ord(a) - ord("a"))
	cm2inch = lambda xy: tuple(i/2.54 for i in xy)
	fontsize = int(fontsize[:-2]) # convert to int
	figsize = cm2inch(figsize) # convert from cm to inch
	params = {
		'figure.figsize': figsize,
		'legend.fontsize': fontsize,
		'axes.labelsize': fontsize,
		'axes.titlesize': fontsize,
		'xtick.labelsize': fontsize,
		'ytick.labelsize': fontsize,
		'font.family': 'Times New Roman'
	}
	plt.rcParams.update(params)
	x = np.random.rand(50)
	y = np.random.rand(50)
	plt.figure()
	plt.scatter(x, y, label="Random Coordinates")
	text = "".join([greek(i) for i in ["a", "b", "c", "d"]])
	plt.annotate(text, xy=(0.5,0.5), xytext=(0.25,0.25),
		arrowprops=dict(arrowstyle='->',lw=1.5))
	plt.title("Two Random Datasets")
	plt.xlabel(r"Data #1 - $\mathdefault{%s_1}$" % GREEK("C"))
	plt.ylabel(r"Data #2 - $\mathdefault{%s_2}$" % GREEK("D"))
	plt.grid()
	plt.legend()
	plt.tight_layout()
	plt.savefig("data/figure1.png", dpi=figdpi)
	plt.close("all")
```

```md
![This Figure was generated using `numpy`
and `matplotlib`.](figure1.png){#fig:figure1}
```

## Generate a Sequence of Figures on-the-fly

This section illustrates how a sequence of complex figures can be
generated using `numpy` and `matplotlib` and how the figures are formatted
using python and referenced using `marky`.

Suppose one experiment which can be run in four different setups with
different values for $\lambda=$
(1) $125.33$nm, (2) $250.66$nm, (3) $375.99$nm, (4) $501.32$nm.
Each run of the experiment using setup (1)--(4), two additional
parameters $\varepsilon$ and $\alpha$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz respectively.

The results of the experiments for the setups (1)--(4) are summarized
in the @fig:figure2_1, !@fig:figure2_2, !@fig:figure2_3 and
!@fig:figure2_4.

**Example**

```python
	n = 100
	alpha = u"\u03b1"
	epsilon = u"\u03b5"
	lamda = u"\u03bb"
	f = lambda x, a, b: a*(np.sqrt(x)+b*np.sin(x*b))
	g = lambda x, a ,b, c: np.fabs(f(x, a, b) - f(c, a, b)) + c
	dat = np.zeros((n-1, 3, 3, 4), dtype=np.float32)
	cols = ["red", "green", "blue"]
	mark = ["o", "x", "<"]
	x = np.array([50.*x/n for x in range(1, n)], dtype=np.float32)
	for k, c in enumerate([10., 20., 30., 40.]):
		for i, a in enumerate([1, 2, 4]):
			for j, b in enumerate([0.2, 0.4, 0.6]):
				dat[:, i, j, k] = g(x, a, b, c)
		plt.figure()
		for j in range(3):
			for i in range(3):
				label_i = "%s=%.1f%%" % (epsilon, (i+1)*10.2) \
					if j == 0 else None
				label_j = "%s=%.1fHz" % (alpha, (j+1)/10.) \
					if i == 0 else None
				y = dat[:, i, j, k].flatten()
				plt.plot(x, y, color=cols[i], lw=0.75, label=label_i)
				plt.scatter(x[1::4], y[1::4], color="black",
					marker=mark[j], lw=0.5, s=5, label=label_j)
		k = k + 1
		kval = k*125.33
		plt.title("Experiment Setup #%d: %s=%.2fnm" % (k, lamda, kval))
		plt.xlabel("Time [s]")
		plt.ylabel("Intensity [kg/s³]")
		plt.grid()
		plt.legend()
		plt.tight_layout()
		plt.savefig("data/figure2-%d.png" % k, dpi=figdpi)
		plt.close("all")
		__(f"""
			![This is the result of the experiment according
			to the setup #{k} with ${lamda}={kval}$nm. The parameters
			${epsilon}$ and ${alpha}$ are varried between
			$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz
			respectively.](figure2-{k}.png){{#fig:figure2_{k}}}

		""")
```
![This is the result of the experiment according
to the setup #1 with $λ=125.33$nm. The parameters
$ε$ and $α$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz
respectively.](figure2-1.png){#fig:figure2_1}

![This is the result of the experiment according
to the setup #2 with $λ=250.66$nm. The parameters
$ε$ and $α$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz
respectively.](figure2-2.png){#fig:figure2_2}

![This is the result of the experiment according
to the setup #3 with $λ=375.99$nm. The parameters
$ε$ and $α$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz
respectively.](figure2-3.png){#fig:figure2_3}

![This is the result of the experiment according
to the setup #4 with $λ=501.32$nm. The parameters
$ε$ and $α$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz
respectively.](figure2-4.png){#fig:figure2_4}


---

*Thanks for reading, please try `marky`.*

---

# References
