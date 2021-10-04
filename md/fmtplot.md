---
title: "`fmtplot`: Format Code for Plots in `pdf` and `html` Output"
date: 2021-09-07
author: lehmann7
header-includes--html: >
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.event.drag.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.mousewheel.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.canvaswrapper.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.colorhelpers.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.saturated.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.browser.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.drawSeries.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.uiConstants.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.resize.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.legend.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.navigate.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.hover.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.touch.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.touchNavigate.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.selection.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.symbol.js"></script>
   <script language="javascript" type="text/javascript" src="data/fmtplotjs/jquery.flot.image.js"></script>
   <link rel="stylesheet" type="text/css" href="data/fmtplot.css">
   <script language="javascript" type="text/javascript" src="data/fmtplot.js"></script>
fontsize: 11pt
xnos-cleveref: true
xnos-capitalise: true
fignos-caption-name: Figure

---
!!! ../data/fmtplot.css aux
!!! ../data/fmtplot.js aux
```!!
	import os
	import json
	import matplotlib.pyplot as plt

	class fmtplot_base:
		def setup(self, figid,
			data=None,
			style=None,
			label=None,
			color=None,
			xticks=None
		): pass
		def show(self, figid, caption=None): pass
		def legend(self, figid, caption=None): pass
		def choice(self, figid): pass
		def script(self): pass
		def fix(self, data, style, label, color):
			data = [([0,1],[0, 1])]*len(label) if data is None else data
			style = [("o", 1.)]*len(data) if style is None else style
			label = [None]*len(data) if label is None else label
			color = ["#ff0000"]*len(data) if color is None else color
			return data, style, label, color

	class fmtplot_flot(fmtplot_base):
		markers = {"o":"circle", "s":"square", "D":"diamond", "^":"triangle", "x":"cross", "+":"plus"}
		def __init__(self, aspect=(16, 9), legpos=None, legcols=1):
			self.aspect = str(aspect[0]) + "-" + str(aspect[1])
			self.script_html = ""
			self.legpos = legpos
			self.legcols = legcols

		def style(self, s):
			text = ""
			for i, c in enumerate(s[0]):
				if c in self.markers: text += "points:{show:true,radius:%e,symbol:'%s'}," % (s[i+1]/2, self.markers[c])
				if c == "L": text += "lines:{show:true,lineWidth:%s},"  % s[i+1]
				if c == "B": text += "bars:{show:true,barWidth:%s,align:'center'}," % s[i+1]
			return text

		def jsid(self, htmlid):
			return "flot-" + htmlid.replace("-", "_")

		def jsticks(self, v):
			if v is None:
				return "null"
			t = ",".join(["[%e,'%s']" % (i[0], i[1]) if type(i) is tuple else "%e" % i for i in v])
			return "[" + t + "]"

		def setup(self, htmlid,
			data=None,
			style=None,
			label=None,
			color=None,
			xticks=None
		):
			data, style, label, color = self.fix(data, style, label, color)
			xticks = self.jsticks(xticks)
			jsid = self.jsid(htmlid)
			jsdat = ""
			jscho = ""
			for i, (d, s, l, c) in enumerate(zip(data, style, label, color)):
				jsdat += "{data:[%s]," % ",".join(["[%e,%e]" % (a, b) for a, b in zip(d[0], d[1])])
				if not s is None: jsdat += self.style(s)
				if not l is None: jsdat += "label:'%s'," % l
				if l is None: jsdat += "label:null,"
				if not c is None: jsdat += "color:'%s'," % c
				jsdat += "},"
			legpos = "null" if self.legpos is None else "'%s'" % self.legpos
			self.script_html += f'flot_init("{jsid}", [{jsdat}], {legpos}, {self.legcols}, {xticks});'
			return ___(f'''
				<div class="flot-plot" id="{jsid}-dummy">
				</div>
			''')

		def show(self, htmlid, caption=None):
			caption = "" if caption is None else caption
			colon = ":" if caption != "" else ""
			jsid = self.jsid(htmlid)
			return ___(f'''
				<div id="fig:{htmlid}" class="fignos">
				<figure>
				<div class="flot-{self.aspect}">
				<div class="flot-plot" id="{jsid}">
				</div>
				</div>
				<figcaption>
				<span>{fignos_caption_name} !@fig:{htmlid}{{nolink=True}}:</span> {caption}
				</figcaption>
				</figure>
				</div>
			''')

		def legend(self, htmlid, caption=None):
			caption = "" if caption is None else caption
			colon = ":" if caption != "" else ""
			return ___(f'''
				<div id="fig:{htmlid}-legend" class="fignos">
				<figure>
				<div class="flot-legend" id="{self.jsid(htmlid)}-legend"></div>
				<figcaption>
				<span>{fignos_caption_name} !@fig:{htmlid}-legend{{nolink=True}}:</span> {caption}
				</figcaption>
				</figure>
				</div>
			''')

		def choice(self, htmlid):
			return f'<div class="flot-choice" id="{self.jsid(htmlid)}-choice"></div>'

		def script(self):
			return "\n<script>" + self.script_html + "\n</script>"

	class fmtplot_mplt(fmtplot_base):
		markers = "osD^x+"
		def __init__(self, figdir=".", figsize=(16, 9), figdpi=200, fontsize="11pt", legpos=None, legcols=1):
			self.figdir = figdir
			self.figdpi = figdpi
			self.legcols = legcols
			cm2inch = lambda xy: (xy[0]/2.54, xy[1]/2.54) # convert from cm to inch
			figsize = cm2inch(figsize)
			fontsize = int(fontsize[:-2])
			self.fontsize = fontsize
			self.legshow = not legpos is None
			self.rcParams = {
				'legend.loc': self.legend_loc(legpos),
				'figure.figsize': figsize,
				'legend.fontsize': fontsize,
				'axes.labelsize': fontsize,
				'axes.titlesize': fontsize,
				'xtick.labelsize': fontsize,
				'ytick.labelsize': fontsize,
				'font.family': 'Times New Roman'
			}
			if not os.path.exists("./build/" + self.figdir):
				os.mkdir("./build/" + self.figdir)

		def legend_loc(self, legpos):
			if legpos == "nw": return "upper left"
			if legpos == "ne": return "upper right"
			if legpos == "sw": return "lower left"
			if legpos == "se": return "lower right"
			return "best"

		def export_legend(self, legend, filename, expand=[-5,-5,5,5]):
			fig  = legend.figure
			fig.canvas.draw()
			bbox  = legend.get_window_extent()
			bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
			bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
			fig.savefig(filename, dpi=self.figdpi, bbox_inches=bbox)

		def setup(self, figid,
			data=None,
			style=None,
			label=None,
			color=None,
			xticks=None
		):
			data, style, label, color = self.fix(data, style, label, color)
			marker = "dx*sov^"
			plt.rcParams.update(self.rcParams)
			plt.figure()
			plt.grid()
			plotgrp = list()
			plotlbl = list()
			for n, (d, s, l, c) in enumerate(zip(data, style, label, color)):
				pgroup = list()
				for i, e in enumerate(s[0]):
					if e in self.markers:
						pgroup.append(plt.scatter(d[0], d[1], color=c, marker=e, s=s[i+1]**2))
					if e == "L":
						pgroup.extend(plt.plot(d[0], d[1], color=c, lw=s[i+1]))
					if e == "B":
						pgroup.append(plt.bar(d[0], d[1], color=c, width=min(d[0][0:-1] - d[0][1:])*s[i+1]))
				if not l is None:
					plotgrp.append(tuple(pgroup))
					plotlbl.append(l)
			from matplotlib.legend_handler import HandlerTuple
			if self.legshow:
				if self.rcParams["legend.loc"] == "best":
					legend = plt.legend(plotgrp, label, numpoints=1,
						handler_map={tuple: HandlerTuple(ndivide=None)},
						bbox_to_anchor=(1.05, 0.5), ncol=self.legcols)
					self.export_legend(legend, "./build/" + self.figdir + "/" + figid + "-legend.png")
					legend.remove()
				else:
					plt.legend(plotgrp, label, numpoints=1,
						handler_map={tuple: HandlerTuple(ndivide=None)},
						ncol=self.legcols)
			if not xticks is None:
				plt.xticks(
					[i[0] if type(i) is tuple else i for i in xticks],
					[i[1] if type(i) is tuple else str(i) for i in xticks]
				)
			plt.tight_layout()
			plt.savefig("./build/" + self.figdir + "/" + figid + ".png", dpi=self.figdpi)
			plt.close("all")

		def show(self, figid, caption=None):
			caption = "" if caption is None else caption
			return f'![{caption}]({self.figdir + "/" + figid + ".png"})' + "{#fig:" + figid + "}"

		def legend(self, figid, caption=None):
			caption = "" if caption is None else caption
			return f'![{caption}]({self.figdir + "/" + figid + "-legend.png"})' + "{#fig:" + figid + "-legend}"

	class fmtplot(fmtcode):
		def __init__(self, pdf, html):
			self.pdf = pdf
			self.html = html
			self.reset()
		def data(self, v):
			self.ldata = [] if self.ldata is None else self.ldata
			self.ldata.append(v)
		def label(self, v):
			self.llabel = [] if self.llabel is None else self.llabel
			self.llabel.append(v)
		def color(self, v):
			self.lcolor = [] if self.lcolor is None else self.lcolor
			self.lcolor.append(v)
		def style(self, v):
			self.lstyle = [] if self.lstyle is None else self.lstyle
			self.lstyle.append(v)
		def reset(self):
			self.ldata = None
			self.lstyle = None
			self.llabel = None
			self.lcolor = None
			self.ldata = None
		def plot(self, figid, xticks=None):
			return self.setup(figid, data=self.ldata, style=self.lstyle,
				label=self.llabel, color=self.lcolor, xticks=xticks)

```

