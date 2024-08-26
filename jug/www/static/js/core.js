// submit_btn.addEventListener("click", myScript);
// object.onclick = function(){myScript};



// const submit_btn = document.getElementById("submit_btn");
// submit_btn.addEventListener("click", function() {
//     document.getElementById("demo").innerHTML = "Hello World";
//     let val = document.getElementById("destination_input").value;
//     alert(val);

// });


$(function() {

    $("#submit_btn").on("click", function() {

        let dest_val = $("#destination_input").val();
        // alert(dest_val);
        dest_val = "/" + dest_val;
        window.location.href = dest_val;

    });

});


// alert("hello");

