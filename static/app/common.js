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
                $('main').animate({'left' : '290px'},{'queue':false});
            }
    	else{
                $(this).addClass('closed');
                $('.sidebar').animate({'left': '-260px'},{'queue':false});
                $('main').animate({'left' : '0px'},{'queue':false}); 
            }
    });
}

