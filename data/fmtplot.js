function flot_plot(id, data)
{
	if (data) $["plot_" + id] = $.plot("#" + id, data, $["opt_" + id]);
	else $["plot_" + id] = $.plot("#" + id, $["data_" + id], $["opt_" + id]);
}

function flot_init(id, data, lpos, lcols)
{
	$["data_" + id] = data;

	$["opt_" + id] = {
			zoom:{interactive:true},
			pan:{interactive:true,enableTouch:true},
			grid:{hoverable:true,clickable:true},
	};

	if (lpos == null) $["opt_" + id]["legend"] = {show:false};
	else if ("nw ne sw se".indexOf(lpos) > -1) $["opt_" + id]["legend"] = {show:true,position:lpos,noColumns:lcols};
	else $["opt_" + id]["legend"] = {show:true,container:$("#" + id + "-legend").get(0),noColumns:lcols};

	let cc = $("#" + id + "-choice");
	if (cc)
	{
		text = "";
		$.each($["data_" + id], function(key, val) {
			cc.append("<input type='checkbox' name='" + id + "-" + key +
			"' checked='checked' id='" + id + "-" + key + "'></input>" +
			"<label for='" + id + "-" + key + "'>" + val.label + "</label>");
		});
		cc.find("input").click(function () { flot_choice(id); });
	}

	flot_plot(id);
}

function flot_choice(id)
{
	let data = $["data_" + id];
	let newd = [];
	let cc = $("#" + id + "-choice");
	cc.find("input:checked").each(function () {
		let key = $(this).attr("name").split("-").at(-1);
		if (key && data[key]) newd.push(data[key]);
	});
	if (newd.length > 0) flot_plot(id, newd);
}

//~ function plotAccordingToChoices(htmlid) {
	//~ let data = [];
	//~ var choiceContainer = $("#choices");
	//~ choiceContainer.find("input").click(plotAccordingToChoices);
	//~ choiceContainer.find("input:checked").each(function () {
		//~ var key = $(this).attr("name");
		//~ if (key && datasets[key]) {
			//~ data.push(datasets[key]);
		//~ }
	//~ });

	//~ if (data.length > 0) {
		//~ $.plot("#placeholder", data, {
			//~ legend: {
				//~ show: true
			//~ },
			//~ yaxis: {
				//~ min: 0
			//~ },
			//~ xaxis: {
				//~ tickDecimals: 0
			//~ }
		//~ });
	//~ }
//~ }
