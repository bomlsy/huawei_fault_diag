var donut_node = null;
var list_connected=[],list_connecting=[],list_disconnected=[],list_error=[],list_timeout=[];
var donut_inited = false;
var current_view = 0;

var sync_on = true;

function show_basic_list(idx)
{
	current_view = idx;
	function change_bg_color(color){$('.rectangle-list li').hover(function(){$(this).css('background',color);}, function() {$(this).css('background','#ddd');});}

	function generate_list_html(list)
	{
		var html = '';
		for (var i in list)
		{

			var nodeid = list[i].id;
			var hostname = list[i].hostname;
			var address = list[i].address;
			html += '<li><div class="row"><div class="col-md-2">#' + nodeid+ '</div><div class="col-md-5">'+ hostname + '</div><div class="col-md-5">'+ address + '</div></div></li>';
		}
		return html;
	}
	
	switch(idx)
 	{
		case 0:
			change_bg_color('#00AAFF');
			$('#node_list').html(generate_list_html(list_connected));
			break;
		case 1:
			change_bg_color('#FFCE56');
			$('#node_list').html(generate_list_html(list_disconnected));
			break;
		case 2:
			change_bg_color('#99CCFF');
			$('#node_list').html(generate_list_html(list_connecting));
			break;
		case 3:
			change_bg_color('#CC6806');
			$('#node_list').html(generate_list_html(list_timeout));
			break;
		case 4:
			change_bg_color('#FF6384');
			$('#node_list').html(generate_list_html(list_error));
			break;

		default:
			// statements_def
			break;
	}

}


function init_blocks()
{
	$.get("/node/get/all",function(result){$('#node_sum').text(JSON.parse(result).length);});
	$.get("/module/get",function(result){$('#mod_sum').text(JSON.parse(result).length);});
	$.get("/key/get",function(result){$('#key_sum').text(JSON.parse(result).length);});
}

function init_donut(msgs)
{
	var status_all = JSON.parse(msgs);

	for (var st in status_all)
	{
		switch (status_all[st].status) {

			case 1:
		 		list_connected.push(status_all[st]);
		 		break;
		 	case 0:
		 		list_connecting.push(status_all[st]);
		 		break;
		 	case -1:
		 		list_disconnected.push(status_all[st]);
		 		break;
		 	case -2:
		 		list_error.push(status_all[st]);
		 		break;
		 	case -3:
		 		list_timeout.push(status_all[st]);
		 		break;
		 	default:
		 		break;
		 } 
	}
	donut_node.data.datasets[0].data=[list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_error.length];
	donut_node.update();
	donut_inited = true;
	show_basic_list(current_view);
}

function update_donut(msgs)
{
	var status_all = JSON.parse(msgs);
	for (var st in status_all)
	{
		var node = status_all[st];
		cleanOldState(node.id);
		switch (node.status) {
			case 1:
		 		list_connected.push(node);
		 		break;
		 	case 0:
		 		list_connecting.push(node);
		 		break;
		 	case -1:
		 		list_disconnected.push(node);
		 		break;
		 	case -2:
		 		list_error.push(node);
		 		break;
		 	case -3:
		 		list_timeout.push(node);
		 		break;
		 	default:
		 		break;
		 } 
	}
	donut_node.data.datasets[0].data=[list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_error.length];
	donut_node.update();
	show_basic_list(current_view);
}


function cleanOldState(nodeid)
{
	for(var idx in list_disconnected) if(nodeid == list_disconnected[idx].id) { list_disconnected.splice(idx,1); return; }
	for(var idx in list_connecting) if(nodeid == list_connecting[idx].id) { list_connecting.splice(idx,1); return; }
	for(var idx in list_timeout) if(nodeid == list_timeout[idx].id) { list_timeout.splice(idx,1); return; }
	for(var idx in list_error) if(nodeid == list_error[idx].id) { list_error.splice(idx,1); return; }
	for(var idx in list_connected) if(nodeid == list_connected[idx].id) {list_connected.splice(idx,1); return; }
}

// draw --

var node_data = {
		labels: ["Connected", "Disconnected", "Connecting" , "Timeout" ,"Access Error"],
	    datasets: [{
	        data: [list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_error.length],
	        backgroundColor: [
		        'rgba(0, 170, 255, 1)',
		        'rgba(255, 206, 86, 1)',
		        'rgba(153, 204, 255, 1)',
		        'rgba(204, 104, 6, 1)',
		        'rgba(255, 99, 132, 1)',
	    ]
	    }]
	};

var node_opt = {
	animation: { animateScale: true},
	onClick : function(event,elem)
	{
		if(elem.length > 0) show_basic_list(elem[0]._index);
	}
}

var ctx = document.getElementById("node_donut").getContext("2d");

donut_node = new Chart(ctx,{type:"doughnut", data:node_data, options:node_opt});

// -- init draw

$.get("/node/get/all",init_donut);
init_blocks();


// Scrollable area size

$('canvas').on('resize',function(){ 
	$('.rectangle-list').height($('canvas').height());
});



// sync button

$('#btn_sync').click(function(event) {
	if ($(this).hasClass('active')){
		$(this).removeClass('active');
		$(this).children('span').removeClass('fa-spin');
		sync_on = false;
	} else {
		$(this).addClass('active');
		$(this).children('span').addClass('fa-spin');
		sync_on = true;
	}
});


// sync

setInterval(function(){ 
	if(sync_on == false) return;
	if(document.visibilityState == "hidden") return;
	if(donut_inited = false) return;
	$.get("/notification/get/update",update_donut);
},3000);

