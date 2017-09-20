//  jQuery must have been load before this file


Window.onbeforeunload=function(){
    localStorage.setItem("windows",0);
}


window.onload = function()
{

    if(localStorage.getItem('windows') == 1){
        window.close();
    }else{
        localStorage.setItem("windows", 1 );
    }
    
    collapsible_sidebar();
    $(window).resize(function(event) {
        if($(this).hasClass('closed')){
                $('.sidebar').css('left', '-260px');
                $('.container-fluid').css('left' , '0px'); 
                $('.container-fluid').css('width' , '100%');
            }else{
                $('.sidebar').css('left', '0px');
                $('.container-fluid').css('left' , '280px');
                $('.container-fluid').css('width' , ($('body').width()-300)+'px');
            }
    });

    $(document).on("contextmenu",function(e){
            if (e.target.nodeName == 'A') e.preventDefault();
    });

}

function htmlspecialchars(str)    
{    
	var s = "";  
	if (str.length == 0) return "";  
	for   (var i=0; i<str.length; i++)  
	{  
	    switch (str.substr(i,1))  
	    {  
		case "<": s += "&lt;"; break;  
		case ">": s += "&gt;"; break;  
		case "&": s += "&amp;"; break;  
		case " ":  
		    if(str.substr(i + 1, 1) == " "){  
		        s += " &nbsp;";  
		        i++;  
		    } else s += " ";  
		    break;  
		case "\"": s += "&quot;"; break;  
		case "\n": s += "<br>"; break;  
		default: s += str.substr(i,1); break;  
	    }  
	}  
return s;  
}  

function refresh_after(sec)
{
	setTimeout(function(){location.reload(true);},sec*1000);
}

function collapsible_sidebar()
{
    $("#switch_sidebar").click(function(){
        if($(this).hasClass('closed')){
                $(this).removeClass('closed');
                $('.sidebar').animate({'left': '0px'},{'queue':false});
                $('.container-fluid').animate({'left' : '280px'},{'queue':false});
                $('.container-fluid').animate({'width' : $('body').width()-300 },{'queue':false});
            }
    	else{
                $(this).addClass('closed');
                $('.sidebar').animate({'left': '-260px'},{'queue':false});
                $('.container-fluid').animate({'left' : '0px'},{'queue':false}); 
                $('.container-fluid').animate({'width' : '100%'},{'queue':false});
            }
    });
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
    $('#logarea').append( time + logcontent + '\n');
    $('#logarea').scrollTop(1000000);
}



function NSL(nodes_id, nsl_str)
{
    var nodeset = new Set(nodes_id);
    var nsus = nsl_str.toLowerCase().replace(' ','').split(/[,，]/);
    for(var idx=0;idx<nsus.length;idx++)
    {
        var nsu = nsus[idx];
        if(nsu)
        {
            if(nsu[0]=='-'){ // -
                nsu = nsu.substr(1).replace('(','').replace(')','');
                if(nsu == 'all' || nsu == 'a'){
                    nodeset.clear();
                }else{
                    if(nsu.indexOf('-') != -1){
                        var nodes_range = nsu.split('-');
                        if(nodes_range.length == 2){
                            for(var i=parseInt(nodes_range[0]);i<=parseInt(nodes_range[1]);i++){
                                nodeset.delete(i);
                            }
                        }else{
                            continue;
                        }
                    }else {
                        nodeset.delete(parseInt(nsu));
                    }
                }
            }else{ 
                nsu = nsu.replace('+','').replace('(','').replace(')','');
                if(nsu == 'all' || nsu == 'a'){
                    nodeset = new Set(nodes_id);
                }else{
                    if(nsu.indexOf('-') != -1){
                        var nodes_range = nsu.split('-');
                        if(nodes_range.length == 2){
                            for(var i=parseInt(nodes_range[0]);i<=parseInt(nodes_range[1]);i++){
                                nodeset.add(i);
                            }
                        }else{
                            continue;
                        }
                    }else {
                        nodeset.add(parseInt(nsu));
                    }
                }
            }
        }
    }
    var nodearr = new Set();
    nodeset.forEach( function(item) {
        if(nodes_id.has(item))
        nodearr.add(item);
    });

    return nodearr;

}
