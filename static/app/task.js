var nodes_id=[];
var nodes_selected_id = [];
var taskmod = "";
var running = false;
var update_fetcher = null;
var update_url = "";
var api_base_url = "";
var mods_info = null;

var task_nodelist=null;

$('#nsl').keyup(function(){
	nodes_selected_id = NSL(nodes_id ,$('#nsl').val());
	for (var i in nodes_id)
	{
		$('#node_'+nodes_id[i]).find('input').removeAttr('checked');
	}

	for (var j in nodes_selected_id)
	{
		$('#node_'+nodes_selected_id[j]).find('input').attr('checked','');
	}
})

function fillin_modoption()
{
	$('#module_select').change(function() {
		for(var i=0; i<mods_info.length;i++)
		{
			if(mods_info[i].module == $('#module_select').val())
			{
				$('#module_argument').val(mods_info[i].argument);
				$('#module_description').text(mods_info[i].description);
			}
		}
	});

	$.get('/module/get',function(m){
		mods_info = JSON.parse(m);
		for(var i=0; i<mods_info.length;i++)
		{
        	$('#module_select').append('<option value="'+ mods_info[i].module + '">'+ mods_info[i].module +'</option>');
		}
		$('#module_argument').val(mods_info[0].argument);
		$('#module_description').text(mods_info[0].description);
	});
}

function generate_li(node)
{
	var html = '';
	var nodeid = node.id;
	var hostname = node.hostname;
	var address = node.address;
	html+='<div class="row">\
			<div class="col-md-1"><input type="checkbox" checked></input>' + '</div><div class="col-md-11" data-toggle="collapse" data-parent="#accordion" href="#task_result_node_'+ nodeid +'" class="collapsed" aria-expanded="false"><div class="row"><div class="col-md-2">#' + nodeid+ '</div><div class="col-md-5">'+ hostname + '</div><div class="col-md-4">'+ address + '</div>\
			</div></div><div id="task_result_node_'+ nodeid +'" class="panel-collapse collapse" aria-expanded="false"><div class="panel-body"><pre></pre></div></div>\
			</div>';
	return html;
}

function init_node(msgs)
{
	var status_all = JSON.parse(msgs);

	var html='';

	for (var st in status_all)
	{
		if(status_all[st].status == 1)
		{
			nodes_id.push(status_all[st].id);
			html += '<li id="node_'+ status_all[st].id +'">' + generate_li(status_all[st]) + '</li>' ;
		}
	}
	$('#node_list').html(html);
}



function switch2(mode)
{
	taskmod = mode;
	switch (taskmod) {
		case 'mod':
			// statements_1
			$('#btn_mod').show();
			$('#div_module').show();
			$('#div_command').hide();
			$('#btn_cmd').hide();
			update_url = "/notification/get/mod";
			api_base_url = "/module/exec/";
			break;
		case 'cmd':
			// statements_1
			$('#btn_mod').hide();
			$('#div_module').hide();
			$('#div_command').show();
			$('#btn_cmd').show();
			update_url = "/notification/get/cmd";
			api_base_url = "/cmd/exec/";
			break;
		default:
			// statements_def
			break;
	}
}



function update_result(msgs)
{
	console.log(msgs);
	var results = JSON.parse(msgs);

	var html='';

	for (var idx in results)
	{
		var res = results[idx];
		var nodeid = res.nodeid;
		var resulttext = res.result;
		var color="";

		task_nodelist.delete(nodeid);
		
		if(resulttext.indexOf("NOTIFICATION_COLOR=RED")!=-1)color = "#FF6384";
		if(resulttext.indexOf("NOTIFICATION_COLOR=BLUE")!=-1)color = "#00AAFF";
		if(resulttext.indexOf("NOTIFICATION_COLOR=GREEN")!=-1)color = "#00FF99";
		if(color=="")color="#ddd";
		$("#node_"+nodeid).hover(function(){$(this).css("background-color",color);},function(){$(this).css("background-color",color);});
		$("#node_"+nodeid).css("background-color",color);
		$('#task_result_node_'+nodeid).find('pre').text(resulttext);
		$('#task_result_node_'+nodeid).css("background-color","#ddd");
		$('#task_result_node_'+nodeid).css("width","100%");

		$("#node_"+nodeid).show();
		if(color!="#ddd") $('#node_'+nodeid).find('.col-md-11').click();

	}
}

function get_selected_ids()
{
	var checkboxes = $('input:checked');
	var res=[]
	for (var i=0;i<checkboxes.length;i++)
	{
		var node_id = $(checkboxes[i]).parent().parent().parent().attr('id');
		res.push(parseInt(node_id.substring(5)));
	}
	return res;
}


function runTask()
{
	function taskbtn_on()
	{
		$('#btn_run').addClass('active');
		$('#btn_run').attr("onclick","");
		$('#btn_run').children('span').removeClass('fa-play');
		$('#btn_run').children('span').addClass('fa-spinner');
		$('#btn_run').children('span').addClass('fa-spin');
	}
	function taskbtn_off()
	{
		$('#btn_run').removeClass('active');
		$('#btn_run').attr("onclick","runTask()");
		$('#btn_run').children('span').removeClass('fa-spinner');
		$('#btn_run').children('span').removeClass('fa-spin');
		$('#btn_run').children('span').addClass('fa-play');
	}

	if(running == false)
	{
		running = true;
		task_nodelist=new Set();
		taskbtn_on();

		update_fetcher = setInterval(function(){ 
			if(document.visibilityState == "hidden") return;
			$.get(update_url , update_result);
			if(task_nodelist.size == 0)taskbtn_off();
		},3000);

		if(taskmod == "mod") 
		{
			var postcontent = $('#module_argument').val() ;
			var modulename = '/'+$('#module_select').val();
		}
		else
		{
			var postcontent = $('#command_content').val();
			var modulename = '';
		}

		var target_node = get_selected_ids();

		for (var i in nodes_id)
		{
			var	nodeid = nodes_id[i];
			$('#node_'+nodeid).hide();
		}

		for (var i in nodes_id)
		{
			var	nodeid = nodes_id[i];
			$('#node_'+nodeid).hide();
			if($.inArray(nodes_id[i], target_node) != -1)
			{
				task_nodelist.add(nodeid);
				$.post(api_base_url+nodeid+modulename, postcontent);
			}
		}
	}else {
		running = false;
		delete task_nodelist;
		clearInterval(update_fetcher);
		taskbtn_off();
	}

}

fillin_modoption();
switch2('mod');
$.get("/node/get/all?detail",init_node);
