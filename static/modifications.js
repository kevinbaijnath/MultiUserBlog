$( document ).ready(function() {
    if($("#error").text().trim().length !== 0){
        $("#error").fadeTo(2000, 500).slideUp(1000, function(){
            $("#error").slideUp(1000);
        });
    }
    $("#showCommentForm").click(function(){
        if($("#newCommentBox").is(':hidden')){
            $("#newCommentBox").show();
            $("#showCommentForm").text("Cancel");
        }else{
            $("#newCommentBox").hide();
            $("#showCommentForm").text("Comment");
        }
    });
    $("#showComments").click(function(){
        $("#hideComments").show()
        $("#commentBox").show()
        $("#showComments").hide()
    });
    $("#hideComments").click(function(){
        $("#showComments").show()
        $("#commentBox").hide()
        $("#hideComments").hide()
    });
});