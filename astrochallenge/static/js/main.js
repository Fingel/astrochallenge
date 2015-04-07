$(".give-kudos").click(function(){
    button = $(this);
    observation = $(this).data('observation');
    $.get("/accounts/kudos/" + observation + '/', function(data){
        button.html(data.kudos + ' kudos ');
        button.append('<span class="glyphicon glyphicon-ok"></span>');
        button.addClass("btn-success").removeClass("btn-info");
    });
});
