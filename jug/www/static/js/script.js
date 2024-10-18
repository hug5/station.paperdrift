// submit_btn.addEventListener("click", myScript);
// object.onclick = function(){myScript};



// const submit_btn = document.getElementById("submit_btn");
// submit_btn.addEventListener("click", function() {
//     document.getElementById("demo").innerHTML = "Hello World";
//     let val = document.getElementById("destination_input").value;
//     alert(val);

// });


$(function() {

    // Focus by default;
    // $("#destination_input").focus();

    gotoCity = function() {
        let dest_val = $("#destination_input").val().toLowerCase();
        //
          // let dest_val = $("#destination_input").val();
          // let dest_val = "Big City";


          // Don't need to do this check anympore; just checking through python so can catch manual entry as well;
          // if (dest_val == "home" || dest_val == "paperdrift") {
          //     dest_val = "/";
          // }
          // else {
          //   dest_val = "/" + dest_val;
          // }
            // window.location.href = dest_val;

        // remove non-alphanumeric characters, but allow for space
        // all bad characters will be replaced with space;
        // then later we'll remove redundant spaces;
        // dest_val = dest_val.replace(/[^0-9a-z\- ]/gi, ' ')


        dest_val = dest_val.replace(/[\[\]{}\\<>?@*~!#$%^&(),;+\.]/gi, ' ');

        // remove redundant spaces
        // dest_val = dest_val.replace(/\s\s+/g, ' ')
        dest_val = dest_val.replace(/ +/g, " ") // this should also work;
        dest_val = dest_val.trim();

        // encode
        dest_val = encodeURIComponent(dest_val);
        // replace %20 with +
        dest_val = dest_val.replace(/%20/gi, '+');

        window.location.href = "/" + dest_val + "/";


        // return decodeURIComponent(str);
    }

    $("#submit_btn").on("click", gotoCity);
    $("#destination_input").on("keypress", function(event) {

        // press enter;
        if (event.which == 13)  {
            // $(this).val();
            gotoCity();
        }
    });

    $("#more_btn").on("click", function(event) {

        let btn_type = $(this).html();


        $(".news_hide").slideToggle(150);
        // $(".news_hide").fadeToggle(150);
        // $(".news_hide").show();
        // $(".news_hide").hide();

        if (btn_type == "+MORE"){
            $(this).html("-LESS");
        }
        else {
            $(this).html("+MORE")
        }

    });





});



// $("#location_box img").fadeOut(0);
// $("#location_box img").fadeIn(400);


// var p_action  = "contactUsMsg",
//     p_name    = lib.ajaxencode(name),
//     p_email   = lib.ajaxencode(email),
//     p_msg     = lib.ajaxencode(msg),

//     param     = "action=" + p_action +
//                 "&name=" + p_name +
//                 "&email=" + p_email +
//                 "&msg=" + p_msg;
// $.post(G.ajaxUrl, param, function(result) {

//     $(this_btn).removeClass("disabled");

//     if (result == "ok") {

//         $("#msgForm").slideUp(400, function() {
//             $("#formSection p").fadeIn(300).html("YOUR MESSAGE WAS SENT!");
//         });
//     }

//     else {
//         $("#formSection p").fadeIn(300).html("Oops! There was an error.");
//     }
// });


// $("#submit").click(function (e) {
//     $.post("result.php",
//     {
//         firstName: $("#firstName").val(),
//         lastName: $("#lastName").val()
//     })
//     .done(function (result, status, xhr) {
//         $("#message").html(result)
//     })
//     .fail(function (xhr, status, error) {
//         $("#message").html("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText)
//     });
// });

// var jqxhr = $.ajax( "example.php" )
//   .done(function() {
//     alert( "success" );
//   })
//   .fail(function() {
//     alert( "error" );
//   })
//   .always(function() {
//     alert( "complete" );
//   });


//    $.ajax({
//      url: 'https://jsonplaceholder.typicode.com/todos/1', // Sample API endpoint
//      method: 'GET',
//      dataType: 'json',
//      success: function(data) {
//      // Update the content on success
//      $("#dataContainer").text('Title: ' + data.title);
//      },
//      error: function(error) {
//      // Handle errors
//      console.error('Error:', error);
//      }
//  });

// $.ajax({
//     url: "geeks.txt",
//     success: function (result) {
//         $("#h11").html(result);
//     },
//     error: function (xhr, status, error) {
//         console.log(error);
//     }
// });



// $.ajax({
//   type: "POST",
//   url: url,
//   data: data,
//   success: success,
//   dataType: dataType
// });