---
title: marky Documentation
date: 1. August 2021
author: Henry Lehmann
link-citations: true
bibliography: marky.bib
header-includes--pdf: >
   \hypersetup{colorlinks=false,
   allbordercolors={0 0 0},
   pdfborderstyle={/S/U/W 1}}
header-includes--html: >
   <style>* { box-sizing: border-box; }</style>
xnos-cleveref: true
xnos-capitalise: true
fontsize: 11pt
-figsize: [10,8]
-figdpi: 300
-version: undefined

---
!!! ../Makefile aux
!!! ../marky.py aux
```!!
	import subprocess
	MD = "Markdown"
	M = "`marky`"
	MF = "`Makefile`"
	MP = "`marky.py`"
	Mp = "marky.py"
	P = "`pandoc`"
	NU = "`numpy`"
	PL = "`matplotlib`"
	R = "RMarkdown"
	Q = "Quarto"
	BT = "`"
	P1= "`_()`"
	P2= "`__()`"
	version = subprocess.check_output(["python", "marky.py",
		"--version"]).decode("utf-8").strip()
```

---

> **Abstract** -- `!M` is a preprocessor for `!MD` using Python.
> `!M` is inspired by [pandoc](https://www.pandoc.org/),
> [`!R`](https://rmarkdown.rstudio.com/), [`!Q`](https://quarto.org/).
> This document is created using `!M` (Version `!version`) and
> contains examples which illustrate the generation of
> document content for `html` and `pdf` and the dynamical adjustment
> of `!MD` text during preprocessing based on `python` code.
> The full raw `!M` source code of this documentation appended at
> the end. The `marky` source code of this document can be read
> [here](marky-src.???). For `marky` download please refer to the
> [`marky` repository](https://github.com/lehmann7/marky).

---

# Introduction

`!M` is a `!MD` preprocessor which transforms a `!MD` document
using python. `!M` implements new markup which controls the execution
of python code and the generation and manipulation of `!MD` text.

`!M` only depends on `!P` and `pyyaml`. `!P` is used for rendering
the `!MD` into `html` and `pdf`. `!P` supports various `!MD`
extensions allowing for scientific writing using equations, figures,
tables, citations and corresponding referencing mechanism for the latter.
`pyyaml` is used for parsing meta data in the front matter of the
`!MD` text if it is present.

Workflow for creating `html` or `pdf` using `!M`

1. user writes a `!MD` text file and places it in `md/*.md`
directory with the extension `.md`. the `!MD` text contains
special `!M` markup which executes python code and manipulates
the `!MD` text.

2. `!M` transforms the files in `md/*.md` into regular `!MD` text
and places the transformed files in `build/*.md`. The transformed text
only contains regular `!MD`, and placeholders for format dependent
output for `html` and `pdf`.

3. before rendering `!M` replaces placeholders for format dependent
output with content creating a temporary file which only contains
regular `!MD` text for `html` and `pdf` documents according to
`!P` `!MD` specification.

4. the regular `!MD` text in the files `build/*.md` is rendered into
`html` and `pdf` using `!P`.

The three steps are implemented in `!MP` and a `!MF`. The
following document describes the special `!M` markup and shows
how to use `!MP` and the `!MF`.

---

# Related Work {#sec:related}

For scientific reporting and writing usually typesetting systems or
complicted WYSIWYG editors are used. In order to simplify the writing
different approaches and frameworks have been developed.

* [`!P`](https://www.pandoc.org/),
* [`!R`](https://rmarkdown.rstudio.com/)
* [Quarto](https://quarto.org/)
* [Scientific `!MD`](https://jaantollander.com/post/scientific-writing-with-markdown/)
* [Technical `!P`](https://lee-phillips.org/panflute-gnuplot/)

All of those approaches use `!P` as an underlying framework for document
conversion. `!P` is a powerful framework for conversion between different
document formats including `!M`, `html` and `pdf`. `!P` implements an
own internal AST, in which different document formats can be imported and
exported. Using this intermediate document representation, `!P` allows
to modify document using filters, which operate on the AST. Filters
can be written in [`haskell`](https://pandoc.org/filters.html),
[`lua`](https://pandoc.org/lua-filters.html) and
[`python`](https://pandoc.org/filters.html#but-i-dont-want-to-learn-haskell).

Where as `!R` and `!Q` are integrated frameworks, which additionally
depend on `knitr`, `RStudio`, `Jupyter`, `!M` depends on `!P` and `pyyaml`
only. `!M` natively only supports executable python code blocks, however,
other languages can be executed using wrappers, which are available for
other languages.

---

# `!M` Features {#sec:features}

`!M` implements following features using an simple `!MD`-style syntax.

1. read `!MD` meta data from front matter,
see @sec:metadata
```md
	---
		<key>: <value>
	---
```

2. execute and hide/show python code blocks inside `!MD` text,
see @sec:block
```md
	`!BT*3`!
		<python_code_shown>
	`!BT*3`

	`!BT*3`!!
		<python_code_hidden>
	`!BT*3`
```

3. generate `!MD` text using python code, see @sec:mdprint
```md
	`!BT*3`!
		_("<markdown_text>")
		__("""
			<markdown_text>
			<markdown_text>
			<markdown_text>
		""")
	`!BT*3`
```

4. format output of python variables into `!MD` text,
see @sec:format
```md
	Output into text: `\!<python_variable>`
```

5. output the result of python expressions into `!MD` text,
see @sec:inline
```md
	Output into text: `\!<python_expression>`
```

6. include `!MD` text, make dependencies and forward meta data,
see @sec:include and !@sec:incmeta.
```md
	!!! include_file.mdi
```

7. format links in `html` and `pdf` documents for
referencing external documents of the same format,
see @sec:formlink.
```md
	[Format Link to html/pdf document](path/to/file.\???)
```

8. use format codes in order to inject format specific
code in `html` and `pdf` documents,
see @sec:formcode.
```md
	`!BT*3`!
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
	`!BT*3`

	Format dependent output: `\!code()`
```

---

# Scientific Writing in `!MD` {#sec:panmd}

[`!MD`](https://pandoc.org/MANUAL.html#pandocs-markdown) is a markup
language for technical writing, with emphasis on readability. `!MD`
can be rendered in many formats including `html` and `pdf` by using
[`!P`](https://pandoc.org/) for example.

Using various `!MD` extensions of `!P` a sufficient structure for
writing scientific documents can be reflected using `!MD` syntax.
`!M` uses the following `!P` `!MD` extensions.
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

`!P` supports
[equations](https://pandoc.org/MANUAL.html#extension-tex_math_dollars)
rendered inline and single-line in tex-style using `$...$` and `$$...$$`,
[bibliography](https://pandoc.org/MANUAL.html#citations)
using the `--citeproc` option,
[section numbering](https://pandoc.org/MANUAL.html#extension-header_attributes)
using the `--number-sections` option and
[table of contents](https://pandoc.org/MANUAL.html#option--toc)
using the `--table-of-contents` option.

`!P` supports [`xnos`](https://github.com/tomduck/pandoc-xnos) filters
for referencing document content like
[figures](https://github.com/tomduck/pandoc-fignos#usage),
[equations](https://github.com/tomduck/pandoc-eqnos#usage),
[tables](https://github.com/tomduck/pandoc-tablenos#usage),
[sections](https://github.com/tomduck/pandoc-secnos#usage)
by using the `--filter pandoc-xnos` option.
`xnos` integrates clever references, which means "Fig.", "Sec.", "Eq."
and "Tab." are added automatically to the corresponding element.
If the prefix is to be omitted, the reference can be written as
`\!@ref:label`.

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
matter of the `!MD` text and contains the following article.

```bibtex
!!! ../data/marky.bib raw
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

# `!MP` Command-Line Usage

## `!MP` Script Usage

`!M` is supplied as a single-file script which contains the `!M`
`!MF` as well as the `!M` documentation `marky.md`, `marky.mdi`
and `marky.bib`.

After downloading `!MP` the script needs to be placed in a project
working directory `working_dir`. The script can be invoked using
a python interpreter `python` `!Mp` or it can be executed using a
shell:
```bash
> cd working_dir
> chmod +x marky.py
> ./marky.py
```

A new project is initialized in the `working_dir` using the `--init`
option. `!M` creates a directory tree for the project, which is
explained in detail in @sec:project. The `!M` `!MF` and
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

`!M` renders the documentation using `!P` into `html` and
`pdf` using `make all`. `html` and `pdf` documents can be rendered after
installing the dependencies `python-pyyaml`, `pandoc` and `pandoc-xnos`
(`pandoc-fignos`, `pandoc-secnos`, `pandoc-eqnos`, `pandoc-tablenos`).
The details are shown in the `!MF` help message in @sec:makefile.

## `!M` Project Structure {#sec:project}

A `!M` project has the following structure, which is auto-generated
in the project directory `working_dir` after invocation of
`!Mp` `--init`.
```!!
	text = ""
	for i in subprocess.check_output(["make",
		"tree"]).decode("utf-8").split("\n"):
		if i.startswith("#"):
			text += i + "\n"
```

```
`!text`
```

By invoking `make all` all files `md/*.md` are transformed
into corresponding `html/*.html` and `pdf/*.pdf` files. By
invoking `make httpd` a python web server is started in `html/`.

All user-generated project content goes into `md/*.md(i)` for
`!MD` text and `!MD` include files and `data/*` for images,
bibliography, videos, html frames, etc...

**ATTENTION:** The files in the directories `build/*.md` are
**auto-generated**. All user-generated content `*.md` and `*.mdi`
has to be placed inside the directory `md/`. Invoking `make clean`
will delete all files in `html/`, `build/` and `pdf/`.

## `!M` Makefile Usage {#sec:makefile}

By running `make` or `make help` in the project `working_dir` the
`!MF` help is shown.
```!!
	text = ""
	for i in subprocess.check_output(["make",
		"help"]).decode("utf-8").split("\n"):
		if i.startswith("#"):
			text += i + "\n"
```

```
`!text`
```

## `!M` Cheat Sheet

By running `make cheat` in the project `working_dir` the `!M` cheat
sheet is shown, which presents a quick overview of `!M` special
markup for execution of python code and manipulation of `!MD` text,
according to the features describes in @sec:features.
```!!
	text = ""
	for i in subprocess.check_output(["make",
		"cheat"]).decode("utf-8").split("\n"):
		if i.startswith("#"):
			i = i.replace(r".\???", r".\\???")
			i = i.replace(r".???", r".\???")
			text += i + "\n"
```

```
`!text`
```

---

# `!M` Preprocessor Markup

## Yaml Meta Data in Front Matter {#sec:metadata}

Meta data is annotated in the front matter of a `!MD` text document.
The front matter must start in the first line with `---` and precedes all
other text being fenced by `---`. The meta data is in `yaml` format.
The `yaml` block is parsed using `python-pyyaml`. By default all meta
data is imported into the preprocessed document. If a meta
data key starts with `-` the key is not imported into the resulting
meta data of the preprocessed document, however the key will be
exposed into the python scole as a local variable. In the following
exmample all keys except `figsize`, `figdpi` and `version` are copied
into the preprocessed `!MD` document.

**Example**
```yaml

---
title: `!title`
date: `!date`
author: `!author`
link-citations: `!link_citations`
bibliography: `!bibliography`
header-includes--pdf: >
  \hypersetup{
  colorlinks=false,
  allbordercolors={0 0 0},
  pdfborderstyle={/S/U/W 1}}
header-includes--html: >
  <style>* { box-sizing: border-box; }</style>
xnos-cleveref: `!xnos_cleveref`
xnos-capitalise: `!xnos_capitalise`
fontsize: `!fontsize`
-version: `!version`
-figsize: `!figsize`
-figdpi: `!figdpi`

---

```

The meta data fields
[`title`, `date`, `author`](https://pandoc.org/MANUAL.html#metadata-variables),
[`link-citations`](https://pandoc.org/MANUAL.html#other-relevant-metadata-fields),
[`bibliography`](https://pandoc.org/MANUAL.html#citation-rendering) and
[`header-includes`](https://pandoc.org/MANUAL.html#variables-set-automatically)
are processed by `!P` during document rendering. `fontsize` adjusts the
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
documents. During make, `!M` scans all meta data fields, and
fields which end with `--pdf` and `--html` are selected and forwarded
to `!P` based on the format to be rendered. This was format dependent
meta data can be specified in `!M` Markdown text.

The `version` field is a user-defined field
which shows the version of this document: *`!version`*. `figsize` and
`figdpi` are used in this document to control the figure size and
resolution in the `!NU` and `!PL` example, see @sec:examples. The font
size is `!fontsize` and the @fig:figure1, !@fig:figure2_1,
!@fig:figure2_2, !@fig:figure2_3 and !@fig:figure2_4 have a size of
`!"x".join(str(i) for i in figsize)`cm. The font size applies to
both document text and figure text.

As the user-defined fields are preceeded with `-`, they are not copied
into the meta data of the preprocessed `!MD` text. They are only
exposed into the python scope as variables for processing the `!M`
`!MD` text, as described in @sec:incmeta.

## Python Code Blocks inside `!MD` Text {#sec:block}

Python code can be executed during transformation of the `!MD` text.
Python code is directly written inside the `!MD` text and is fenced
using the `` `!BT*3` `` statement. The block needs to start with either
`\!` or `\!!`.
* `\!`: The python code is executed and **shown** in the output.
* `\!!`: The python code is executed and **hidden** in the output.

```md
	`!BT*3`!
		<python_code_shown>
	`!BT*3`

	`!BT*3`!!
		<python_code_hidden>
	`!BT*3`
```

Meta data from `!MD` front matter can be used as local variables in
python code blocks. The `import` statement can be used in python code
blocks in order to access installed python packages. All code blocks
span one large scope for sharing functions and local variables.
Using the `print()` function the text will be printed to the console
and **not** inside the resulting `!MD` text. In order to modify
the `!MD` text using `!M` during preprocessing, the `!P1` statement
has to be used, see @sec:mdprint.

**Example**
```!
	import numpy as np
	def get_x(a=0):
		return np.array([41 + a])
	y = 1
```

This is a paragraph.

```!
	x = get_x(y)
	print("Hello Console! x is", x)
```

## Generation of `!MD` Text using Python Code {#sec:mdprint}

### The `!P1` Statement

Using the `print()` statement the text will be printed to the console.
When using the `!P1` and `!P2` statements new `!MD` text can be
inserted dynamically into the document during preprocessing.

**`!P1` Statement**
* `_(*args, sep=" ")`:
	1. convert arguments to string
	2. join arguments using `sep`
* `_(_, *args   )`: append to previous output
* `_(_, *args, _)`: append to previous output and append next output
* `_(   *args, _)`: append next output to this output

**`!P2` Statement**
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
```!
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

```!
	_("This", _)
	_("is")
	_(_, " one", _)
	_("line! not ending with \\")
	_("this?")
```

```!
	_(f"Hello Markdown! x is **{x}** and y is *{y}*")
```

### Indentation of the `!P1` Statement

The `!P1` statement needs to be indented according to the python program
flow (`for`, `while`, `if`, `else`, `try`, `with`, `def`, `class`) and
supports dynamic insertion of `!MD` text into the document based
on loops and conditions.

**Example 1**

```!
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

**Example 2**

@tbl:table1 is generated using the following python clode block.

```!
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

Table: Table is generated using code and the `!P1` statement. {#tbl:table1}

## Formatted Output of Python Variables {#sec:format}

`!M` can output python variables inline into `!MD` text using
the `` `\!VARIABLE` `` statement. `VARIABLE` can be any python variable
from a python code block or meta data field. The output can be
formatted using the `` `\!VARIABLE[:FORMAT]` `` statement according
to the python operator `{<variable>[:<format>]}` implemented in the
[`str.format()`](https://docs.python.org/3/library/string.html#formatstrings)
specification. The `` `\!VARIABLE` `` statement is escaped
using `` `\\!VARIABLE` ``.

**Example**
```!
	x = int(1)
	y = float(2.3)
	z = 0
	a = [1, 2, 3]
	b = (4, 5)
```

```md
This is a paragraph and x is `\!x:03d` and y is `\!y:.2f`.
Other content is: `\!a`, `\!b` and escaping works: `\\!z`.
```

This is a paragraph and x is `!x:03d` and y is `!y:.2f`.
Other content is: `!a`, `!b` and escaping works: `\!z`.

## Output Results of Python Expressions {#sec:inline}

`!M` outputs results of python expressions inline into `!MD` text
using the `` `\!EXPRESSION` `` statement. `EXPRESSION` can be any python
expression. The output can be formatted using the python
`` `\!EXPRESSION[:FORMAT]` `` statement according to the python operator
`{<expression>[:<format>]}` implemented in the python
[`f`-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
specification. The `` `\!EXPRESSION` `` statement is escaped
using `` `\\!EXPRESSION` ``.

**Example**
```md
This is a list with the numbers `\!", ".join([str(i) for i in a])`.
The result of the function `get_x` is `\!get_x()` and escaping
works: `\\!get_x(b[1])[0]`.
```

This is a list with the numbers `!", ".join([str(i) for i in a])`.
The result of the function `get_x` is `!get_x()` and escaping
works: `\!get_x(b[1])[0]`.

## Include Statement and Make Dependencies {#sec:include}

`!M` supports include of `!MD` text using the `\!!!` statement.
The `\!!!` statement must be on a single line and follows the path
of the include file. The path of the include file is relative to
the root `!MD` document which is processed. The paths of all
included files are collected and a `!MF` rule is created and
stored in a file (path of output `!MD` text appended with `.mk`).

The `\!!!` statement is escaped using `\\!!!`.
The include statement **cannot** be used in code blocks. `!M` `!MD`
text must have the extension `.md` and include files must have the
extension `.mdi`

The include statement supports flags for parsing the include file.
```md
\!!! PATH/FILE.mdi FLAGS
```

**Flags**
* `raw`: the file is included as is without any parsing
* `nometa`: meta data in front matter is skipped during parsing
* `notext`: all Markdown text is skipped during parsing
* `nomarky`: include the `!MD` text without any `!M` processing
* `#+N`: increase the level of ATX headings `#`. The headings are
parsed according to `!P` extensions
([blank_before_header](https://pandoc.org/MANUAL.html#extension-blank_before_header),
[space_in_atx_header](https://pandoc.org/MANUAL.html#extension-space_in_atx_header))
* `>>N`: increase the indentation using `N` tabs
* `>N`: increase the indentation using `N` spaces
* `noref`: do not reference this file as Makefile dependency
* `aux`: reference as Makefile dependency, but do not process

**Example**
```md
\!!! marky.mdi #+2
The file was included: `\!included` and $x=`\!x`$ and $y=`\!y`$.
```

!!! marky.mdi #+2
The file was included: `!included` and $x=`!x`$ and $y=`!y`$.

The file `marky.mdi` was loaded with shifting ATX headings by 2 which
means `##` has been added to the included section. The file contains:
```md
!!! marky.mdi raw >>1
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

The include statement `\!!!` loads and parses an `*.mdi` include file.
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
\!!! include.mdi
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
the root `!MD` document which is processed. However, if a meta data
key is preceeded by `-` the key is not imported into the root document.
All `yaml` meta data keys which start with `-` are exposed to the
python scope and will appear as local variables, but they will not
appear in the meta data of the front matter in the preprocessed
`!MD` text. Given the example above, the resulting meta data in
the front matter of the preprocessed `!MD` text looks as follows.

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
`html` and `pdf` documents the `!MD` link statement is used.
```md
[Link Caption](path/to/file.html)
[Link Caption](path/to/file.pdf)
```

When using relative paths in the URL, the documents can be referenced
according to the directory tree of the source `!M` `!MD` text
`md/*/*.md`. However, the resulting link will be a path relative
to the directory `html/` for `html` documents and relative to `pdf/`
for `pdf` documents. As all `html` and `pdf` documents are kept in
separate directories, one link statement cannot be used for rendering
`html` and `pdf` with consistent paths in the link statement.

By using the `!M` format link statement `.\???`, the file extension
in the links is replaced depending on the output format
resuling in consistent links for `html` and `pdf`
documents. The format link statement can be escaped using `.\\???`.

**Example**
```md
[Link to this Document](marky.\???)
```

[Link to this Document](marky.???)

## Format Codes for `html` and `pdf` Documents {#sec:formcode}

Often when writing markdown for `html` and `pdf` documents, the
format needs to be adjusted according to the format. `!P` `!MD`
already renders all common Markdown into `html` and `pdf`.
`!M` supports format specific tweaking using format codes.

In order to inject format specific code, `html` code or `tex` code
for `pdf` documents, the format codes are used. A format code is
written as `` `\?FMTCODE(ARGS)` `` which is translated in two python
function calls:
1. `FMTCODE_html(ARGS)`: format code for injection of raw `html`
code for rendering `html`-based documents in `!P`.
2. `FMTCODE_pdf(ARGS)`: format code for injection of raw `tex`
code in `pdf`-based documents in `!P`.

During preprocessing, `!M` processes all format codes for each
format `html` and `pdf` and caches the output. Before rendering
the Markdown in one particular format using `!P`, `!M` extracts
the results of the corresponding format codes and skips the others.
Additional `tex` packages have to be included using the meta data
field `header-includes`.

For returning the raw format code, either the `!P1` statement can
be used @sec:mdprint **or** the `return` statement can be used.
If both statements are mixed, the output which had been returned
will be appended to the text generated with the `!P1` statement.

**Example**
```!
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
The output of the format code `\\?test1()` is "`\?test1()`" and
`\\?test2()` is "`\?test2()`" (in HTML it is not empty).
```

The output of the format code `\?test1()` is "`?test1()`" and
`\?test2()` is "`?test2()`" (in HTML it is not empty).

---

# `!M` `!MD` Examples {#sec:examples}

## JavaScript in `html` and Placeholder in `pdf`

When creating `!MD` text for `html` output, the user often wants
interactivity using widgets like sliders, check boxes, drop down boxes
etc. However, when exporting into `pdf` those elements need to be
replaced with non-interactive placeholders. In order to develop a single
`!MD` document, which can be rendered in `html` with interactive
elements and into `pdf` with placeholder, the `!M` format codes can be
used, see @sec:formcode. The following example defines a
`<input type="range">` and two `<spans>` with `id="myval"` and
`id="myres"`, in order to update the value of $y=sin(x)$ in `html`. For
`pdf` output the equation and the value range is shown.

**Example**
```!
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
$x$ and $y$ are related to each other by `\?formula()`.

