$( document ).ready(function() {
    if($("#error").text().trim().length !== 0){
        $("#error").fadeTo(2000, 500).slideUp(1000, function(){
            $("#error").slideUp(1000);
        });
    }
    $(".post").find(".show-new-comment-form").click(function(){
        item = $(".post")
        item.find(".show-new-comment-form").click(function(){
            if (item.find(".new-comment-box").is(':hidden')){
                item.find(".new-comment-box").show();
                item.find(".show-new-comment-form").text("Cancel")
            }else{
                item.find(".new-comment-box").hide();
                item.find(".show-new-comment-form").text("Comment")
            }
        })
    });

    $(".post").find(".show-comments").click(function(){
        item = $(".post")
        item.find(".hide-comments").show()
        item.find(".comment-box").show()
        item.find(".show-comments").hide()
    });

    $(".post").find(".hide-comments").click(function(){
        item = $(".post")
        item.find(".show-comments").show()
        item.find(".comment-box").hide()
        item.find(".hide-comments").hide()
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