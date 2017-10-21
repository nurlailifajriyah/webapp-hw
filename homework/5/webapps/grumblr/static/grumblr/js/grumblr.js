
function populateList() {
    var pathname = '/get-items';
    if(window.location.pathname.includes("profile")){
        var paths = window.location.pathname.split('/')
        pathname = '/get-profile-items/' + paths[paths.length-1];
    }
    $.get(pathname)
      .done(function(data) {
          var list = $('#blogpost');
          list.data('max-time', data['max-time']);
          list.html('');
          for (var i = 0; i < data.items.length; i++) {
              item = data.items[i];
              var new_item = $(item.html);
              new_item.data("item-id", item.id);
              list.append(new_item);
              comment_list = null;
              $.get('/get-comments/' + item.id)
                  .done(function(data) {
                      comment_list = $("#blogpost").find('#comments-' + data['blogpostid']);
                      comment_list.data('max-time', data['max-time']);
                      for (var j = 0; j < data.comments.length; j++) {
                          var comment = data.comments[j];
                              var new_comment = $(comment.html); //call html from model.py
                              new_comment.data("comment-id", comment.id);
                              comment_list.append(new_comment);
                      }
                  });
//                  }
          }
      });
}

function addItem(){
    var itemField = $("#id_blog_text");
    $.post("/add-item/globalstream", {"blog_text": itemField.val()})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

function getUpdates() {
    var pathname = '/get-items/';
    var list = $("#blogpost")
    var max_time = list.data("max-time")
    $.get(pathname + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
                  var new_item = $(item.html); //call html from model.py
                  new_item.data("item-id", item.id);
                  list.prepend(new_item);
          }
      });
}
function getProfileUpdates() {
    var paths = window.location.pathname.split('/')
    var pathname = '/get-profile-items/';
    var list = $("#blogpost")
    var max_time = list.data("max-time")

    $.get(pathname + paths[paths.length-1] + '/' + max_time )
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
                  var new_item = $(item.html); //call html from model.py
                  new_item.data("item-id", item.id);
                  list.prepend(new_item);
          }
      });
}

function addComment(){
    var blogpostid = $(this).attr("id");
    var itemField =  $("#blogpost").find('#new_comment-' + blogpostid)
    $.post("/add-comment/" + blogpostid, {"comment": itemField.val()})
      .done(function(data) {
          showCommentArea(blogpostid);
          itemField.val("").focus();
      });
}


function showCommentArea(blogpostid){
    var pathname = '/get-comments/';
    var list = $("#blogpost").find('#comments-' + blogpostid)
    var max_time = list.data("max-time")
    $.get(pathname + blogpostid + '/' + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.comments.length; i++) {
              var comment = data.comments[i];
                  var new_item = $(comment.html); //call html from model.py
                  new_item.data("comment-id", comment.id);
                  list.prepend(new_item);
          }
      });
}

$(document).ready(function () {
  // Add event-handlers


  populateList();

  $("#new_message").focus();

  $("#add-btn").click(addItem);


  if(window.location.pathname.includes("profile")){
    window.setInterval(getProfileUpdates, 5000);
   }
   else{
    window.setInterval(getUpdates, 5000);
   }

   $("#blogpost").on('click', ".comment-btn", addComment);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
