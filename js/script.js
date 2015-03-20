$( document ).ready(function()
{
  if(navigator.geolocation){

     var pos = navigator.geolocation.getCurrentPosition(
       function(position)
       {
         sessionStorage.setItem('lat', position.coords.latitude);
         sessionStorage.setItem('lon', position.coords.longitude);
         sessionStorage.setItem('geo', 1);
         return position;
      }, function(error){
        sessionStorage.setItem('geo', 0);

      });


  }

  sessionStorage.setItem('public', 0);

  if(sessionStorage.getItem('token') === null){
    $.ajax({
      type: "GET",
      url: 'html/login.html',

      success:function(html) {
        $('#content').html(html);


      },
      error: function(html){
        alert("Request failed. Couldn't load log in page. Sorry. Try again maybe?");
      }
    });
  }
  else{
    $('#user').removeClass('hidden');
    $('#user').prepend("<h4>Welcome, "+sessionStorage.getItem('name')+"! <button onClick='logout()'>Logout</button></h4>");
    loadBooks();
  }
});

//gets user's books from db and displays them on page
function loadBooks(){
  $.ajax({
    type: "GET",
    url: 'html/books.html',

    success:function(html) {
      $('#content').html(html);
      if(sessionStorage.getItem('token') !== null)
        $('#publicButton').removeClass('hidden');

    },
    error: function(html){
      alert("Request failed. Couldn't load books page. Sorry. Try again maybe?");
    }
  });

  if (sessionStorage.getItem('public')==1)
    url =  './public';
  else
    url = './book';

  token = sessionStorage.getItem('token')

  $.ajax({
    type: "GET",
    url: url,
    dataType: 'json',
    data: {token: token},

    success:function(html) {
      $('#books').empty();
      for (var x=0; x < html.length; x++){
        var bookhtml = "<div class='bookreview img-rounded'><p><strong>"+html[x].title+"</strong> <br />by<br /><em> "+html[x].author+"</em></p><img src='"+html[x].coverurl+"' /><br /><img src='img/"+html[x].rating+".png' /><p><em>\""+html[x].comment+"\" <br></em>~"+html[x].username+"</p><br />";


        if (parseInt(html[x].user) == parseInt(token))
          bookhtml += "<button class='btn-block' onClick='editBook("+html[x].key+")'>Edit/Delete</button>";

        if (html[x].lat !== null){
          bookhtml += "<a href='https://www.google.com/maps/place/"+html[x].lat+","+html[x].lon+"' target='_blank'>Where was this review made?</a>";
        }
        bookhtml+="</div>";


      $('#books').append(bookhtml);
    }

    },
    error: function(html){
      alert("Request failed. Couldn't load book reviews. Sorry. Try again maybe?");
    }
  });
}

//attempts to log in / create new user
function doLogin(){
  var valid = true;
  var uname = $("input[name='uname']").val();
  if(uname==="" || /\s/.test(uname)){
    alert("Username cannot be blank or contain spaces.");
    valid=false;
  }

  var pw = $("input[name='pw']").val();
  if(pw==="" || /\s/.test(pw)){
    alert("Password cannot be blank or contain spaces.");
    valid=false;
  }

  var name = $("input[name='name']").val().replace(" ", "");
  if (name === "") name = null;

  if (valid)
  $.ajax({
    type: "POST",
    url: './login',
    dataType: 'json',
    data:{
      uname: uname,
      pw: pw,
      name: name
    },
    success:function(html) {
      alert(html.msg);
      sessionStorage.setItem('token', html.token);
      sessionStorage.setItem('name', html.username);
      $('#user').prepend("<h3>Welcome, "+sessionStorage.getItem('name')+"! <button onClick='logout()'>Logout</button></h3>");
      loadBooks();

    },
    error: function(html){
      alert("Request failed. " + html.statusText);
      console.log(html);
    }
  });
}

