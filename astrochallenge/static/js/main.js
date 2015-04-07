$(".give-kudos").click(function(){
    button = $(this);
    observation = $(this).data('observation');
    $.get("/accounts/kudos/" + observation + '/', function(data){
        if(data.result != 'success'){
            location.replace('/accounts/login/');
        }else {
            button.html(data.kudos + ' <span class="glyphicon glyphicon-thumbs-up"></span>');
            button.addClass("btn-success").removeClass("btn-info");
        }
    });
});
