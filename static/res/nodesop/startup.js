window.onload = function () {
    var i = getCookie('mainpage');
    var a = $('#main_nav').children('li').eq(i - 1);
    a.children('a').click();
    addlog('System Running');
    $.get('/getnodes',nodestatus_handler);
}

function nodestatus_handler(result)
{

    var msgs=JSON.parse(result);
    if(Array.isArray(msgs))
    {
        if (msgs.length > 0) {
            for (var mi in msgs) {
                var msg = msgs[mi]
                insertNodeStatus(msg);
            }
        }
    }
    else
    {
        insertMsg(msgs);
    }
}


function insertNodeStatus(msg)
{
    var nodeid = msg.id;
    var hostname = msg.hostname;
    var lastmsg="",buttonclass="",buttontext="",rowclass="",btn_onclick="";
    switch (msg.status) {
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
