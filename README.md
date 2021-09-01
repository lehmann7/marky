> `marky` is Markdown preprocessor for embedding python code into 
> Markdown documents using `pandoc` as a renderer for `pdf` and `html`.

# `marky`

`marky` markup is compatible with standard Markdown and 
can be read  as-is.
In order to understand the examples and see the complete
`marky` syntax please refer to the following documents:

* [`marky` Quickstart](https://lehmann7.github.io/quickstart.html)
* [`marky` Quickstart Source](https://lehmann7.github.io/quicksource.html)
* [`marky` Example](https://lehmann7.github.io/example.html)
* [`marky` Documentation](https://lehmann7.github.io/marky.html)

---

# Version

This is an early implementation of `marky`. So far, it is only tested on
a linux bash shell. However, `marky` only uses standard tools `make`,
`python` and `pandoc` and it is likely that it will run on a MacOS shell
too. When testing `marky` in another setup, please report issues.

---

# `marky` Markup for Embedding and Execution of Python Code

> For the full documentation of the `marky` markup, please refer to the
> documentation or quickstart above.

`marky` preprocesses Markdown files and executes embedded python code.
After preprocessing, a regular Markdown file is present, which can be
rendered into `html` and `pdf` using `pandoc`.

**Hidden Code, Executed**

```python
	```!
	import math
	print("Hello Console!")
	```
```

**Displayed Code, Executed**

```python
	```?
	def list_and(l):
		return ", ".join(str(i) for i in l[:-1]) + " and " + str(l[-1])

	x = 2
	y = math.sqrt(x)
	```
```

**Inline Formatted Output**

The square root of $x=`` `?x` ``$ is `` `?y:.3f` ``.

**Inline Expression**

The first ten numbers are `` `!list_and(range(10))` ``.

**Format Links**

```md
[Link to document](file.\???)
```

will be proprocessed into the following text:
* when rendering `html`: `[Link to document](file.html)`
* when rendering `pdf`: `[Link to document](file.pdf)`

**Format Codes**

```python
	```?
	def FMTCODE_html(): return "H<sup>T</sup><sub>M</sub>L"
	def FMTCODE_pdf(): return "\LaTeX"
	```
```

The format code is called using `` `?FMTCODE()` ``.


# Install and Render Documentation and Examples

> For the full documentation of the `marky` usage, please refer to the
> documentation or quickstart above.

`marky` is a single-file stand alone script which depends on
`python` (>=3.6), `pandoc` (>=2.11), `pyyaml` and `pandoc-xnos`.

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

**Initialize `marky` Environment**

The `marky` environment is initialized using the following commands.
The `marky` Makefile, documentation and quickstart are unpacked from
the `marky` script file into the current working directory.

```bash
cd $HOME
cd marky
./marky.py --init
WRITE ./md/marky.md
WRITE ./md/marky.mdi
WRITE ./md/quickstart.md
WRITE ./md/quicksource.md
WRITE ./md/example.md
WRITE ./data/marky.bib
USAGE
1. `make help`
2. `make all-html httpd`
3. `make all-pdf`
```

During initialization `marky` creates two directories `md/` and `data/`.
`md/` is the diretory which contains the Markdown text to be rendered
into `html` and `pdf`. `data/` is the resource diretory which contains
scripts, images, videos and other assets.

**Render Documentation and Examples**

If all dependencies have been installed accordingly and the `marky`
environment is initialized, `marky` can be used to render a local
copy of the documentation and the quickstart.

The following commands render the Markdown text of the documentation.

```bash
cd $HOME
cd marky
make all
```

During `make` a new directory `build/` is created, which contains
temporary files (preprocessed Markdown text, linked text for `html`
and `pdf`). The resulting `html` and `pdf` documents are placed inside
`html/` and `pdf/`.

**`marky` Makefile**

The `marky` Makefile coordinates the three steps of the `marky`
document pipeline preprocessing, linking and rendering.
The `marky` Makefile supports several targets for displaying help
or rendering all, multiple or specific documents.

1. `make help`: display help message on the console
2. `make cheat`: display the `marky` markup Cheat Sheet
3. `make scan`: scan for new documents `md/*.md` and update Makefile
4. `make all`: render all documents `md/*.md` into `html` and `pdf`
5. `make all-pdf`: render all documents `md/*.md` into `pdf`
6. `make all-html`: render all documents `md/*.md` into `html`
7. `make httpd`: start python webserver in `html/`
8. `make clean`: remove all files: `build/*`, `pdf/*`, `html/*`

