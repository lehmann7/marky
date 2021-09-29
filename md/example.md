---
title: "`marky` Example"
date: Date
author: Name
link-citations: true
bibliography: data/marky.bib
header-includes--pdf: >
   \hypersetup{colorlinks=false,
   allbordercolors={0 0 0},
   pdfborderstyle={/S/U/W 1}}
header-includes--html: >
   <style>* { box-sizing: border-box; }</style>
xnos-cleveref: true
xnos-capitalise: true
fontsize: 11pt

---

> **Abstract** -- This is a `marky` example document for
> illustrating `marky` markup. The `marky` source code of this
> document can be read [here](example-src.???).
> For more information please refer to the
> [`marky` repository](https://github.com/lehmann7/marky),
> [`marky` documentation](marky.???) or the
> [`marky` quickstart](quickstart.???).

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

```!
	import math
	def list_and(l):
		return ", ".join(str(i) for i in l[:-1]) + " and " + str(l[-1])

	x = 2
	y = math.sqrt(x)
```

**Hidden Code, Executed**

```!!
	print("Hello Console!")
```

**Displayed Code, Not Executed**

```python
	x = 3
```

**Inline Formatted Output**

The square root of $x=`!x`$ is `!y:.3f`.

**Inline Expression**

The first ten numbers are `!list_and(range(10))`.

**Format Links**

```md
[Link to document](file.\???)
```

will be proprocessed into the following text:
* for `html`: `[Link to document](file.html)`
* for `pdf`: `[Link to document](file.pdf)`

[Link to this document](example.???)

**Format Codes**

```!
	def html_FMTCODE(): return "H<sup>T</sup><sub>M</sub>L"
	def pdf_FMTCODE(): return "\LaTeX"
```

This is a `?_FMTCODE()` document.

---

*Thanks for reading, please try `marky`.*

---

# References {-}
