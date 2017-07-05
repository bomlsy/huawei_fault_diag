function addlog(logcontent) {
    var time = new Date;
    var hour = time.getHours();
    if (hour < 10) hour = '0' + hour;
    var minute = time.getMinutes();
    if (minute < 10) minute = '0' + minute;
    var second = time.getSeconds();
    if (second < 10) second = '0' + second;
    time = '[' + hour + ':' + minute + ':' + second + '] ';
    $('#logarea').val($('#logarea').val() + time + logcontent + '\n');
    $('#logarea').scrollTop(1000000);
}


function setCookie(name, value) {
    var exp = new Date();
    exp.setTime(exp.getTime() + 86400000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}


function main_switcher(elem) {
    var lielem = $(elem).parent();
    var uielem = lielem.parent();
    uielem.children('li').removeClass('active');
    lielem.addClass('active');
    var index_of_sw = uielem.children('li').index(lielem);
    index_of_sw++;
    var arr_index=[1, 2, 3];
    for (var i in arr_index) {
        if (index_of_sw == arr_index[i])
            $('#main-div-' + arr_index[i]).show();
        else
            $('#main-div-' + arr_index[i]).hide();
    }
    setCookie('mainpage', index_of_sw);

}

function status_filter(elem) {
    var _target = elem.innerText;
    var lielem = $(elem).parent();
    var uielem = lielem.parent();
    uielem.children('li').removeClass('active');
    lielem.addClass('active');

    if (_target == 'All') {
        $('#table_status').children('tr').show();
    } else if (_target == 'Alert') {
        $('#table_status').children('tr').each(function() {
            if ($(this).hasClass('danger')) $(this).show()
            else $(this).hide();
        })
    } else if (_target == 'Warning') {
        $('#table_status').children('tr').each(function() {
            if ($(this).hasClass('warning')) $(this).show();
            else $(this).hide();
        })
    }
}

function getNodeById(nodeid)
{
    var table_status = document.getElementById('table_status');
    var t_rows = table_status.rows;
    if(t_rows.length>0)
    {
        for (var nodeindex in t_rows) {
            if (t_rows[nodeindex].cells[0].innerHTML == nodeid)
                return t_rows[nodeindex];
        }
    }
    return false;
}


function update_status(nodeid,content)
{
	var node = getNodeById(nodeid);

	if(node)
	{
		node.cells[1].innerHTML=content.hostname;
	    var lastmsg="",buttonclass="",buttontext="",rowclass="",btn_onclick="";
	    switch (content.status) {
	        case 1:
	            buttontext = "Online";
	            buttonclass = "btn btn-success";
	            btn_onclick = "disconnect(this,"+ nodeid +")";
	            lastmsg = "Connected";
	            break;
	        case 0:
	            buttonclass = "btn btn-warning";
	            buttontext = "Pending";
	            lastmsg = "SSH connecting";
	            break;
	        case -1:
	            buttontext = "Offline";
	            buttonclass = "btn btn-sucess";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Disconnected";
	            break;
	        case -2:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Access Error";
	            break;
	        case -3:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Node Timeout";
	            break;
	        default:
	            return;
	            break;
	    }
	    node.className=rowclass;
	    var btn_status = '<button class="'+ buttonclass +'"  onclick="'+ btn_onclick +'"><span class="glyphicon glyphicon-off"></span>'+ buttontext +'</button>';
		node.cells[2].innerHTML=btn_status;
		node.cells[3].innerHTML=lastmsg;

		if($('#modal_nodeid').text()==nodeid)
        {
            $('#modal_status').html(btn_status);
        }

	}
	else
	{
	    var hostname = content.hostname;
	    var lastmsg="",buttonclass="",buttontext="",rowclass="",btn_onclick="";
	    switch (content.status) {
	        case 1:
	            buttontext = "Online";
	            buttonclass = "btn btn-success";
	            btn_onclick = "disconnect(this,"+ nodeid +")";
	            lastmsg = "Connected";
	            break;
	        case 0:
	            buttonclass = "btn btn-warning";
	            buttontext = "Pending";
	            lastmsg = "SSH connecting";
	            break;
	        case -1:
	            buttontext = "Offline";
	            buttonclass = "btn btn-default";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Disconnected";
	            break;
	        case -2:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Access Error";
	            break;
	        case -3:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            lastmsg = "Node Timeout";
	            break;
	        default:
	            return;
	            break;
	    }
   	    var table_status = document.getElementById('table_status');
	    var node_row = document.createElement('tr');
	    node_row.className=rowclass;

	    var cell_nodeid = document.createElement('td');
	    var cell_hostname = document.createElement('td');
	    var cell_lastmsg = document.createElement('td');
	    var cell_status = document.createElement('td');
	    var cell_conf = document.createElement('td');
	    var btn_status = '<button class="'+ buttonclass +'"  onclick="'+ btn_onclick +'"><span class="glyphicon glyphicon-off"></span>'+ buttontext +'</button>';
        var btn_conf = '<button data-toggle="modal" data-target="#modal_nodedetail" class="btn btn-default" onclick="btn_conf('+ nodeid +')"><span class="glyphicon glyphicon-cog"></span></button>';

	    cell_nodeid.innerHTML=nodeid;
	    cell_hostname.innerHTML=hostname;
	    cell_status.innerHTML=btn_status;
	    cell_lastmsg.innerHTML=lastmsg;
	    cell_conf.innerHTML=btn_conf;

	    node_row.appendChild(cell_nodeid);
	    node_row.appendChild(cell_hostname);
	    node_row.appendChild(cell_status);
	    node_row.appendChild(cell_lastmsg);
	    node_row.appendChild(cell_conf);

	    table_status.appendChild(node_row);
	}

    addlog("Node "+ nodeid + ': ' + content.hostname + " " + lastmsg);

}

function btn_conf(nodeid)
{
    $.get('/getnodes?detail=1&node='+nodeid,function(jmsg){
        var msg=JSON.parse(jmsg);
	    var buttonclass="",buttontext="",rowclass="",btn_onclick="";
	    switch (msg.status) {
	        case 1:
	            buttontext = "Online";
	            buttonclass = "btn btn-success";
	            btn_onclick = "disconnect(this,"+ nodeid +")";
	            break;
	        case 0:
	            buttonclass = "btn btn-warning";
	            buttontext = "Pending";
	            break;
	        case -1:
	            buttontext = "Offline";
	            buttonclass = "btn btn-default";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            break;
	        case -2:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            break;
	        case -3:
	            rowclass="danger";
	            buttontext = "Offline";
	            buttonclass = "btn btn-danger";
	            btn_onclick = "connect(this,"+ nodeid +")";
	            break;
	        default:
	            return;
	            break;
	    }
	    var btn_status = '<button class="'+ buttonclass +'"  onclick="'+ btn_onclick +'"><span class="glyphicon glyphicon-off"></span>'+ buttontext +'</button>';
	    $('#modal_status').html(btn_status);

	    $('#modal_nodeid').html(nodeid);
	    $('#modal_hostname').html(msg.hostname);
	    $('#modal_username').val(msg.username);
	    $('#modal_address').val(msg.address);
	    $('#modal_port').val(msg.port);
	    var btnauth = '';
	    if(msg.authtype=="key")
        {
            showkeypath(true);
            btnauth='<button class="btn btn-default" onclick="showkeypath(false)"><span class="glyphicon glyphicon-file"></span> KeyFile</button>';
        }else
        {
            showkeypath(false);
            btnauth='<button class="btn btn-default" onclick="showkeypath(true)"><span class="glyphicon glyphicon-font"></span>Password</button>';
        }

	    $('#btn_authtype').html(btnauth);

    });
}

function showkeypath(tf)
{
    var btnauth = '';
    if(tf)
    {
        btnauth='<button class="btn btn-default" onclick="showkeypath(false)"><span class="glyphicon glyphicon-file"></span> KeyFile</button>';
    }else
    {
        btnauth='<button class="btn btn-default" onclick="showkeypath(true)"><span class="glyphicon glyphicon-font"></span>Password</button>';
    }
    $('#keyfilepath').get(0).hidden=!tf;
	$('#btn_authtype').html(btnauth);
}

function connect(btn,nodeid)
{
    btn.className="btn btn-warning";
    btn.innerHTML='<span class="glyphicon glyphicon-off"></span>Pending';
    $.get('/connect?node='+nodeid,function(msg){addlog(JSON.parse(msg).msg);})
}
function disconnect(btn,nodeid)
{
    btn.className="btn btn-warning";
    btn.innerHTML='<span class="glyphicon glyphicon-off"></span>Pending';
    $.get('/disconnect?node='+nodeid,function(msg){addlog(JSON.parse(msg).msg);})
}

function notification_puller()
{
    if(document.hidden)return;  // pause refreshing when window is hidden. HTML5
	$.get('/getnotification',function notification_handler(result){
		var msgs = JSON.parse(result);
		if(msgs.length>0)
		{
            for (var mi in msgs) {
                var msg = msgs[mi];
                if (msg.event == 'update') {
                    update_status(msg.id, msg.content);
                }
                if (msg.event == 'execute_mod') {

                }
                if (msg.event == 'execute_cmd') {

                }
            }
        }
	} );
}




setInterval(notification_puller, 3000);
