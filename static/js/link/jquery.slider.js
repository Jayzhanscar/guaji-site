!(function($){
    $.fn.extend({
        slider:function(sibling){
            sibling.first().after("<li id='bgli'></li>")

            $(this).hover(function(){
                var nowleft = $(this).position().left;
                var bjlileft = $("#bgli").position().left;
                if(nowleft>bjlileft){
                    $("#bgli").stop().animate({left:nowleft+20
                    },300,function(){
                        $("#bgli").stop().animate({left:nowleft},100)
                    })
                }else{
                    $("#bgli").stop().animate({left:nowleft-20
                    },300,function(){
                        $("#bgli").stop().animate({left:nowleft},100)
                    })
                }



            },function(){
                return false;
            })
        }
    })
})(jQuery);