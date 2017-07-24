var nodes_id=[];
var modal_node=null;

var sync_on = true;
var chart_inited = false;



function addlog(logcontent) {
    var time = new Date;
    var hour = time.getHours();
    if (hour < 10) hour = '0' + hour;
    var minute = time.getMinutes();
    if (minute < 10) minute = '0' + minute;
    var second = time.getSeconds();
    if (second < 10) second = '0' + second;
    time = '[' + hour + ':' + minute + ':' + second + '] ';
    $('#logarea').val( time + logcontent + '\n' + $('#logarea').val());
    $('#logarea').scrollTop(1000000);
}


function connect(btn,nodeid)
{
    btn.className="flat-button yellow";
    btn.innerHTML='<span class="fa fa-power-off"></span>Pending';
    $(btn).removeAttr("onclick");
    $.get('/node/connect/'+nodeid,function(msg){addlog(JSON.parse(msg).msg);})
}
function disconnect(btn,nodeid)
{
    btn.className="flat-button yellow";
    btn.innerHTML='<span class="fa fa-power-off"></span>Pending';
    $(btn).removeAttr("onclick");
    $.get('/node/disconnect/'+nodeid,function(msg){addlog(JSON.parse(msg).msg);})
}

function btn_conf(nodeid)
{
    $.get('/node/get/'+nodeid+'?detail',function(jmsg){

        var node=JSON.parse(jmsg);

        modal_node = node;

		var nodeid = node.id;
		var status = node.status;

		var lastmsg="",buttonclass="",buttontext="",rowclass="",btn_onclick="";
	    switch (status) {
	        case 1:
	            buttontext = "Online";
	            buttonclass = "flat-button";
	            btn_onclick = "disconnect(this,"+ nodeid +")";
	            lastmsg = "Connected";
	            break;
	        case 0:
	            buttonclass = "flat-button yellow";
	            buttontext = "Pending";
	            lastmsg = "SSH connecting";
	            break;
	        case -1:
	            buttontext = "Offline";
	            buttonclass = "flat-button gray";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Disconnected";
	            break;
	        case -2:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "flat-button red";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Access Error";
	            break;
	        case -3:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "flat-button red";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Node Timeout";
	            break;
	        default:
	            return;
	            break;
	    }
	    var btn_status = '<button class="'+ buttonclass +'"  onclick="'+ btn_onclick +'"><span class="fa fa-power-off"></span>'+ buttontext +'</button>';
	    $('#modal_status').html(btn_status);

	    $('#modal_nodeid').html(nodeid);
	    $('#modal_hostname').html(node.hostname);
	    $('#modal_username').val(node.username);
	    $('#modal_address').val(node.address);
	    $('#modal_port').val(node.port);
	    var btnauth = '';
	    if(node.authtype=="key")
        {
            chooseauthtype(true);
            btnauth='<button class="help" onclick="chooseauthtype(false)"><span class="fa fa-file"></span></button>';
        }else
        {
            chooseauthtype(false);
            btnauth='<button class="help" onclick="chooseauthtype(true)"><span class="fa fa-font"></span></button>';
        }

	    $('#btn_authtype').html(btnauth);

    });
}

function chooseauthtype(tf)
{
    var btnauth = '';
    if(tf)
    {
        btnauth='<button class="help" onclick="chooseauthtype(false)"><span class="fa fa-file"></span></button>';
        $('#keyfileselect').get(0).hidden = false;
        $('#passwordtext').get(0).hidden = true;
    }else
    {
        btnauth='<button class="help" onclick="chooseauthtype(true)"><span class="fa fa-font"></span></button>';
        $('#keyfileselect').get(0).hidden = true;
        $('#passwordtext').get(0).hidden = false;
    }
	$('#btn_authtype').html(btnauth);
}


function generate_li(node)
{
	var nodeid = node.id;
	var hostname = node.hostname;
	var address = node.address;
	var status = node.status;

	nodes_id.push(nodeid);

	var lastmsg="",buttonclass="",buttontext="",rowclass="",btn_onclick="";
		switch (status) {
	    case 1:
	        buttontext = "Online";
	        buttonclass = "flat-button";
	        btn_onclick = "disconnect(this,"+ nodeid +")";
	        lastmsg = "Connected";
	        break;
	    case 0:
	        buttonclass = "flat-button yellow";
	        buttontext = "Pending";
	        lastmsg = "SSH connecting";
	        break;
	    case -1:
	        buttontext = "Offline";
	        buttonclass = "flat-button gray";
	        btn_onclick = "connect(this,"+ nodeid +")";
	        lastmsg = "Disconnected";
	        break;
	    case -2:
	        rowclass="danger";
	        buttontext = "Offline";
	        buttonclass = "flat-button red";
	        btn_onclick = "connect(this,"+ nodeid +")";
	        lastmsg = "Access Error";
	        break;
	    case -3:
	        rowclass="danger";
	        buttontext = "Offline";
	        buttonclass = "flat-button red";
	        btn_onclick = "connect(this,"+ nodeid +")";
	        lastmsg = "Node Timeout";
	        break;
	    default:
	        return;
	        break;
	}
	node.className=rowclass;
	var btn_status = '<button class="'+ buttonclass +'"  onclick="'+ btn_onclick +'"><span class="fa fa-power-off"></span>'+ buttontext +'</button>';
	var btn_conf = '<button data-toggle="modal" data-target="#modal_nodedetail" class="help" onclick="btn_conf('+ nodeid +')"><span class="fa fa-cog"></span></button>';

	addlog('#'+nodeid+' '+lastmsg);

	var html = '<div class="row">\
			<div class="col-md-1"><input type="checkbox" checked></input>' + '</div>\
			<div class="col-md-2">#' + nodeid+ '</div>\
			<div class="col-md-3">'+ hostname + '</div>\
			<div class="col-md-3">'+ address + '</div>\
			<div class="col-md-2">'+ btn_status + '</div>\
			<div class="col-md-1">'+ btn_conf + '</div>\
			</div>';

	return html;

}

