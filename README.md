> `marky` is Markdown preprocessor allowing to execute embedded python
> code in Markdown documents. After preprocessing, a regular Markdown
> file is present, which is rendered into `html` and `pdf` using
> `pandoc`. `marky` handles all this steps using a Makefile.

# `marky`

`marky` markup is compatible with standard Markdown. `marky` introduces
a simple markup syntax for executing python code embedded in
Markdown text.

In the following a short introduction of `marky` is presented.
In order to understand the complete `marky` features and
syntax please refer to the following documents.

1. *Read the Rendered Documents*
* [`marky` Quickstart](https://lehmann7.github.io/quickstart.html)
* [`marky` Example](https://lehmann7.github.io/example.html)
* [`marky` Documentation](https://lehmann7.github.io/marky.html)
2. *Read the Source Code with `marky` Markup*
* [`marky` Example Source](https://lehmann7.github.io/example-src.html)
* [`marky` Quickstart Source](https://lehmann7.github.io/quick-src.html)
* [`marky` Documentation Source](https://lehmann7.github.io/marky-src.html)

# Features

`marky` introduces a small set of new markup for executing embedded
python code in Markdown documents, which is still compatible with
regular Markdown. Rendering `marky` documents with regular Markdown
results in a formatted document with code snippets included.
When preprocessing the document with `marky` the code snippets are
executed and results are inserted into the Markdown text.

`marky` is implemented according to the
[KISS principle](https://en.wikipedia.org/wiki/KISS_principle) and
introduces the following main features.

1. Code Blocks for embedding python code. Python code is executed
and displayed `!` or executed only `!!`.
```md
	```!
	PYTHON_CODE
	```

	```!!
	PYTHON_CODE
	```
```

2. Inline Code for embedding results of python expressions and
variables into Markdown text using `` `!EXPRESSION:FORMAT` `` and
`` `!VARIABLE:FORMAT` ``.

3. Format dependent insertion of raw `html` and *tex* for `pdf`
using `` `?FORMATCODE()` `` and format dependent links using
`[Link description](file.???)`.

4. Include statement for Markdown text using `!!!`. `marky` keeps
track of Make dependencies.
```md
	!!! file.mdi
```

5. Document meta data in Markdown front matter. This feature is
not explained in the short introduction. Please refer to the `marky`
documentation for explanation.
```md
	---
	META_DATA
	---
	MARKDOWN
```

# Implementation

This is an early implementation of `marky`. It is tested on
a linux bash shell. However, `marky` only uses standard tools `make`,
`python` and `pandoc` and it is likely that it will run on other shells
with the same tools. When testing `marky` in another setup,
please report issues.

# TODO

* reimplement parsing of markup
* better display of traceback for code errors
* implement quite output mode
* implement output mode for showing code output only
* merge meta data for `field`, `field--pdf` and `field--html`

# `marky` Markup for Execution of Embedded Python Code

> For the full documentation of the `marky` markup, please refer to the
> documentation or quickstart, as stated above.

`marky` preprocesses Markdown files and executes embedded python code.
For embedding python code `marky` introduces a simple syntax, which is
compatible with regular Markdown.

**Displayed Code, Executed**

The code fenced by `` ```! `` and `` ``` ``, is executed and displayed
in the document.

```python
	```!
	def list_and(l):
		return ", ".join(str(i) for i in l[:-1]) + " and " + str(l[-1])

	x = 2
	y = math.sqrt(x)
	```
```

**Hidden Code, Executed**

The code fenced by `` ```!! `` and `` ``` ``, is executed but **not**
displayed in the document.

```python
	```!!
	import math
	print("Hello Console!")
	```
```

**Inline Formatted Output**

`marky` can output formatted results of expressions and variables inline
using the following statements.

The square root of x=`` `!x` ``, is `` `!y:.3f` ``.

*Output:*
The square root of x=2, is 1.414.

The first five numbers are `` `!list_and(range(5))` ``.

*Output:*
The first five numbers are 0, 1, 2, 3 and 4.

The `list_and(l)` function is implemented in the python code block
above. The variables `x` and `y` are defined there as well.

**Format Links**

```md
[Link to document](file.\???)
```

will be proprocessed into the following text:
* when rendering `html`: `[Link to document](file.html)`
* when rendering `pdf`: `[Link to document](file.pdf)`

**Format Codes**

```python
	```!
	def FMTCODE_html(): return "H<sup>T</sup><sub>M</sub>L"
	def FMTCODE_pdf(): return "\LaTeX"
	```
```

The format code returns `` `?FMTCODE()` ``.

*Output for `pdf`*:
The format code returns \LaTeX.

*Output for `html`*:
The format code returns H<sup>T</sup><sub>M</sub>L

**Include Statement**

`marky` allows to include other Markdown text using the `!!!` statement.
Please refer to the `marky` documentation for complete description
of the `!!!` statement. During rendering `marky` keeps track of
included files and creates Makefile rules for dependent make.

```md
	!!! file.mdi
```

**Meta Data**

Document meta data can be included in the Markdown front matter.
This feature is not explained in the short introduction.
Please refer to the `marky` documentation for explanation.

```md
	---
	META_DATA
	---
	MARKDOWN
```

**Escape Markup**

The `marky` markup can be escaped. When markup is escaped
`marky` removes the escape sequence and prints out the
unescaped statement.

Markup           |Escape Sequence|Unescaped Sequence
-----------------|---------------|------------------
code block hidden|`` ```\!! ``   |`` ```!! ``
code block shown |`` ```\! ``    |`` ```! ``
inline code      |`` `\!...` ``  |```` `!...` ````
format code      |`` `\?...` ``  |```` `?...` ````
include statement|`\!!!`         |`!!!`
format link      |`.\???`        |`.???`

# Download and Run `marky`

> For the full documentation of the `marky` usage, please refer to the
> documentation or quickstart, as stated above.

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
`html/` and `pdf/`. For rendering the `html` documents, `pandoc`
requires internet access, because java scripts and style sheets are
fetched from content delivery networks.

**`marky` Makefile**

The `marky` Makefile coordinates the three steps of the `marky`
document processing pipeline: preprocessing, linking and rendering.
The `marky` Makefile supports several targets for displaying help
or rendering all, multiple or specific documents.

Target         |Description
---------------|----------------------------------------------------
`make help`    |display help message on the console
`make cheat`   |display the `marky` markup Cheat Sheet
`make scan`    |scan for new documents `md/*.md` and update Makefile
`make all`     |render all documents `md/*.md` into `html` and `pdf`
`make all-pdf` |render all documents `md/*.md` into `pdf/*.pdf`
`make all-html`|render all documents `md/*.md` into `html/*.html`
`make httpd`   |start python webserver in `html/`
`make clean`   |remove all files: `build/*`, `pdf/*`, `html/*`

---

*Thanks for reading, please try `marky`.*
