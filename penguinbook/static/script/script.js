$(document).ready(function() {

    // GLOBLE VARIABLES
    const currentUserID = NaN;
    var chattingFriendID = 0;
    var socketList = new Array();
    /********************************************************** INDEX NAVBAR *********************************************/

    // SCRIPT TO CHECK WHETHER ERROR OCCURED AT LOG-IN/SIGN-IN TIME OR REGISTRATION/SIGNUP TIME.
    $("#forgot-password").click(function(){
        $("#find-email").modal("show");
    });

    // SCRIPT TO CREATE CSRF_TOKEN IN EXTERNAL JAVASCRIPT FILE.
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

   // SCRIPT TO SEARCH/FIND REGISTERED EMAIL.
   $("#submit-find-email").click(function(){ 

        $.ajax({
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            method: "POST",
            url: window.location.href,
            dataType: "json",    
            data: {
                find_email :$("#input-find-email").val(),
            },
            success: function(response){
        
                $('#find-email').modal('toggle');
                if(response.flag=='email exist'){
                    $("#password-reset").modal("show");
                }
                else{
                    alert("Account doesn't exist !");
                    location.reload();
                }
            },
            error: function(){
                $("#find-email").modal("toggle");
                alert("Something wrong :-(");
            }
        });
    });
    
    // SCRIPT TO RESET PASSWORD.
    $("#submit-new-password").click(function(){ 
    
        if ($("#password1").val()==$("#password2").val())
        {   
            $.ajax({
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                method: "POST",
                url: window.location.href,
                dataType: "json",
                data: {
                    email: $("#input-find-email").val(),
                    new_password: $("#password1").val(),
                },
                success: function (response){
                    $("#password-reset").modal("toggle");
                    alert(response.flag);
                },
                error: function (response){
                    $("#password-reset").modal("toggle");
                    alert("Something wrong :-(");
                },
            });
        }
        else{
            alert("Password mismatch !");
            $("#password-reset").modal("toggle");
        }
    }); 

    /********************************************************** SCRIPT FOR COMMON PAGE(HOME & PROFILE)*********************************************/

    // SCRIPT TO SHOW THE FRIENDSHIP NOTIFICATIONS.
    $("#notifications-friendship").click(function(){
        $("#notifications-friendship-toast").toast('show');
    });
    
    // SCRIPT TO HIDE THE FRIENDSHIP NOTIFICATIONS.
    $("#notifications-friendship-toast-close").click(function(){
        $("#notifications-friendship-toast").toast("hide");
    });

    $(".like").click(function(event){
        // GET THE ID OF POST WHETHER IT IS TEXT POST OR IAMGE POST OR BOTH AND ID OF POSTER(THE USER WHO POSTED).
        // alert(event.target.id);
        const [postID, posterID] = event.target.id.split("-").slice(1,)
        likes = $("#likes-"+postID+"-"+posterID).text().split(" ")[1];
        // alert(postID);
        // alert(posterID);
        // alert(likes);
        var likeStatus = NaN;
        if($("#"+event.target.id).css("color")!='rgb(0, 0, 255)'){
            if (likes==""){
                likes=0;
            }
            likes=Number(likes) + 1;
            likeStatus = "liked";
            // $("#"+event.target.id).text(" like "+likes).css("color", "blue");            
        }else{

            likes=Number(likes) - 1;
            likeStatus = "unliked";
            // $("#"+event.target.id).text(" like "+likes).css("color", "");            

        }

        $.ajax({
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            method: "post",
            url: window.location.href,
            dataType: "json",
            data: {
                post_id:postID,
                // liker_id:currentUserID,
                like_status:likeStatus,
                like_gainer_id: posterID
            },
            success:function(){
                if (likeStatus=="liked"){

                    $("#likes-"+postID+"-"+posterID).text("Likes "+likes);
                    $("#"+event.target.id).text(" like").css("color", "blue");

                }
                else{
                    if(likes==0){

                        likes="";
                    }
                    $("#likes-"+postID+"-"+posterID).text("Likes "+likes);
                    $("#"+event.target.id).text(" like").css("color", "");

                }
                
            },
            error:function(){

                alert("Check your internet connection !");
            }
        });
    });

    $(".likes").mouseenter(function(event){
        const postID = event.target.id.split("-")[1]

        $("#likers-"+postID).toast("show");
    });

    $(".likers").mouseleave(function(event){
        // const postID = event.target.id.split("-")[1]
        // alert(event.target.id);
        $(".likers").toast("hide");
    });
    
    $(".comment").keypress(function(event) { 
        if(event.keyCode === 13){

            const [postID, posterID, commenterID]=event.target.id.split("-").slice(2,)
            commentText = $("#"+event.target.id).val();
            var commentData = {'post_id': postID, 'poster_id': posterID, 'commenter_id':commenterID, 'comment_text':commentText};
            $.ajax({
                headers:({'X-CSRFToken':getCookie("csrftoken")}),
                method:'post',
                url: window.location.href,
                data:commentData,
                success:function(data){
                    // $("#comment-history-"+postID).append($("#user-icon-name").html()+data.new_comment);
                    // $("#comment-history-"+postID).append($("#user-icon-name").html());

                    $("#post-"+postID).before(
                        "<div class='mt-2 ml-1'><a href="+"{% url 'profile' %}?"+currentUserID+'>'+data.first_name+" "+data.last_name+"</a> "+data.new_comment+"</div>");
                    $("#"+event.target.id).val("");
                },
                error:function(){
                    alert("Unable to comment");
                }
            });event.preventDefault();
        }
    });
    
    $(".short-bio").click(function(event){
        alert(event.target.id);

    })
    /********************************************************** SCRIPT FOR HOME PAGE ************************************************/
    $("#friend-list-toast").toast('show');

    $(".friend").click(function(event){
        alert("called it self.")
        $("#online-friends").height("30%");
        chattingFriendID = event.target.id;
        $("#chat-box-header").find('img').attr('src',$(this).find('img').attr('src'));
        $("#chat-box-header").find('a').attr('href',"/penguinbook/profile/?"+chattingFriendID);
        $("#chat-box-header").find('a')[0].text=$(this).find('strong').attr('name');
        $("#chat-box").toast('show');

        $.ajax({
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            method: "post",
            url: window.location.href,
            dataType: "json",
            data: {
                message_receiver_id:chattingFriendID
            },
            success:function(chat_history){
                chat_history=JSON.parse(chat_history);
                $("#chat-box-body").empty();

                for(message of chat_history){

                    if(Number(message.fields.user)==currentUserID){

                        $("#chat-box-body").append("<div class='row-lg mt-1 reply-box'><label class='alert alert-success alert-sm float-right ml-5' id='user-text-reply'>"+message.fields.message+"</label></div><br>");
                    }else{
                        $("#chat-box-body").append("<div class='row-lg mt-1 reply-box'><label class='alert alert-primary float-left mr-5' id='friend-text-reply'>"+message.fields.message+"</label></div><br>");

                    }
                    $('#chat-box-body').animate({ scrollTop: $('#chat-box-body').prop('scrollHeight')},10);// 10 is delay time of scroll.

                }
            },
            error:function(){

                alert("Unable to load chat history, refresh page and try again !");
            }   
        });
    });
    var chatSocket = Array()
    $('#chat-box').on('shown.bs.toast', function(){
        //TERNARY OPERATOR TO CREATE UNIUE ROOM NAME
        roomName = chattingFriendID>currentUserID?String(chattingFriendID)+String(currentUserID):String(currentUserID)+String(chattingFriendID);
        if(jQuery.inArray(roomName, socketList)==-1){

            // CREATING SOCKET
            chatSocket = new WebSocket('ws://'+window.location.host+'/ws/penguinbook/home/'+roomName+'/');
            socketList.push(roomName)
        }
            chatSocket.onmessage=function(e) {
                const data = JSON.parse(e.data);
                if(data.message){

                    if(Number(data.user_id)==Number(currentUserID)){

                        $("#chat-box-body").append("<div class='row-lg mt-1 reply-box'><label class='alert alert-success alert-sm float-right ml-5' id='user-text-reply'>"+data.message+"</label></div><br>");
                    }else{
                        $("#chat-box-body").append("<div class='row-lg mt-1 reply-box'><label class='alert alert-primary float-left mr-5' id='friend-text-reply'>"+data.message+"</label></div><br>");
                    }
                    $('#chat-box-body').animate({ scrollTop: $('#chat-box-body').prop('scrollHeight')},10);// 10 is delay time of scroll.
                };
            }
        
        chatSocket.onclose = function(e){
            console.error('Chat socket closed unexpectedly');
            socketList.pop(roomName)
        };
    });
    
    // $('#chat-message-input').focus();
    $('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    $('#chat-message-submit').on('click', function(e) {
        //stplit for message extration from string.
        const message = $('#chat-message-input').val();
        // const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'user_id':currentUserID,
            'message_receiver_id':chattingFriendID
        }));
        $('#chat-message-input').val('');

    });

    $("#chat-box-close").click(function(){
        chatSocket.close(); //Close connecton for connected client ws
        $("#chat-box").toast("hide");
        $("#online-friends").height("94%");

    });
   
    /********************************************************** SCRIPT FOR PROFILE PAGE *********************************************/
    
    var canvas  = $('#canvas');
    context = canvas.get(0).getContext('2d');
    // var preview = $('#preview');

    /* FLAG TO GET INFO WHTHER YOU ARE UPLOADING DISPLAY PICTURE OR DISPLAY COVER. */
    var photoUploadFlag = new String()
    
    /* SCRIPT TO OPEN THE PHOTO ON MODAL TO EDIT, PREVIEW AND UPLOAD. */
    $(".photo-upload").change(function (event) {
        if (this.files && this.files[0]) {

            if ( this.files[0].type.match(/^image\//)){

                photoUploadFlag = event.target.id;
                var reader = new FileReader();
                reader.onload = function (event) {

                    const img = new Image();
                    img.src = event.target.result;
                    img.onload = function() {

                        context.canvas.height = img.height;
                        context.canvas.width  = img.width;
                        context.drawImage(img, 0, 0);
                    }
                    $("#photo-edit-upload-modal").modal("show");
                }
                reader.readAsDataURL(this.files[0]);
            }else{
                alert("Invalid file type! Please select an image file.");
            }
        }else{
            alert('No file(s) selected.');
        }
    });
  
    /* SCRIPTS TO HANDLE THE CROPPER BOX. */
    var $image = $("#canvas");
    var cropBoxData;
    var canvasData;

    $("#photo-edit-upload-modal").on("shown.bs.modal", function () {

        var ratio;
        if(photoUploadFlag.localeCompare("input-display-picture")==0){

            ratio=1/1;
        }else if(photoUploadFlag.localeCompare("input-display-cover")==0){

            ratio=3/1;
        }
        else{ /*if(photoUploadFlag.localeCompare("input-post-image")==0) */
            
            ratio=NaN;
        }
        $image.cropper({
            aspectRatio: ratio,
            viewMode:2,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        }).on("hidden.bs.modal", function () {
            cropBoxData = $image.cropper("getCropBoxData");
            canvasData = $image.cropper("getCanvasData");
            $image.cropper("destroy");
        });
    });

    /* SCRIPT TO GET THE CROPPED IMAGE AND DRAW ON THE SAME MODAL AS PREVIEW. */
    $("#photo-crop-button").click(function () {
        var croppedImageDataURL = $image.cropper("getCroppedCanvas").toDataURL("image/png"); 
        // var image = new Image();
        if(photoUploadFlag.localeCompare("input-display-picture")==0){

            $("#preview").empty().append( $("<img id='image-file' style='width:100%'>").attr("src", croppedImageDataURL));
        }else if(photoUploadFlag.localeCompare("input-display-cover")==0){

            $("#preview").empty().append( $("<img id='image-file' style='height:100%; max-height:400px; display:block'>").attr("src", croppedImageDataURL));
        }else{ /*if(photoUploadFlag.localeCompare("input-post-image")==0) */

            $("#preview").empty().append( $("<img id='image-file' style='height:100%;max-height:410px;width:auto;'>").attr("src", croppedImageDataURL));
        }
        // $(".about-post").val($("#about-post").val());
        // alert($(".about-post").val());

    });

    /* SCRIPT TO GET THE CO-ORDINATES OF THE NEW IMAGE TO BE CROPPED AND UPLOAD THE IMAGE TO THE SERVER. */
    $("#upload-button").click(function () {
        $(".about-post").val($("#about-post").val());
        var cropData = $image.cropper("getData");
        $(".crop-box-start-point-x").val(cropData["x"]);
        $(".crop-box-start-point-y").val(cropData["y"]);
        $(".crop-box-width").val(cropData["width"]);
        $(".crop-box-height").val(cropData["height"]);
        $(".photo-upload-flag").val(photoUploadFlag);
        $(".about-post").val($("#about-post").val())
        // $("#photo-edit-upload-modal").modal('toggle');
        if(photoUploadFlag.localeCompare("input-display-picture")==0){

            $("#form-upload-display-picture").submit();

        }else if(photoUploadFlag.localeCompare("input-display-cover")==0){

            $("#form-upload-display-cover").submit();

        }else{
            
            $("#form-post-text-image").submit();
        }
    });
    
    $("#post-text-submit").click(function(){
        $.ajax({
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            method: "POST",
            dataType:'json',
            url:window.location.href,
            data:{
                post_text:$("#post-text").val()
            },
            success:function(){
                alert($('#form-post-text-image img').attr('src'));
                var new_post = $(
                '<div class="alert alert-secondary mt-3" id="post-form">'+
                    '<div class="row">'+
                        '<div class="col-sm">'+
                            "<img src="+$('#form-post-text-image img').attr('src')+" class='profile-icon'>"+
                            "<strong><a href='{% url 'profile' %}?{{user.id}}' id='profileID'>"+$('#form-post-text-image a').text()+"</a></strong>"+
                        '</div>'+
                        '<div class="col-sm text-right">'+ new Date()+'</div>'+
                    '</div>'+
                        "<div class='row center mt-2'><div class='col-sm ml-3' id='only-post-text'>"+$('#post-text').val()+"</div></div>"+
                    "<hr>"+
                    "<div class='d-flex justify-content-between'>"+
                        "<label style='font-size:15px' class='far fa-thumbs-up ml-5'> Like</label>"+
                        "<label style='font-size:15px' class='far fa-comment'> Comment</label>"+
                        "<label style='font-size:15px' class='far fa-share-square mr-5'> Share</label>"+
                    '</div>'+
                    '<hr>'+
                    '<form method="POST" enctype="multipart/form-data">'+
                        '<div class="form-group">'+
                            '<label for="{{ user_post_form.post_text.label }}"></label>'+
                            '<textarea class="form-control form-control-sm" rows="1" name="post-text" placeholder="Comment. . ." style="border-radius: 30px"></textarea>'+
                        '</div>'+
                    '</form>'+
                '</div>');
                if($("#post-text").val()){                                               
                    new_post.insertAfter("#form-post-text-image");
                }
                $("#post-text").val(""); // reset form data
            },
            error:function(){
                alert("cant post"),
                $("#post-text").val("");
            },
        });
    });
    // $myForm.unbind('submit').bind('submit',function(event){
    $("#send-user-action").click(function(){
        if($("#send-user-action").text()==" Friend"){

            alert("The unfriend and block features are under devlopment.")
            $("#send-user-action").attr('class',"fas fa-user-check send-user-action")

        }else if($("#send-user-action").text()==" Add Friend"){

            // $('#'+event.target.id).attr('id',"cancel-request");
            $("#send-user-action").attr('class',"fas fa-user-times send-user-action");
            $("#friendship-approach").val("you requested");

        }else if($("#send-user-action").text()==" Accept Request"){
            
            // $('#'+event.target.id).attr('id',"friend");
            $("#send-user-action").attr('class',"fas fa-user-check send-user-action");

            $("#friendship-approach").val("you accepted");

        }else if($("#send-user-action").text()==" Cancel Request"){
            
            // $('#'+event.target.id).attr('id',"add-friend");
            $("#send-user-action").attr('class',"fas fa-user-plus send-user-action");
        }
        else{
            // $('#'+event.target.id).val(" Blocked");
            $("#send-user-action").attr('class',"fas fa-user-lock send-user-action")
        }
            // <div class="dropdown" id="blockOrUnfriend">
            //   <label class="fas fa-camera-retro" data-toggle="dropdown" type="button" style="font-size: 22px;"> Edit </label>
            //   <ul class="dropdown-menu">
            //     <li><label class="btn" id="block">Block</label></li>
            //     <li><label class="btn" id="unfriend">unfriend</label></li>
            //   </ul>
            // </div>

            // var $formData = $(this).serializeArray();
            // var $thisURL = $('#send-friend-request-button').attr('data-url') || window.location.href; // or set your own url
            // $.post('/url/', $(this).serialize(), function(data){

        $.ajax({

            headers: { "X-CSRFToken": getCookie("csrftoken")},
            method: "POST",
            url: $('#form-send-friend-request').attr('data-url') || window.location.href, // or set your own url
            dataType: "json",
            data: {

                id : $('#send-user-id').val(),
                action : $.trim($("#send-user-action").text()),
                friendship_approach: $("#friendship_approach").val()
            },
            success: function (data){

                console.log(data)
                $("#send-user-action").text(" "+data.friendship_status);
                
            },
            error:function (data){

                console.log(data);
                alert('Error '+data.friendship_status);
            },
        })
    });
});