$x$ must be in the range `\?range()`.
```

$x$ and $y$ are related to each other by `?formula()`.

$x$ must be in the range `?range()`.

## Generate a Figure on-the-fly during Preprocessing

This section illustrates how python modules can be used to create
document content. Document content is placed inside the `data/`
directory of the current project working directory (refer to `!M`
project structure, @sec:project)

![This Figure was generated using `!NU` and
`!PL`.](figure1.png){#fig:figure1}

[`!NU`](https://www.numpy.org) and [`!PL`](https://www.matplotlib.org)
are powerful python modules for mathematical computing and plot
generation. The following example shows how to generate @fig:figure1
using `!NU` and `!PL` and include it into the document.

**Example**

```!
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
![This Figure was generated using `!NU`
and `!PL`.](figure1.png){#fig:figure1}
```

## Generate a Sequence of Figures on-the-fly

This section illustrates how a sequence of complex figures can be
generated using `!NU` and `!PL` and how the figures are formatted
using python and referenced using `!M`.

Suppose one experiment which can be run in four different setups with
different values for $\lambda=$
`!", ".join(["(%d) $%.2f$nm"%(k, 125.33*k) for k in range(1, 5)])`.
Each run of the experiment using setup (1)--(4), two additional
parameters $\varepsilon$ and $\alpha$ are varried between
$10.2\ldots30.6\%$ and $0.1\ldots0.3$Hz respectively.

The results of the experiments for the setups (1)--(4) are summarized
in the @fig:figure2_1, !@fig:figure2_2, !@fig:figure2_3 and
!@fig:figure2_4.

**Example**

```!
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

---

*Thanks for reading, please try `marky`.*

---

# References
