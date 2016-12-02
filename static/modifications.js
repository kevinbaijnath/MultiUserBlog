$( document ).ready(function() {
    if($("#error").text().trim().length !== 0){
        $("#error").fadeTo(4000, 500).slideUp(1000, function(){
            $("#error").slideUp(1000);
        });
    }
});