function init_chart(msgs)
{
	var status_all = JSON.parse(msgs);

	var html='';

	for (var st in status_all)
	{
		html += '<li id="node_'+ status_all[st].id +'">' + generate_li(status_all[st]) + '</li>' ;
	}
	$('#node_list').html(html);
	chart_inited = true;
}


function update_chart(msgs)
{
	var status_all = JSON.parse(msgs);
	if(status_all.length)
	{
		for (var st in status_all)
		{
			var node = status_all[st];
			var nodeid = node.id;
			var html = generate_li(node);
			$('#node_'+nodeid).html(html);

			if($('#modal_nodeid').text()==nodeid)
	        {
	            $('#modal_status').html($('#node_'+nodeid).find('button.flat-button').parent().html());
	        }
		}
	}
}

function connect_selected()
{
	var selected = NSL(nodes_id ,$('#nsl').val());
	for (var j in selected)
	{
		$.get('/node/connect/'+selected[j],function(m){addlog(JSON.parse(m).msg);});
	}
}

function disconnect_selected()
{
	var selected = NSL(nodes_id ,$('#nsl').val());
	for (var j in selected)
	{
		$.get('/node/disconnect/'+selected[j],function(m){addlog(JSON.parse(m).msg);});
	}
}


function delete_selected()
{
	var selected = NSL(nodes_id ,$('#nsl').val());
	for (var j in selected)
	{
		$.get('/node/delete/'+selected[j],function(m){addlog(JSON.parse(m).msg);});
	}
}


$('#btn_passwd').show();$('#btn_key').hide(); $('#modal_addnode_password').show();$('#modal_addnode_key').hide();
function add_node()
{
	if( $('#keyfileselect').val())
	{
		var key = $('#keyfileselect').val();
	}else {
		var key = "";
	}
	if($('#btn_passwd').is(':visible'))
		var authtype = 'password';
	else
		var authtype = 'key';

	var postdata = {"access" :{
			"address": $('#modal_addnode_address').val(),
			"port": $('#modal_addnode_port').val(),
			"username": $('#modal_addnode_username').val(), 
   			"password": $('#modal_addnode_key').val(), 
			"authtype": authtype ,
			"key": key
		}};

	reload_chart();
	$.post('/node/add', JSON.stringify(postdata),function(m){console.log(m); addlog(m.msg);},'json');
}

function reload_chart()
{
	$.get("/node/get/all?detail",init_chart);
}


function delete_node(btn)
{
	var nodeid = $('#modal_nodeid').text();
	$.get('/node/delete/'+nodeid,function(m){addlog(JSON.parse(m).msg);});
	$('#node_'+nodeid).remove();
}

function update_node(btn)
{
	var nodeid = $('#modal_nodeid').text();
	if( $('#keyfileselect').val())
	{
		var key = $('#keyfileselect').val();
	}else {
		var key = "";
	}

	var postdata = {"access" :{
			"address": $('#modal_address').val(),
			"port": $('#modal_port').val(),
			"username": $('#modal_username').val(), 
   			"password": $('#passwordtext').val(), 
			"authtype": modal_node.authtype ,
			"key": key
		}};

	$('#node_'+nodeid).children().children()[3].innerText = $('#modal_address').val();
	$.post('/node/update/'+nodeid, JSON.stringify(postdata),function(m){console.log(m); addlog(m.msg);},'json');
}




$('#nsl').keyup(function(){
	var selected = NSL(nodes_id ,$('#nsl').val());
	for (var i in nodes_id)
	{
		$('#node_'+nodes_id[i]).find('input').removeAttr('checked');
	}

	for (var j in selected)
	{
		$('#node_'+selected[j]).find('input').attr('checked','');
	}
})


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


$.get("/node/get/all?detail",init_chart);

setInterval(function(){ 
	if(sync_on == false) return;
	if(document.visibilityState == "hidden") return;
	if(chart_inited == false) return;
	$.get("/notification/get/update",update_chart);
},3000);

