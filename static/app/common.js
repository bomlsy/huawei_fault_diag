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
                if(nsu == 'all'){
                    nodeset.clear();
                }else{
                    if(nsu.indexOf('-') != -1){
                        var nodes_range = nsu.split('-');
                        if(nodes_range.length == 2){

    console.log(nodes_range[0],nodes_range[1]);
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
                if(nsu == 'all'){
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
        var nodearr = [];
        nodeset.forEach( function(item,sitem,s) {
            if($.inArray(item, nodes_id) != -1)
                nodearr.push(item);
        });

    return nodearr;

}