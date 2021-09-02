---
title: "`marky` Quickstart"
header-includes--pdf:
   \usepackage{multicol}
   \hypersetup{colorlinks=false,
   allbordercolors={0 0 0},
   pdfborderstyle={/S/U/W 1}}
header-includes--html: >
   <style>* { box-sizing: border-box; }</style>
xnos-cleveref: true
xnos-capitalise: true
fontsize: 11pt

---

---

> **Abstract** -- This is a `marky` quickstart document for
> illustrating `marky` markup using simple examples.
> The `marky` source code of this document can be read
> [here](quick-src.???). For documentation and download
> please refer to the
> [`marky` repository](https://github.com/lehmann7/marky).

---

# Introduction

This is a `marky` quickstart document for illustrating `marky` markup
using simple examples. This document is the rendered version of
the source code presented [here](quick-src.???). The `marky` markup
is compatible with standard Markdown and can be read as-is.
This document represents the output of `marky` after processing
python code, which is embedded into the document itself.
In order to understand the examples and see the complete
`marky` syntax, the source code of this file can be read
[here](quick-src.???). The complete documentation of `marky`
is available [here](marky.???)

---

# Markdown

`marky` is a Markdown preprocessor allowing to transform Markdown
text using python. The preprocessed Markdown text is rendered to `pdf`
and `html` (other formats using `pandoc`). `pandoc` has a powerful set
of Markdown extensions supporting structured writing as well as
bibliography, figure referencing, table referencing, tex-style
equations with referencing etc. (refer to Scientific Writing in
Markdown, [`marky` Documentation](marky.???)).

The rendering of Markdown text into `html` and `pdf` consists of three
steps which are illustrated using the `marky` documentation
`md/marky.md`.

1. *Preprocessing* \
   (process `marky` markup, run code, generate content)
	* Input: `marky` Markdown text: `md/marky.md`
	* Output: pandoc Markdown text: `build/marky.md`
2. *Linking* \
	(apply format specific code for `html` and `pdf`)
	* Input: pandoc Markdown text: `build/marky.md`
	* Output
	1. pandoc Markdown text for `html`: `build/marky.html.md`
	2. pandoc Markdown text for `pdf`: `build/marky.pdf.md`
3. *Rendering* \
   (render `html` and `pdf` document using `pandoc`)
	* Input
	1. pandoc Markdown text for `html`: `build/marky.html.md`
	2. pandoc Markdown text for `pdf`: `build/marky.pdf.md`
	* Output
	1. `html` document: `html/marky.html`
	2. `pdf` document: `pdf/marky.pdf`

The whole process is ecapsulated into a python script and a Makefile.
Rendering documents using `marky` requires to write Markdown text
and run `make all`.

---

# Automated Reporting

Markdown text with embedded code snippets is a powerful paradigm for
automated technical and scientific reporting and possibly other
documents. On one hand data can be organized according to the document
structure using algorithms embedded in the report itself, and on the
other hand the data can be inserted in the report directly from
variables. This elliminates the need for manual copying of data into
the text and allows to update or reproduce the report automatically
for the same and other data. Using the simple `marky` syntax the user
can concentrate on documentation writing from the Markdown perspective
and assist the creation of document content using python code
snippets.

`pandoc` filters (refer to Related Work, [`marky` Documentation](marky.???))
allow transforming the document while rendering it. `pandoc` filters
operate on an internal abstract syntax tree (AST) representation,
therefore the user must express dynamically created document content
as nodes in the format of the AST. `marky` takes a slight different
approach and operates on the Markdown text itself, before it is parsed
and rendered.

Python code is embedded into the document with a simple markup syntax
similar to [Rmarkdown](https://www.rmarkdown.org)
using code blocks and inline expressions. `marky` parses the code,
executes it and writes the results back into the Markdown text. The
code can produce output using algorithms or output formatted string
variables. `marky` also allows for the insertion of format dependent
raw code in `html` and *tex* (for `pdf`  documents).

1. code snippets are embedded into the document text
2. code snippets are executed during preprocessing
3. code produces text for the Markdown document
4. code variables are displayed in the document text
5. format dependent code is applied for `html` and `pdf`

---

# Download and Run `marky`

`marky` is Markdown preprocessor allowing to execute embedded python
code in Markdown documents. After preprocessing, a regular Markdown
file is present, which is rendered into `html` and `pdf` using
`pandoc`. `marky` handles all this steps using a Makefile.
`marky` is a single-file script which depends on `python` (>=3.6),
`pandoc` (>=2.11), `pyyaml` and `pandoc-xnos`.

**Installing Dependencies**

`pandoc` binaries for Debian-based Linux are released
[here](https://github.com/jgm/pandoc/releases).
`pyyaml` is installed using the linux package manager or `pip` and
`pandoc-xnos` consists of the components `fignos`, `secnos`, `eqnos`
and `tablenos` which are installed using `pip`. Depending on the
linux installation maybe `pip3` has to be used.

```bash
pip install pyyaml
pip install pandoc-fignos
pip install pandoc-secnos
pip install pandoc-eqnos
pip install pandoc-tablenos
```

**Download `marky` Script**

`marky` is downloaded using the following commands.

```bash
cd $HOME
git clone https://github.com/lehmann7/marky.git
cd marky
```

Alternatively, marky can be obtained diretly without `git`:

```bash
cd $HOME
mkdir marky
cd marky
wget https://raw.githubusercontent.com/lehmann7/marky/main/marky.py
chmod +x marky.py
```

**Initialize `marky` Environment**

The `marky` environment consists of the Makefile and the documentation.
The `marky` Makefile, documentation and quickstart are unpacked from
the `marky.py` script file into the current working directory.
The `marky` environment is initialized using the following commands.

```bash
cd $HOME
cd marky
./marky.py --init
WRITE ./md/marky.md
WRITE ./md/marky.mdi
WRITE ./md/marky-src.md
WRITE ./md/quickstart.md
WRITE ./md/quick-src.md
WRITE ./md/example.md
WRITE ./md/example-src.md
WRITE ./data/marky.bib
USAGE
1. `make help`
2. `make all-html httpd`
3. `make all-pdf`
```

During initialization `marky` creates two directories `md/` and `data/`.
`md/` is the directory which contains the Markdown text to be rendered
into `html` and `pdf`. `data/` is the resource directory which contains
bibliography, images, videos and other assets.

**Render Documentation and Examples**

If all dependencies have been installed accordingly and the `marky`
environment is initialized, `marky` can be used to render a local
copy of the documentation, the quickstart and the example.

The following commands render the Markdown text of the documentation.

```bash
cd $HOME
cd marky
make all-pdf
make all-html
```

During `make` a new directory `build/` is created, which contains
temporary files (preprocessed Markdown text, linked text for `html`
and `pdf`). The resulting `html` and `pdf` documents are placed inside
`html/` and `pdf/`. For rendering `pdf` a tex environment like
`texlive` needs to be installed. For rendering the `html` documents,
`pandoc` requires internet access, because java scripts and style
sheets are fetched from content delivery networks.

**`marky` Makefile**

The `marky` Makefile coordinates the three steps of the `marky`
document processing pipeline: preprocessing, linking and rendering.
The `marky` Makefile supports several targets for displaying help
or rendering all, multiple or specific documents.

*Makefile Targets*

1. `make help`: display help message on the console
2. `make cheat`: display the `marky` markup Cheat Sheet
3. `make scan`: scan for new documents `md/*.md` and update Makefile
4. `make all`: render all documents `md/*.md` into `html` and `pdf`
5. `make all-pdf`: render all documents `md/*.md` into `pdf`
6. `make all-html`: render all documents `md/*.md` into `html`
7. `make httpd`: start python webserver in `html/`
8. `make clean`: remove all files: `build/*`, `pdf/*`, `html/*`

*Make Single Document*

When running `make all`, `marky` renders all documents, which can
be undesirable if only one particular document shall be rendered.
By `make scan`, `marky` scans the directory `md/*.md` for new Markdown
documents to be processed. For each document, which has been found,
`marky` sets up alias targets in order to debug the preprocessing,
linking and rendering of this document.

Assuming the document `md/marky.md` shall be rendered step by step,
`marky` introduces the following targets.

1. *Preprocessing*: `make md-marky` \
	* `md/marky.md` -> `build/marky.md`
2. *Linking `html`*: `make lhtml-marky` \
	* `build/marky.md` -> `build/marky.html.md`
3. *Linking `pdf`*: `make lpdf-marky` \
	* `build/marky.md` -> `build/marky.pdf.md`
4. *Rendering `html`*: `make html-marky`
	* `build/marky.html.md` -> `html/marky.html`
5. *Rendering `pdf`*: `make pdf-marky`
	* `build/marky.pdf.md` -> `pdf/marky.pdf`

---

# Write A New Document

In order to render a new document the Markdown text needs to be saved
to a file located in `md/example.md` which can be found rendered
[here](example.???). The following Markdown snippet
can be used as a starting point.

```yaml
!!! example.md raw >>1
```

---

# Code Blocks

Code blocks are embedded in Markdown using fenced code using
either the `\!` or `\!!` flag for displayed and hidden code
respectively.

```text
    ```\!
	CODE_BLOCK_SHOWN
    ```

    ```\!!
	CODE_BLOCK_HIDDEN
    ```
```

**Display and Execute Code**

This code block annotated with `!` is displayed and executed.

```!
	import math
	x = math.sqrt(2)
```

**Execute Code without Display**

The code block annotated with `!` is not displayed, but executed.

```!!
	y = x + 1
```

**Display Code but do not Execute**

This code block is displayed as python, but not executed.

```python
	z = 0./0.
```

**Using the Python `import` Statement**

Large code blocks can be imported from python modules and the
`import` statement can be used for loading installed libraries.

```python
	import numpy
	import sys
	sys.path.append(".")
	#import module_in_working_directory
```

---

# Inline Code

Inline statements are directly embedded into the text flow using
expressions and variables with the corresponding
syntax `` `\!EXPRESSION` `` or `` `\!VARIABLE` ``.
The output of variables can be formatted using the
`` `\!VARIABLE[:FORMAT]` `` or `` `\!EXPRESSION[:FORMAT]` ``
statement according to the python operator `{<variable>[:<format>]}`
implemented in the
[`str.format()`](https://docs.python.org/3/library/string.html#formatstrings)
specification and the operator `{<expression>[:<format>]}` implemented in
[`f`-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

**Inline Formatted Output**

The result of $\sqrt{2}$ is:
* unformatted output: `! math.sqrt(2.0)`
* formatted output: `! "%.4f" % math.sqrt(2.0)`

The variable $x$ is
* unformatted output: `! x`
* formatted output: `! x:.4f`

The variable $y=x+1$ is
* unformatted output: `! y`
* formatted output: `! y:.4f`

(The code block for the definition of $y$ is hidden.)

**Inline Expression Output**

```!
	x = list(range(1, 11))
	y = [i*i for i in x]

	def list_str(a):
		return [str(i) for i in a]
	def list_and(a):
		return ", ".join(list_str(a[:-1])) + " and " + str(a[-1])
```

The list can be inserted into the text. The square of the first
`!len(x)` numbers `!list_and(x)` is `!list_and(y)`. Square numbers
are computed according to $y=x^2$.

**Inline Statements in Tables**

```!
	class square:
		def __init__(self):
			self.x = 0
		def get_x(self):
			return self.x
		def next_y(self):
			y = self.x**2
			self.x += 1
			return y
	sq = square()
```

The following table is computed according to $y=x^2$.

x            |y
-------------|--------------
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`
`!sq.get_x()`|`!sq.next_y()`

---

# Generate Markdown Text

Markdown text can be produced algorithmically from a python algorithm
using the `_()` and `__()` function. The `_()` and `__()` function are
special names which are reserved by `marky`. (refer to Generation of
Markdown Text, [`marky` documentation](marky.???) for in-depth
explanation).

## The `_()` Function

 The `_()` function basicly resembled the python `print()` function.
`marky` does not patch the standard `print()` function which still
displays text in the console and not in the Markdown text.
The `_()` function supports appending text to the previous and the next
line of output by using `_` as the fist or last parameter.
1. `_(_, *args   )`: append this output to previous output
2. `_(_, *args, _)`: append to previous and next output
3. `_(   *args, _)`: append next output to this output
4. `_()`: disable append flag

**Monkey Patch `print()` Function**

The `print()` function can be *monkey patched* using the following
statment in order to call the `_()` function instead.

```!
	print("Print", "to",  "console", "!")
	_("Print", "to",  "Markdown", "!")

	print = _ # monkey patch
	print("Print", "to",  "Markdown", "!")
```

**Join Arguments using `sep`**

The signature of the `_()` is `_(*args, sep=" ")`. `sep` is used to
join the arguments `*args` into one string.

```!
	_("The first five natural numbers are:")
	_(1, 2, 3, 4, 5, sep=", ")
```

**Generate a Table with Appending**

The append feature is used to create a table.

```!
	_("Column 1", _)
	_("|Column 2", _)
	_("|Column 3", _)
	_()

	_("|".join(["--------"]*3))

	for i in range(5):
		_("% 8d" % (i*3))
		for j in [1, 2]:
			_(_, "|% 8d" % (i*3+j))
```

The algorithm produces the following Markdown text.

```md
Column 1|Column 2|Column 3
--------|--------|--------
       0|       1|       2
       3|       4|       5
       6|       7|       8
       9|      10|      11
      12|      13|      14
```

## The `__()` Function

Compared to the `_()` function, the `__()` function only takes one
argument and its purpose is to output a formatted paragraph with
indentation. The signature of the `__()` function is `_(arg, crop=True)`.

**Generate a Paragraph with `f`-Strings**

The `__()` function can be combined with triple quoted block strings
and the python 3 `f`-strings or `f"..."` string interpolation, refer to
[`f`-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

```!
	import random
	s = 0
	random.seed(s)
	p = [random.random() for i in range(3)]

	__(f"""
		Parameter one is {p[0]:.3f} and the value depends on the seed
		of the pseudo random number generator, which was chosen
		to be {s}. For the same seed always the same random numbers
		are created. The next two numbers are {p[1]:.3f} and {p[2]:.3f}.
		The sum of the three numbers is {sum(p):.3f} and it is
		{'greater' if sum(p) > 2. else 'lesser or equal'} than two.
	""")
```

**Cropping and Indentation of Output**

Before the text generated by the `__()` function is printed into the
document. The text is cropped according to the leading white space
of the first non-empty line. The leading white space of the first
non-empty line is removed from all other lines of the output.

```!
	__("""
		* List Level 1
			* List Level 2
			* List Level 2
				* List Level 3
			* List Level 2
		* List Level 1
		* List Level 1
	""")
```

The code block produces the following output.

```md
* List Level 1
	* List Level 2
	* List Level 2
		* List Level 3
	* List Level 2
* List Level 1
* List Level 1
```

**Disable Cropping of Output**

The cropping is disabled using the keyword `__(text, crop=False)`.

```!
	__("""
		* List Level 1
	""", crop=True)

	__("""
		* List Level 2
	""", crop=False)
```

The code block produces the following output.

```md
* List Level 1
		* List Level 2
```

---

# Format Dependent Links

When writing several Markdown documents often documents are linked
between each other using the Markdown link statement
`[Link Name](file.html)` or `[Link Name](file.pdf)`.
However, when rendering documents with links into `html` and `pdf`
the file extension often must be adjusted according to the output format.
`marky` supports the `.\???` statement, which will be replaced by
`.html` or `.pdf` depending on the output format.

```md
[Link to document](file.\???)
```

will be proprocessed into the following text:
* for `html`: `[Link to document](file.html)`
* for `pdf`: `[Link to document](file.pdf)`

[Link to this document](quickstart.???)

---

# Format Dependent Code

`pandoc` Markdown allows to write format specific code within Markdown
using `html` and *tex* for `pdf` documents. However, when inserting
raw `html` or raw *tex* code, the document only can be rendered into
`html` or `pdf` accordingly.

`marky` introduces format codes, which are applied during linking
after preprocessing. During linking format specific codes for `html`
and `pdf` are applied in a consistent manner, resulting in documents
with Markdown and `html` or Markdown and *tex* only. Using this
pattern `marky` documents contain regular Markdown, which can be
rendered into `html` and `pdf`, as well as format specific codes
for tweaking or polishing `html` and `pdf` output.

Format codes are specified in code blocks and called using the
inline syntax `` `\?FMTCODE(ARGS)` ``, which is translated into the two
following pyhon function calls.
1. `FMTCODE_html(ARGS)`: called when linked for `html`.
2. `FMTCODE_pdf(ARGS)`: called when linked for `pdf`.

Assuming preprocessing the file `md/marky.md`, linking format codes
results in the two following output files.
1. `build/marky.html.md`: contains output of `html` format codes.
2. `build/marky.pdf.md`: contains output of `pdf` format codes.

**Example Multi-Column Text in `pdf` and `html`**

Defnition of two format codes `mcol_begin` and `mcol_end`, one for the
begin of multi column and another for the end of the multi column
section. The format codes are appended with `_html` and `_pdf`
respectively.

```!
	def mcol_begin_pdf(): return r"\begin{multicols}{2}"
	def mcol_end_pdf(): return r"\end{multicols}"
	def mcol_begin_html(): return r"<div style='column-count: 2;'>"
	def mcol_end_html(): return r"</div>"
```

The `column-count` CSS property requires Internet Explorer>=10,
Firefox>=52, Safari>=9, Opera>=37 or Chrome>=50, refer to
[w3schools](https://www.w3schools.com/css/css3_multiple_columns.asp).
In order to use the `multicol` *tex* package, the statement
`\usepackage{multicol}` has to be included in the yaml meta data
in the front matter of the Markdown document.

`?mcol_begin()`Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
Text Text Text Text Text Text Text Text Text Text Text Text Text
`?mcol_end()`

---

# Include Statement

`marky` allows to include other Markdown text using the `\!!!` statement.
Please refer to the `marky` documentation for complete description
of the `\!!!` statement. During rendering `marky` keeps track of
included files and creates Makefile rules for dependent make.

```md
	!!! file.mdi
```

---

# Meta Data

`marky` supports document meta data in Markdown front matter.
This feature is not explained in the quickstart. Please refer
to the `marky` documentation for explanation.

```md
	---
	META_DATA
	---
	MARKDOWN
```

---

# Escape Markup

The `marky` markup can be escaped. When markup is escaped
`marky` removes the escape sequence and prints out the
unescaped statement.

Markup           |Escape Sequence|Unsecaped Sequence
-----------------|---------------|-----------------
code block hidden|`` ```\\!! ``  |`` ```\!! ``
code block shown |`` ```\\! ``   |`` ```\! ``
inline code      |`` `\\!...` `` |`` `\!...` ``
format code      |`` `\\?...` `` |`` `\?...` ``
include statement|`\\!!!`        |`\!!!`
format link      |`.\\???`       |`.\???`

---

*Thanks for reading, please try `marky`.*
