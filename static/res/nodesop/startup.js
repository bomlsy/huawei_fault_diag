window.onload = function () {
    var i = getCookie('mainpage');
    var a = $('#main_nav').children('li').eq(i - 1);
    a.children('a').click();
    addlog('系统已启动');

    $.get('/getnodes',jsonmsghandler);

}


function jsonmsghandler(result)
{
    msg=result.parseJSON();
    if(msg.length)
    {
        for(var m in msg)
        {
            insertMsg(msg[m])
        }
    }
    else
    {
        insertMsg(msg)
    }
}

function insertMsg(msg)
{
       if(msg.status==0)
}