---

> **Abstract**-- `fmtplot` is a format code, which produces interactive
> plots for `html` using [`flot`](https://www.flotcharts.org) and static
> plots for `pdf` using [`matplotlib`](https://www.matplotlib.org/).
> Plots are generated using a `marky` format code with a class
> `fmtplot` which implements plot and code generation for both
> cases. The plots which are generated using `fmtplot` can be referenced
> using `pandoc-fignos`.

---

# Prerequirements

In order to the `fmtplot` with `html` output, JavaScript libraries
have to be downloaded using.

```bash
	cd data
	./get_fmtplotjs
```

The script download the following files:
```text
	jquery.canvaswrapper.js
	jquery.colorhelpers.js
	jquery.event.drag.js
	jquery.flot.browser.js
	jquery.flot.drawSeries.js
	jquery.flot.hover.js
	jquery.flot.image.js
	jquery.flot.js
	jquery.flot.legend.js
	jquery.flot.navigate.js
	jquery.flot.resize.js
	jquery.flot.saturated.js
	jquery.flot.selection.js
	jquery.flot.symbol.js
	jquery.flot.touch.js
	jquery.flot.touchNavigate.js
	jquery.flot.uiConstants.js
	jquery.js
	jquery.mousewheel.js
```

---

# Plot Generation

Plots are prepared by calling the class `fmtplot` together with
for the classes `fmtplot_flot` for `html` and `fmtplot_mplt` for `pdf`.
The format code has the following arguments.

```!
	pltdat = fmtplot(
		html=fmtplot_flot(aspect=(16, 9)),
		pdf=fmtplot_mplt(figdir="data", figsize=(16, 9),
			figdpi=200, fontsize="11pt")
	)
```

`aspect` specifies the aspect of a full-width plot for `html` output.
for `pdf` output `figdir` specifies the directory for figure output
`build/<figdir>/`, `fisize` is the size of the figure in `cm` and
`figdpi` and `fontsize` specify DPI number and the font size in `pt`.

In order to init @fig:plot1 for output, the format code

> `setup(figid, data, label, style, color)`

is called with the corresponding arguments.

```python
	_(pltdat.setup("plot1", data=data, label=label,
		style=style, color=color))
```

**Figure Identifier**

`figid` is the identifier of the figure, used for internal referencing
and referencing inside the document. For `pdf` documents the `figid`
also is used for the image filename `build/<figdir>/<figid>.png`.

**Plot Data**

Plot `data` is specified in two sequences containing `x` and `y` values
of point coordinates.
```!
	import numpy as np
	x1 = np.array(range(10)) + 0
	x2 = np.array(range(10)) + 1
	x3 = np.array(range(10)) + 2
	x4 = np.array(range(10)) + 3
	x5 = np.array(range(10)) + 5
	x6 = np.array(range(10)) + 6
	y1 = 40*np.array(range(10)) + 4
	y2 = 30*np.array(range(10)) + 5
	y3 = 20*np.array(range(10)) + 6
	y4 = 10*np.array(range(10)) + 7
	y5 = 10*np.array(range(10)) + 8
	y6 = 10*np.array(range(10)) + 9
	data=[
		(x1, y1),
		(x2, y2),
		(x3, y3),
		(x4, y4),
		(x5, y5),
		(x6, y6)
	]
```

**Plot Labels**

For each data sequence `(x, y)` the label is specified in a list.
A sequence with the label `None` does not appear in the legend and
in the `html` choices.
```!
	label=[
		"Label for (x1, y1)",
		"Label for (x2, y2)",
		"Label for (x3, y3)",
		"Label for (x4, y4)",
		"Label for (x5, y5)",
		"Label for (x6, y6)"
	]
```

**Plot Style**

For each data sequence `(x, y)` the style is specified in a list.
The style for one sequence is a tuple where the first element
is the `styleid` identifier string and the other elements are arguments
`argN` for the `styleid`s in the order of the identifiers in the string.

* `("<styleid>", <arg1>)`
* `("<styleid><styleid>", <arg1>, <arg2>)`

```!
	style=[
		( "^", 11),
		( "o", 11),
		( "s", 11),
		("DL", 11, 2),
		("+L", 11, 2),
		("xB", 11, 0.5)
	]
```

The styles can be combined `Lo`, `^B`, `DLB` in order to annotate
lines and bars with points.
There are as many arguments as chars in the `<styleid>` string.
The following markers `^osD+x` can be used for points in `<styleid>`.
Ths is a subset of the
[`matplotlib` markers](https://matplotlib.org/stable/api/markers_api.html).
which is supported by `flot`. `lines` and `bars` are specified using
`B` and `L`. @tbl:styleid summarizes the style specification.

`<styleid>`|shape (symbol)   |argumet
:---------:|:---------------:|--------
`o`        |points (circle)  |point size in `pt`
`s`        |points (square)  |
`D`        |points (diamond) |
`^`        |points (triangle)|
`x`        |points (cross)   |
`+`        |points (plus)    |
`L`        |lines            |line width in `pt`
`B`        |bars             |relative bar width

Table: List of style identifier strings `<styleid>` and corresponding
arguments. The bar width is specified relative to the minimum distance
between neighbouring `x` points in the data sequence. {#tbl:styleid}

**Plot Color**

For each data sequence `(x, y)` the color for lines and points is
specified in a list.
```!
	color=[
		"#ff0000",
		"#00ff00",
		"#0000ff",
		"#ff00ff",
		"#00ffff",
		"#000000"
	]
```

**Plot Output in Document**

The format code
`show(figid, caption="...")` places @fig:plot1 in the
document using the settings decribed above. Additionally the argument
`caption="..."` is used for setting the figure caption. The figure
@fig:plot1 is referenced by appending `fig:` to the `figid` using
the keyword @`fig:plot1`.

```!
	_(pltdat.setup("plot1", data, label=label, style=style, color=color))
	_(pltdat.show("plot1", """This figure is generated using the format code
	fmtplot.plot(...) with the arguments data, label, style, color
	described above. The figure caption is set using the argument caption.
	"""))
```

---

# Plot Legend

By default `fmtplot` hides the legend. The legend can be placed
outside of the plot in a separate canvas/image or inside the plot.
In order to configure the legend the arguments `legpos` and
`legcols` of the format code constructor are used.
`legcols` specifies the number of columns in the legend and
`legpos` specifies the legend position using the following values.
* `None`: do not show legend
* `"out"`: show legend in separate image using `fmtplot.legend(figid)`
* `"nw"`: show legend in upper left corner
* `"ne"`: show legend in upper right corner
* `"sw"`: show legend in lower left corner
* `"se"`: show legend in lower right corner

**Legend In Plot**

A legend in figures is specified using one of the keywords
`nw`, `ne`, `sw` or `se` for `legpos`. In @fig:plot2, the legendis
placed in the upper right corner using `nw`.
```!
	legin = fmtplot(
		html=fmtplot_flot(legpos="nw", legcols=2),
		pdf=fmtplot_mplt(legpos="nw", legcols=2)
	)
	_(legin.setup("plot2", data, label=label, style=style, color=color))
	_(legin.show("plot2", """This plot is generated with legend inside
	the plot using legpos as one of nw, ne, sw, se and with 2 columns
	using legcols=2."""))
```

**Separate Legend**

A legend in a separate image is specified using the keyword `out`.
@fig:plot3 has a separate legend given in @fig:plot3-legend.
```!
	legout = fmtplot(
		html=fmtplot_flot(legpos="out", legcols=2),
		pdf=fmtplot_mplt(legpos="out", legcols=2)
	)
	_(legout.setup("plot3", data, label=label, style=style, color=color))
	_(legout.show("plot3", """This plot is generated with separate legend
	using legpos=out and with 2 columns using legcols=2."""))
```

**Placement of Separate Legend**

In order to place the separate legend for @fig:plot3, the
`legend(figid, caption="...")`
format code is called. The figure @fig:plot3 is referenced by appending
`fig:` to the `figid` using the keyword @`fig:plot3`. The legend in
@fig:plot3-legend is  referenced by additionally appending
`-legend` using the keyword @`fig:plot3-legend`.
```!
	_(legout.legend("plot3", caption="""This is the legend for @fig:plot3.
	It was placed using the format code fmtplot.legend(figid, caption)."""))
```

---

# Plot Example

```!
	ex = fmtplot(
		html=fmtplot_flot(legpos="out", legcols=2),
		pdf=fmtplot_mplt(legpos="out", legcols=2)
	)
	_(ex.setup(
		"plotex",
		[
			(x1, y1), (x2, y2),
			(x3, y3), (x4, y4)
		],
		label=[
			"Label for (x1, y1)",
			"Label for (x2, y2)",
			"Label for (x3, y3)",
			None
		],
		style=[
			("o", 11),
			("L", 2),
			("LD", 1, 5),
			("Bo", 0.5, 10)
		],
		color=[
			"#ff0000",
			"#00ff00",
			"#0000ff",
			"#000000",
		]
	))
```

```!
	_(ex.show("plotex", """This plot is generated."""))
```

```!
	_(ex.legend("plotex", caption="""This is the legend for @fig:plotex."""))
```

---

# HTML Choice Placement

`html` output supports interactive plots with zooming and paning
and enabling and disabling the plot entities using checkboxes.
The is feature is demonstrated in @fig:plot4. The checkboxes are
located below the figure.
```!
	choice = fmtplot(
		html=fmtplot_flot(legpos="ne", legcols=2),
		pdf=fmtplot_mplt(legpos="ne", legcols=2)
	)
	_(choice.setup("plot4", data, label=label, style=style, color=color))
	_(choice.show("plot4", """This plot is used together with the format
	code fmtplot.choice(figid). For html output, a list of checkboxes is
	generated inside a div-tag. For pdf no output is generated."""))
```

In order to place the choice checkboxes for @fig:plot4, the
`choice(figid)` format code is used. The checkboxes
are placed inside a `<div>` tag.
For `pdf` output there no choice is displayed.

```!
	_(choice.choice("plot4"))
```

---

# Java Script Placement

`html` requires the placement of JavaScript which contains the plot
data and setup code for the plots. The JavaScript is inserted into
`html` documents using the the format code `fmtplot.script()`.
JavaScripts have to be placed at the end of the document.
For `pdf` no output is generated.

```!
	_(pltdat.script())
	_(ex.script())
	_(legin.script())
	_(legout.script())
	_(choice.script())
```

---

*Thanks for reading, please try `fmtplot`.*

---
