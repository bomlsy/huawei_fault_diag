function resetbutton()
{
$('#btn_text').hide();
$('#btn_file').show();
$('#modal_addmod_file').show();
$('#modal_addmod_text').hide();
}



function init_chart(msgs)
{
	var mod_all = JSON.parse(msgs);

	var html='';

	for (var st in mod_all)
	{

		var modname = mod_all[st].module;
		var modcontent = mod_all[st].content;
		var modarg = mod_all[st].argument;
		var moddesc = mod_all[st].description;
		// rand
		var randid = "";
		var randpoll = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
		for(var i = 0; i < 16; i++){
		    randid += randpoll.charAt(Math.floor(Math.random() * randpoll.length));
		}

		html += '<div class="panel panel-default">\
					<div class="panel-heading cgroupi" data-toggle="collapse" data-parent="#accordion" href="#'+randid+'" class="collapsed" aria-expanded="false">\
                        <span class="panel-title"> ' + modname + ' </span>\
						<div class="float-md-right"><button class="flat-button small red" onclick=delete_mod(\''+ modname +'\')><span class="fa fa-close"></span> Del</button></div>\
                    </div>\
                    <div id="'+randid+'" class="panel-collapse collapse" aria-expanded="false">\
                    	<div class="panel-body info-area">\
							<h6>Default Arguments: ' + modarg +  '</h6>\
							<pre>'+moddesc+'</pre>\
		                    <div class="panel panel-default">\
								<div class="panel-heading cgroupi" data-toggle="collapse" data-parent="#accordion" href="#'+randid+'_1" class="collapsed" aria-expanded="false">\
									<span class="panel-title">content</span>\
			                    </div>\
			                    <div id="'+randid+'_1" class="panel-collapse collapse" aria-expanded="false">\
			                    	<div class="panel-body code-area">\
										<pre>'  + modcontent +'</pre>\
			                    	</div>\
			                    </div>\
			                </div>\
                    	</div>\
                    </div>\
                </div>';

	}
	$('#mod_list').html(html);
}




function add_mod()
{
	var savename = "";
	var modfilecontent = $('#modal_addmod_text').val();

	if($('#btn_file').is(':visible'))
	{
		if($('modal_addmod_name').val() == "")
			savename = $('#modal_addmod_name').attr('placeholder');
		else
			savename = $('#modal_addmod_name').val();
	}
	else
	{
		if($('modal_addmod_name').val() == "") 
			{addlog('Module file name is not specified.');return;}
		else
			savename = $('#modal_addmod_name').val();
	}

	if(modfilecontent == "") {addlog('Module file content is empty.');return;}

	var postdata = {"module": savename,
	"content":modfilecontent,
	"description": $('#modal_addmod_desc').val(),
	"argument": $('#modal_addmod_arg').val(),
	};

	$.post('/module/add', JSON.stringify(postdata) ,function(m){addlog(JSON.parse(m).msg);load_mods();});

}

function delete_mod(modname)
{
	$.get('/module/delete/'+modname,function(m){addlog(JSON.parse(m).msg);load_mods();});
}


function load_mods(){
	$.get('/module/get',function(m){init_chart(m);})
}

// Initialization Begin

load_mods();


$(document).on({ 
    dragleave:function(e){    //拖离 
        e.preventDefault(); 
    }, 
    drop:function(e){  //拖后放 
        e.preventDefault(); 
    }, 
    dragenter:function(e){    //拖进 
        e.preventDefault(); 
    }, 
    dragover:function(e){    //拖来拖去 
        e.preventDefault(); 
    } 
}); 


var box = document.getElementById('modal_addmod_file'); //拖拽区域 
box.addEventListener("drop",function(e){ 
    e.preventDefault(); //取消默认浏览器拖拽效果 
    var fileList = e.dataTransfer.files; //获取文件对象 
    //检测是否是拖拽文件到页面的操作 
    if(fileList.length == 0){ 
        return false; 
    }

    $('#modal_addmod_name').val(fileList[0].name);
    $('#modal_addmod_name').attr('placeholder',fileList[0].name);

    var reader = new FileReader();
    reader.readAsText(fileList[0]);
    reader.onload = function (e) {
        var result = reader.result;
		$('#modal_addmod_text').show();
		$('#modal_addmod_text').val(result);
    }


},false); 
