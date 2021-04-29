$(".p1, .l1").hover(function(){
    $(this).css("color", "rgb(100, 71, 7)");
    }, function(){
    $(this).css("color", "rgb(130, 130, 221)");
});  

$(".inner_p, .list_p").hover(function(){
    $(this).css("color", "rgb(100, 71, 7)");
    }, function(){
    $(this).css("color", "rgb(9, 50, 53)");
    
});  

$(".check_r").hover(function(){
    $(this).css("color", "rgb(100, 71, 7)");
    }, function(){
    $(this).css("color", "rgb(9, 50, 53)");
    
}); 

$(".ls_p").hover(function(){
    $(this).css("color", "rgb(100, 71, 7)");
    }, function(){
    $(this).css("color", "rgb(9, 50, 53)");
    
}); 

$(".ls_e").hover(function(){
    $(this).css("border-color", "rgb(130, 130, 221)");
    }, function(){
    $(this).css("border-color", "black");
}); 


$(".submit").hover(function(){
    $(this).css("border-color", "rgb(130, 130, 221)");
    }, function(){
    $(this).css("border-color", "black");
}); 

$(".arrow").hover(function(){
    $(this).css("color", "rgb(130, 130, 221)");
    }, function(){
    $(this).css("color", "rgb(51, 36, 5)");
}); 

$(document).ready(function(){
    
    $('.demo').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
    });

    $('#backTop').backTop({

        // the scroll position in px from the top
        'position' : 400,
    
        // scroll animation speed
        'speed' : 500,
    
        // red, white, black or green
        'color' : 'black',
    });

});



