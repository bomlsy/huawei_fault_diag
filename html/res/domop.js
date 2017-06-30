window.onload = function () {
    var i = getCookie('mainpage');
    var a = $('#main_nav').children('li').eq(i - 1);
    a.children('a').click();
    addlog('系统已启动');

}


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
    for (var i of [1, 2, 3, 4]) {
        if (index_of_sw == i)
            $('#main-div-' + i).show();
        else
            $('#main-div-' + i).hide();
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
        uielem.next().children('tbody').children('tr').show();
    }
    else if (_target == 'Alert') {
        uielem.next().children('tbody').children('tr').each(
            function () {
                if ($(this).hasClass('danger'))
                    $(this).show()
                else
                    $(this).hide();
            })
    }
    else if (_target == 'Warning') {
        uielem.next().children('tbody').children('tr').each(
            function () {
                if ($(this).hasClass('warning'))
                    $(this).show();
                else
                    $(this).hide();
            })
    }
}