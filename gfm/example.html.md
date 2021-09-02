---
author: Name
bibliography: marky.bib
date: Date
fontsize: 11pt
header-includes: '<style>* { box-sizing: border-box; }</style>

  '
link-citations: true
title: '`marky` Example'
xnos-capitalise: true
xnos-cleveref: true

---

---

> **Abstract** -- This is a `marky` example document for
> illustrating `marky` markup. The `marky` source code of this
> document can be read [here](examplesource.html).
> For documentation and download please refer to the
> [`marky` repository](https://github.com/lehmann7/marky).

---

# Referenced Section {#sec:label}

This is a reference to @sec:label.

![This is the caption](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==){#fig:label}

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

# `marky` Markup for Execution of Embedded Python Code

**Displayed Code, Executed**

```python
	import math
	def list_and(l):
		return ", ".join(str(i) for i in l[:-1]) + " and " + str(l[-1])

	x = 2
	y = math.sqrt(x)
```

**Hidden Code, Executed**


**Displayed Code, Not Executed**

```python
	x = 3
```

**Inline Formatted Output**

The square root of $x=2$ is 1.414.

**Inline Expression**

The first ten numbers are 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9.

**Format Links**

```md
[Link to document](file.???)
```

will be proprocessed into the following text:
* for `html`: `[Link to document](file.html)`
* for `pdf`: `[Link to document](file.pdf)`

[Link to this document](example.html)

**Format Codes**

```python
	def FMTCODE_html(): return "H<sup>T</sup><sub>M</sub>L"
	def FMTCODE_pdf(): return "\LaTeX"
```

This is a `.html` document and the format code returns: H<sup>T</sup><sub>M</sub>L.

---

*Thanks for reading, please try `marky`.*

---

# References {-}
