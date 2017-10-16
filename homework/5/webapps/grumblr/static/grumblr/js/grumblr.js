function showCommentArea(){
      window.alert("test")
}

function populateList() {
    var pathname = '/get-items';
    if(window.location.pathname.includes("profile")){
        var paths = window.location.pathname.split('/')
        pathname = '/get-profile-items/' + paths[paths.length-1];
    }
    $.get(pathname)
      .done(function(data) {
          var list = $("#blogpost");
          list.data('max-time', data['max-time']);
          list.html('')
          for (var i = 0; i < data.items.length; i++) {
              item = data.items[i];
              var new_item = $(item.html);
              new_item.data("item-id", item.id);
              list.append(new_item);
          }
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
function addItem(){
    var itemField = $("#new_message");
    $.post("/add-item/globalstream", {"item": itemField.val()})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}

$(document).ready(function () {
  // Add event-handlers
  $("#add-btn").click(addItem);
  $("#comment-btn").click(showCommentArea);

  populateList();
  $("#new_message").focus();

  if(window.location.pathname.includes("profile")){
    window.setInterval(getProfileUpdates, 5000);
   }
   else{
    window.setInterval(getUpdates, 5000);
   }

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
