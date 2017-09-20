var donut_node = null;
var list_connected=[],list_connecting=[],list_disconnected=[],list_accesserror=[],list_timeout=[],list_porterror=[],list_routeerror=[];
var donut_inited = false;
var current_view = 0;

var sync_on = true;

function show_basic_chart(idx)
{
	current_view = idx;
	function change_bg_color(color){
		$('.rectangle-list li').hover( function(){
				console.log(color);
				$(this).css('background-color',color);
			}, function() { $(this).css('background-color','#ddd'); }
		);
	}

	function generate_list_html(list)
	{
		var html = '';
		for (var i=0; i<list.length; i++)
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
			$('#node_list').html(generate_list_html(list_connected));
			change_bg_color('rgba(0, 170, 255, 0.5)');
			break;
		case 1:
			$('#node_list').html(generate_list_html(list_disconnected));
			change_bg_color('rgba(255, 206, 86, 0.5)');
			break;
		case 2:
			$('#node_list').html(generate_list_html(list_connecting));
			change_bg_color('rgba(153, 204, 255, 0.5)');
			break;
		case 3:
			$('#node_list').html(generate_list_html(list_timeout));
			change_bg_color('rgba(204, 104, 6, 0.5)');
			break;
		case 4:
			$('#node_list').html(generate_list_html(list_accesserror));
			change_bg_color('rgba(255, 99, 132, 0.5)');
			break;
		case 5:
			$('#node_list').html(generate_list_html(list_porterror));
			change_bg_color('rgba(102, 102, 102, 0.5)');
			break;
		case 6:
			$('#node_list').html(generate_list_html(list_routeerror));
			change_bg_color('rgba(67, 67, 67, 0.5)');
			break;
		default:
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

	for (var st=0; st<status_all.length; st++)
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
		 		list_accesserror.push(status_all[st]);
		 		break;
		 	case -3:
		 		list_timeout.push(status_all[st]);
		 		break;
		 	case -4:
		 		list_porterror.push(status_all[st]);
		 		break;
		 	case -5:
		 		list_routeerror.push(status_all[st]);
		 		break;
		 	default:
		 		break;
		 } 
	}
	donut_node.data.datasets[0].data=[list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_accesserror.length,list_porterror.length,list_routeerror.length];
	donut_node.update();
	donut_inited = true;
	show_basic_chart(current_view);
}

function update_donut(msgs)
{
	var status_all = JSON.parse(msgs);
	if(status_all.length)
	{
		for (var st=0; st<status_all.length; st++)
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
			 		list_accesserror.push(node);
			 		break;
			 	case -3:
			 		list_timeout.push(node);
			 		break;
			 	case -4:
			 		list_porterror.push(status_all[st]);
			 		break;
			 	case -5:
			 		list_routeerror.push(status_all[st]);
			 		break;
			 	default:
			 		break;
			 } 
		}
		donut_node.data.datasets[0].data=[list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_accesserror.length,list_porterror.length,list_routeerror.length];
		donut_node.update();
		show_basic_chart(current_view);
	}
}


function cleanOldState(nodeid)
{
	for (var idx=0; idx<list_disconnected.length; idx++) if(nodeid == list_disconnected[idx].id) { list_disconnected.splice(idx,1); return; }
	for (var idx=0; idx<list_connecting.length; idx++) if(nodeid == list_connecting[idx].id) { list_connecting.splice(idx,1); return; }
	for (var idx=0; idx<list_timeout.length; idx++) if(nodeid == list_timeout[idx].id) { list_timeout.splice(idx,1); return; }
	for (var idx=0; idx<list_accesserror.length; idx++) if(nodeid == list_accesserror[idx].id) { list_accesserror.splice(idx,1); return; }
	for (var idx=0; idx<list_connected.length; idx++) if(nodeid == list_connected[idx].id) {list_connected.splice(idx,1); return; }
	for (var idx=0; idx<list_porterror.length; idx++) if(nodeid == list_porterror[idx].id) {list_porterror.splice(idx,1); return; }
	for (var idx=0; idx<list_routeerror.length; idx++) if(nodeid == list_routeerror[idx].id) {list_routeerror.splice(idx,1); return; }	
}



// draw --

var node_data = {
		labels: ["Connected", "Disconnected", "Connecting" , "Timeout" ,"Access Error","Port Refused","Unreachable"],
	    datasets: [{
	        data:[list_connected.length, list_disconnected.length, list_connecting.length , list_timeout.length, list_accesserror.length,list_porterror.length,list_routeerror.length],
	        backgroundColor: [
		        'rgba(0, 170, 255, 1)',
		        'rgba(255, 206, 86, 1)',
		        'rgba(153, 204, 255, 1)',
		        'rgba(204, 104, 6, 1)',
		        'rgba(255, 99, 132, 1)',
			'rgba(102, 102, 102, 1)',
			'rgba(67, 67, 67, 1)'
	    ]
	    }]
	};

var node_opt = {
	animation: { animateScale: true},
	onClick : function(event,elem)
	{
		if(elem.length > 0) show_basic_chart(elem[0]._index);
	}
}

var ctx = document.getElementById("node_donut").getContext("2d");

donut_node = new Chart(ctx,{type:"doughnut", data:node_data, options:node_opt});

// -- init draw

$.get("/node/get/all",init_donut);
init_blocks();



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
},2000);

