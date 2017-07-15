//  jQuery must have been load before this file


window.onload = function()
{
    collapsible_sidebar();
}



function collapsible_sidebar()
{
    $("#switch_sidebar").click(function(){
        if($(this).hasClass('closed')){
                $('#sidebar').animate({'left': '0px'},{'queue':false});
                $(this).removeClass('closed');
                $('main').animate({'left' : '260px'},{'queue':false});
                var wid = $('body').width() - 260;
                wid = wid + 'px';
                console.log(wid);
                $('main').animate({'width': wid},{'queue':false});
            }
    	else{
                $(this).addClass('closed');
                $('#sidebar').animate({'left': '-260px'},{'queue':false});
                $('main').animate({'left' : '0px'},{'queue':false}); 
                $('main').animate({'width':'100%'},{'queue':false});
            }
    });
}

