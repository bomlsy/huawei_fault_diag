//  jQuery must have been load before this file


window.onload = function()
{
    collapsible_sidebar();
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