//adds book to database, associated with user
function addBook(){
  var valid = true;

  var title = $("input[name='title']").val().trim();
  if (title === ""){
    alert("Title cannot be blank.");
    valid = false;
  }

  var author = $("input[name='author']").val().trim();
  if (author === ""){
    alert("Author cannot be blank.");
    valid = false;
  }

  var rating = $("input[name='rating']").val().trim();
  if (rating <0 || rating >5 || rating === ""){
    alert("Rating must be in range 0-5.");
    valid = false;
  }

  var comment = $("input[name='comment']").val().trim();

  var visible = $('input[name="public"]').is(':checked');

  if (visible)
    visible = 1;
  else
    visible = 0;



  var token = sessionStorage.getItem('token');

  var key = $("input[name='key']").val();

  var data = {
    title: title,
    author: author,
    rating: rating,
    comment: comment,
    visible: visible,
    token: token,
  }

  if (sessionStorage.getItem('geo')==1){
    data['lat'] = sessionStorage.getItem('lat');
    data['lon'] = sessionStorage.getItem('lon');
  }


  $.ajax({
    type: "GET",
    url: 'https://www.googleapis.com/books/v1/volumes',
    dataType: 'json',
    data: {q: title},
    success:function(html) {
      coverurl = null;
      for (var x=0; x< html.items.length; x++){
        if ("volumeInfo" in html.items[x])
          if ("imageLinks" in html.items[x].volumeInfo)
            if ("smallThumbnail" in html.items[x].volumeInfo.imageLinks)
              coverurl = html.items[x].volumeInfo.imageLinks.smallThumbnail;
              break;
      }
      data['coverurl'] = coverurl;

      if (key != ""){
        var url = './book/'+key;
        var method = "PUT";
      }
      else{
        var url = './book';
        var method = "POST";
      }

      $.ajax({
        type: method,
        url: url,
        dataType: 'json',
        data: data,
        success:function(html) {
          alert(html.msg);
          loadBooks();

        },
        error: function(html){
          alert("Request failed. Couldn't add book review. Sorry.");
        }
      });
    },
    error: function(html){
      data['coverurl'] = "img/nothumb.png";

      $.ajax({
        type: "POST",
        url: './book',
        dataType: 'json',
        data: data,
        success:function(html) {
          alert(html.msg);
          loadBooks();

        },
        error: function(html){
          alert("Request failed. Couldn't add book review. Sorry.");
        }
      });


    }
  });

}

//logs out
function logout(){
  sessionStorage.clear();
  $.ajax({
      type: "GET",
      url: 'html/login.html',

      success:function(html) {
        $('#content').html(html);
        $('#books').empty();
        $('#user').empty();
        $('#publicButton').addClass('hidden');

      },
      error: function(html){
        alert("Request failed. Couldn't load log in page. Sorry. Try again maybe?");
      }
    });
}

//switches visibility of level of displayed reviews
function togglePublic(mode){
  if (mode > 0){
    $('#publicButton').attr('onClick', 'togglePublic(0)').text("View Your Reviews");
    sessionStorage.setItem('public', 1);
    loadBooks();
  }
  else{
    $('#publicButton').attr('onClick', 'togglePublic(1)').text("View Public Reviews");
    sessionStorage.setItem('public', 0);
    loadBooks();
  }

}

//populates form to change an entry
function editBook(key){

  token = sessionStorage.getItem('token');

  $.ajax({
    type: "GET",
    url: './book/' + key,
    dataType: 'json',
    data: {token:token},
    success:function(html) {
      $("input[name='key']").val(key);
      $("input[name='title']").val(html['title']);
      $("input[name='author']").val(html['author']);
      $("input[name='rating']").val(html['rating']);
      $("input[name='comment']").val(html['comment']);
      if (html['visible'])
        $("input[name='public']").prop('checked', true);
      else
      $("input[name='public']").prop('checked', false);
      $("#addButton").text("Update entry");
      $("#deleteButton").removeClass('hidden').attr('onClick', 'delBook('+key+')');
      $('html, body').animate({ scrollTop: 0 }, 'fast');

    },
    error: function(html){
      alert("Request failed. Couldn't add book review. Sorry.");
    }
  });


}


//deletes an entry
function delBook(key){

  token = sessionStorage.getItem('token');

  $.ajax({
    type: "DELETE",
    url: './book/' + key+'/'+token,
    dataType: 'json',

    success:function(html) {
      alert(html.msg);
      $("#addButton").text("Add Book Review");
      $("#deleteButton").addClass('hidden').attr('onClick', '');
      loadBooks();

    },
    error: function(html){
      alert("Request failed. Couldn't add book review. Sorry.");
    }
  });


}
