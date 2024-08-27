// submit_btn.addEventListener("click", myScript);
// object.onclick = function(){myScript};



// const submit_btn = document.getElementById("submit_btn");
// submit_btn.addEventListener("click", function() {
//     document.getElementById("demo").innerHTML = "Hello World";
//     let val = document.getElementById("destination_input").value;
//     alert(val);

// });


$(function() {

    $("#destination_input").focus();

    gotoCity = function() {
        let dest_val = $("#destination_input").val().toLowerCase();
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


        window.location.href = "/" + dest_val + "/";

    }

    $("#submit_btn").on("click", gotoCity);
    $("#destination_input").on("keypress", function(event) {

        // press enter;
        if (event.which == 13)  {
            // $(this).val();
            gotoCity();
        }
    });

});


// alert("hello");

