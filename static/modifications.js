$( document ).ready(function() {
    if($("#error").text().trim().length !== 0){
        $("#error").fadeTo(2000, 500).slideUp(1000, function(){
            $("#error").slideUp(1000);
        });
    }
    $(".post").each(function(index, element){
        $(element).find(".show-new-comment-form").click(function(){
            if ($(element).find(".new-comment-box").is(':hidden')){
                $(element).find(".new-comment-box").show();
                $(element).find(".show-new-comment-form").text("Cancel")
            }else{
                $(element).find(".new-comment-box").hide();
                $(element).find(".show-new-comment-form").text("Comment")
            }
        });

        $(element).find(".show-comments").click(function(){
            $(element).find(".hide-comments").show()
            $(element).find(".comment-box").show()
            $(element).find(".show-comments").hide()
        });

        $(element).find(".hide-comments").click(function(){
            $(element).find(".show-comments").show()
            $(element).find(".comment-box").hide()
            $(element).find(".hide-comments").hide()
        });
    });
    
    // $("#showCommentForm").click(function(){
    //     if($("#newCommentBox").is(':hidden')){
    //         $("#newCommentBox").show();
    //         $("#showCommentForm").text("Cancel");
    //     }else{
    //         $("#newCommentBox").hide();
    //         $("#showCommentForm").text("Comment");
    //     }
    // });
    // $("#showComments").click(function(){
    //     $("#hideComments").show()
    //     $("#commentBox").show()
    //     $("#showComments").hide()
    // });
    // $("#hideComments").click(function(){
    //     $("#showComments").show()
    //     $("#commentBox").hide()
    //     $("#hideComments").hide()
    // });
});