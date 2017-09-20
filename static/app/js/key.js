function resetbutton()
{
$('#btn_text').hide();
$('#btn_key').show();
$('#modal_addkey_file').show();
$('#modal_addkey_text').hide();
}



function init_chart(msgs)
{
	var key_all = JSON.parse(msgs);

	var html='';

	for (var st=0; st<key_all.length; st++)
	{

		var keyname = key_all[st].key;
		var keycontent = key_all[st].content;
		// rand
		var randid = "";
		var randpoll = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
		for(var i = 0; i < 16; i++){
		    randid += randpoll.charAt(Math.floor(Math.random() * randpoll.length));
		}

		html += '<div class="panel panel-default">\
					<div class="panel-heading cgroupi"  data-toggle="collapse" data-parent="#accordion" href="#'+randid+'" class="collapsed" aria-expanded="false">\
                        <span class="panel-title"> ' + keyname + ' </span>\
						<div class="float-md-right"><button class="flat-button small red" onclick=delete_key(\''+ htmlspecialchars(keyname) +'\')><span class="fa fa-close"></span> Del</button></div>\
                    </div><div id="'+randid+'" class="panel-collapse collapse" aria-expanded="false"><div class="panel-body code-area"><pre>'  + htmlspecialchars(keycontent) +'</pre></div></div></div>';

	}
	$('#key_list').html(html);
}




function add_key()
{
	var savename = "";
	var keyfilecontent = $('#modal_addkey_text').val();

	if($('#btn_key').is(':visible'))
	{
		if($('modal_addkey_name').val() == "")
			savename = $('#modal_addkey_name').attr('placeholder');
		else
			savename = $('#modal_addkey_name').val();
	}
	else
	{
		if($('modal_addkey_name').val() == "") 
			{addlog('Key file name is not specified.');return;}
		else
			savename = $('#modal_addkey_name').val();
	}

	if(keyfilecontent == "") {addlog('Key file content is empty.');return;}

	$.post('/key/add/' + savename, keyfilecontent ,function(m){addlog(JSON.parse(m).msg);load_keys();});

}

function delete_key(keyname)
{
	$.get('/key/delete/'+keyname,function(m){addlog(JSON.parse(m).msg);load_keys();});
}


function load_keys()
{
	$.get('/key/get',function(m){init_chart(m);})
}

load_keys();


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


var box = document.getElementById('modal_addkey_file'); //拖拽区域 
box.addEventListener("drop",function(e){ 
    e.preventDefault(); //取消默认浏览器拖拽效果 
    var fileList = e.dataTransfer.files; //获取文件对象 
    //检测是否是拖拽文件到页面的操作 
    if(fileList.length == 0){ 
        return false; 
    }

    $('#modal_addkey_name').val(fileList[0].name);
    $('#modal_addkey_name').attr('placeholder',fileList[0].name);

    var reader = new FileReader();
    reader.readAsText(fileList[0]);
    reader.onload = function (e) {
        var result = reader.result;
		$('#modal_addkey_text').show();
		$('#modal_addkey_text').val(result);
    }


},false); 
