$(function() {
//////////////////////////////////

function setHomeSection() {
    if ( $("#homeSection").length < 1 ) return false;
    //if ( $("#homeTest").length < 1 ) return false;


    // Word cloud
    (function() {

        var
            fg = 0,
            bg = 1,

            glist = $("#wordcloudDiv").attr("gallery"),
            arr   = glist.split(","),
            limit = arr.length - 1,

            ibgload           = 700, //time to wait before loading image for 2nd image into background
            wordInterval1     = 3000,  // wordcloud initial interval, then we make it longer
            wordInterval2     = 6000,  // after initial short interval, make longer here
            timeToFadeFgOut   = 2500,    // time to fade foreground out, revealing background underneath; creates fade effect
            timeToFadeNewFgIn = 1000,     // time to fade in new foreground that looks exactly like the prior background so that we now see fg image, not bg image
            timeToLoadNewBg   = 1000;  // time to wait after new FG image was faded in, to load the new bg image




        //do this once on page load
        setTimeout(function() {
            //I set the div's height in CSS so that the page doesn't go weird when it initially load; then I set to auto here
            $("#wordcloudDiv").css("height", "auto");

            //set background to next image but with slight delay so that other page images get chance to load;
            // essentially a preload effect;
            $("#wordcloudDiv").css("background-image", "url(" + arr[bg] + ")"); //1
        }, ibgload);


        var
            newImg = new Image(),

            wordclouding = function() {

                //intitial interval was 3000; then we make it longer, 6000
                if (wordInterval1 < wordInterval2) {
                    clearInterval(wordcloudingInterval);
                    wordInterval1 = wordInterval2;
                    setInterval(wordclouding, wordInterval1);

                }

                //fadeout the foreground image, revealing background underneath
                $("#wordcloudDiv img").fadeOut(timeToFadeFgOut, function(){
                    fg = bg;     //fg = 0
                    bg++;        //bg = 1

                    if (bg > limit) {
                        bg = 0;
                    }

                    //this is seamlessly replace the foreground image with background;
                        //user shouldn't see that it's happening; when done, replace background with next img
                        //this essentially creates a pre-load effect by setting up the next image;
                        // Sometimes there seems to be a glitch; trying using longer fadein and seeing if that
                        //fixes it; maybe it's a browser issue; sometimes ther's a glitch; most of the time
                        //there doesn't seem to be; This might be a Firefox only issue;
                    $(this).attr("src", arr[fg]).fadeIn(timeToFadeNewFgIn, function() {
                        newImg.src = arr[bg];
                        //when foreground has been set, then replace bg with next image
                        //this time going to try to use a image object, load it there first, and then replace bg; see if that fixes the glitch;
                        setTimeout(function() {
                            $("#wordcloudDiv").css("background-image", "url(" + arr[bg] + ")");
                        }, timeToLoadNewBg);

                    });

                });
            };

        //Set our wordcloud internval, setInterval
        var wordcloudingInterval = setInterval(wordclouding, wordInterval1);


    })();
    // doWordCloud();

    //click on sectionB... take to book page
    // $("#sectionB").on("click", function() {
    //     window.location.href = "/book/theswines/";
    // });

}
function setBookSection() {

    if ( $("#bookSection").length < 1 ) return false;

    //intro section only
    if ( $("#bookIntroArticle").length < 1 ) return false;


    $("#authorNoteExpandBtn").on("click", function() {

        var btnText = $("#authorNoteExpandBtn").html();

        if (btnText == "+") {
            //$("#transparentP").hide();

                    // $("#authorNoteP").css("height", "auto");
                    // $("#authorNoteP").slideDown(300).css("height", "auto");

                    //maybe animate only works if the height is set originally through js?
                    // $("#authorNoteP").css("height", "auto").hide(0).animate({
                    //     "height": "auto"
                    // }, 400);

            // $("#authorNoteP").css("height", "auto").hide(0).slideDown(300);
            // $("#authorNoteP").css("height", "auto");
            $("#authorNoteP").slideDown(200);
            $("#authorNoteExpandBtn").html("-"); //.css("position", "static");

        } else {
            // $("#authorNoteP").slideUp(300, function(){
            //     $(this).css("height", "").show(0);
            // });

            // $("#authorNoteP").css("height", "");
            $("#authorNoteP").slideUp(200);
            // $("#transparentP").show();
            $("#authorNoteExpandBtn").html("+"); //.css("position", "relative");
        }

        return false;
    });


}
function setContactSection() {
    if ( $("#contactSection").length < 1 ) return false;

    var this_btn; //set later


    var doAjax = function(name, email, msg) {

        var p_action  = "contactUsMsg",
            p_name    = lib.ajaxencode(name),
            p_email   = lib.ajaxencode(email),
            p_msg     = lib.ajaxencode(msg),

            param     = "action=" + p_action +
                        "&name=" + p_name +
                        "&email=" + p_email +
                        "&msg=" + p_msg;

        $.post(G.ajaxUrl, param, function(result) {

            $(this_btn).removeClass("disabled");

            if (result == "ok") {

                $("#msgForm").slideUp(400, function() {
                    $("#formSection p").fadeIn(300).html("YOUR MESSAGE WAS SENT!");
                });
            }

            else {
                $("#formSection p").fadeIn(300).html("Oops! There was an error.");
            }
        });

    };

    //init events
    $("#sendBtn").on("click", function() {

        if ( !lib.formInputCheck("msgForm") || $(this).hasClass("disabled") ) return false;

        var name     = $("#nameField").val(),
            email    = $("#emailField").val(),
            msg      = $("#msgField").val();
        this_btn = $(this); //not part of var inititialization above

        doAjax(name, email, msg);
        //prevent double clicking
        $(this_btn).addClass("disabled");
        return false;
    });


}


function setAuthSection() {
    if ( $("#authSection").length < 1 ) return false;

    if ( $("#loginSection").length > 0 ) {
        if ( $("#loginSection").length < 1 ) return false;

        var doAjax = function(type, email, pw) {
            var p_action  = type,
                p_email   = lib.ajaxencode(email),
                p_pw      = pw ? lib.ajaxencode(pw) : "",
                param     = "action=" + p_action +
                            "&email=" + p_email +
                            "&pw=" + p_pw;

            $.post(G.ajaxUrl, param, function(result) {

                if (result == "ok") {
                    if (type == "loginhelp") {
                        var msg = "A temporary password is on its way! Please check your email, including spam folder.";
                        var customFn = function(param) {
                            if (param == "close") {
                                location.reload(); //reload page
                            }
                        };
                        //do msgBox sending in our custom function that will be called
                        lib.doMsgBox("Help", msg, ["CLOSE"], customFn);
                    } else {
                        // location.reload(); //reload page
                    // $h .= "<form action=\"$go_url\" autocomplete=\"on\">";

                        var go_url = $("#loginSection form").attr("action");
                        window.location.href = G.baseUrl + go_url;
                    }
                }

                //some result other than "ok"
                else {
                    var msg_login               = "Sorry. Wrong email or password.",
                        msg_loginhelpError      = "Sorry. Please try again.",
                        msg_loginhelpBademail   = "Sorry. We couldn't find your email. Please double-check your email address.",
                        msg = "";

                    if (type == "login") {
                        msg = msg_login;
                    }
                    else if (type == "loginhelp") {
                        msg = result == "bademail" ? msg_loginhelpBademail : msg_loginhelpError;
                    }

                    // alert(msg);
                    lib.doMsgBox("Ooops!", msg, ["CLOSE"]);
                }
            });
        };

        $("#loginBtn").on("keypress", function(event) {
            if ( event.which == 13 ) {
                // event.preventDefault();
                var senderId = $(this).attr("id");
                $("#" + senderId).click();
            }
        });

        $("#loginBtn, #loginhelpBtn").on("click", function() {

            //this will check if fields are filled in; also checks valid emails
            if (!lib.formInputCheck("loginBoxFieldset")) return;


            // var pw1 = $("#pwField1").val();
            var sender = $(this).attr("id"),
                //hasError = false,
                type,
                email,
                pw;

            email = document.getElementById("email-1").value.trim().toLowerCase();

            if (sender == "loginBtn") {
                type = "login";
                pw = document.getElementById("password-1").value;
            }
            else if (sender == "loginhelpBtn") {
                type = "loginhelp";
            }

            doAjax(type, email, pw);

        });

        var selected_previous = "loginSel"; //current selected
        // $(".loginSectionBoxDiv").on("click", function() {
        $("#loginSel, #loginhelpSel").on("click", function() {

            var sender = $(this).attr("id");
            if (sender == selected_previous) return;

            $("#loginBtn, #loginhelpBtn").hide(0);

            if (sender == "loginSel") {
                if (sender == selected_previous) return;
                $("#loginBtn").show(0);
                if (selected_previous == "loginhelpSel") {
                    $("#password-1").slideDown(200);
                }
                if (selected_previous == "signupSel") {
                    $("#password-2").slideUp(200);
                }
            }
            else if (sender == "loginhelpSel") {
                $("#loginhelpBtn").show(0);
                $("#password-1, #password-2").slideUp(200);
            }
            $("#email-1").focus();
            selected_previous = sender;
        });
    } //loginSection


    if ( $("#settingsSection").length > 0 ) {

        // *TODO::Need to make these methdos generic
        $("#emailSaveBtn").on("click", function(){

            var doAjax = function(email) {

                var p_action  = "changeEmail",
                    p_email   = lib.ajaxencode(email),
                    param     = "action=" + p_action +
                                "&email=" + p_email;

                $.post(G.ajaxUrl, param, function(result) {

                    if (result == "ok") {

                        //make new email the current email
                        $("#currentEmail .fieldValue").html(email);
                        var oriTxt = $("#emailSaveBtn").html(); //get original button text
                        $("#emailSaveBtn").html("Saved!"); //changed to notify that its saved

                        //setTimeout is not part of js but a DOM method; can't send parameters or something like that; however
                        //modern browsers accept a third parameter like so below;
                        //https://stackoverflow.com/questions/1190642/how-can-i-pass-a-parameter-to-a-settimeout-callback
                        //https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout
                        setTimeout(function() {
                            $("#emailSaveBtn").html(oriTxt); //change the text back;
                            $("#emailChangeBtn").click(); //trigger click to close;
                        }, 1000, oriTxt);
                    }

                    //some result other than "ok"
                    else {
                        // alert("error");
                        var msg = "There was an error.";
                        lib.doMsgBox("Ooops!", msg, ["CLOSE"]);

                    }

                });
            };


            var hasError = false;
            var email = document.getElementById("email-1").value.trim().toLowerCase();
            var currentEmail = $("#currentEmail .fieldValue").html().toLowerCase();
            if (email == "" || email == currentEmail || !lib.checkEmail(email)) {
                $("#email-1").addClass("error");
                hasError = true;
            }

            if (!hasError) {
                // alert("no error");
                doAjax(email);
            }

        });

        $("#passwordSaveBtn").on("click", function(){
            var doAjax = function(pw) {
                var p_action  = "changePW",
                    p_pw      = lib.ajaxencode(pw),
                    param     = "action=" + p_action +
                                "&pw=" + p_pw;
                $.post(G.ajaxUrl, param, function(result) {

                    if (result == "ok") {
                        //make new email the current email
                        var oriTxt = $("#passwordSaveBtn").html(); //get original button text
                        $("#passwordSaveBtn").html("Saved!"); //changed to notify that its saved

                        //see above
                        setTimeout(function() {
                            $("#passwordSaveBtn").html(oriTxt); //change the text back;
                            $("#passwordChangeBtn").click(); //trigger click to close;
                        }, 1000, oriTxt);
                    }

                    //some result other than "ok"
                    else {
                        // var msg = "There was an error.<br>asdfasdfasdfasd<br>asdfasdfasf<br>asdfasdfasdf";
                        var msg = "There was an error.";
                        lib.doMsgBox("Ooops!", msg, ["CLOSE"]);
                    }
                });
            };

            var hasError = false;
            var pw = document.getElementById("password-1").value;
            if (pw.trim() === "") {
                $("#password-1").addClass("error");
                hasError = true;
            }

            if (!hasError) {
                //alert("no error");
                doAjax(pw);
            }
        });

        $("#nameSaveBtn").on("click", function(){

            var doAjax = function(name) {
                var p_action  = "changeName",
                    p_name    = lib.ajaxencode(name),
                    param     = "action=" + p_action +
                                "&name=" + p_name;
                $.post(G.ajaxUrl, param, function(result) {
                    if (result == "ok") {

                        //make new email the current email
                        $("#currentName .fieldValue").html(name);
                        var oriTxt = $("#nameSaveBtn").html(); //get original button text
                        $("#nameSaveBtn").html("Saved!"); //changed to notify that its saved

                        //setTimeout is not part of js but a DOM method; can't send parameters or something like that; however
                        //modern browsers accept a third parameter like so below;
                        //https://stackoverflow.com/questions/1190642/how-can-i-pass-a-parameter-to-a-settimeout-callback
                        //https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout
                        setTimeout(function() {
                            $("#nameSaveBtn").html(oriTxt); //change the text back;
                            $("#nameChangeBtn").click(); //trigger click to close;
                        }, 1000, oriTxt);
                    }
                    //some result other than "ok"
                    else {
                        // var msg = "There was an error.<br>asdfasdfasdfasd<br>asdfasdfasf<br>asdfasdfasdf";
                        var msg = "There was an error.";
                        lib.doMsgBox("Ooops!", msg, ["CLOSE"]);
                    }
                });
            };

            var hasError = false;
            var name = document.getElementById("name-1").value;
            if (name.trim() === "") {
                $("#name-1").addClass("error");
                hasError = true;
            }

            if (!hasError) {
                //alert("no error");
                doAjax(name);
            }
        });
        $("#emailSection, #passwordSection, #nameSection").on("click", ".fBtn", function(){
            //we have 4 .fBtn; only want to react to the ones that has the class .change;
            //the other buttons are to save changes
            if ($(this).hasClass("change")) {
                var aId = $(this).attr("openDiv");
                //toggle the associated input field and clear its field value to ready it for next time
                $("#" + aId).toggle(300).children("input").val("");
            }
        });
    } //#settingsSection

    if ( $("#adminSection").length > 0 ) {

        // $(".updateBtn, .addBtn, .delBtn").on("click", function(){
        $("#adminUserRowSection").on("click", ".updateBtn, .addBtn, .delBtn", function(){

            var doAjax = function() {

                var p_action      = "adminUsersUpdate",
                    p_type        = type,
                    p_authNo      = authNo,
                    p_name        = lib.ajaxencode(name),
                    p_email       = lib.ajaxencode(email),
                    p_permissions = lib.ajaxencode(permissions),

                    param = "action="       + p_action +
                            "&type="        + p_type +
                            "&authNo="      + p_authNo +
                            "&name="        + p_name +
                            "&email="       + p_email +
                            "&permissions=" + p_permissions;
                $.post(G.ajaxUrl, param, function(result) {


                    var arr = result.split(";");
                    var result_status = arr[0];

                    if (result_status == "ok") {

                        var timer = type == "delete" ? 0 : 700;
                        setTimeout(function() {
                            var rowHtml = lib.ajaxdecode(arr[1]);
                            // $("#adminUserRowSection").fadeOut(200).html(rowHtml).fadeIn(200);
                            $("#adminUserRowSection").html(rowHtml);

                        }, timer);

                    }

                    else {
                        var msg = "There was an error.";
                        lib.doMsgBox("Ooops!", msg, ["CLOSE"]);
                        $(ths).html(btnTextOri);
                    }

                });
            };

            var type,
                authNo      = "",
                name        = "",
                email       = "",
                permissions = "",
                ths         = $(this),
                parent,
                hasError,
                btnTextOri;


            parent = $(this).parent();
            authNo = $(parent).find(".authNo-1").val();

            if ($(this).hasClass("updateBtn")) {
                type = "update";
            }
            else if ($(this).hasClass("addBtn")) {
                type = "add";
            }
            else if ($(this).hasClass("delBtn")) {
                type = "delete";

                //get current value of button
                var currVal    = $(this).html();
                var defaultBtn = $(this).attr("defaultBtn");
                var confirmBtn = $(this).attr("confirmBtn");

                clearTimeout(G.deltimer);

                if (currVal == confirmBtn) {
                    //do ajax to delete file; pass folder/file info for db; and html row to remove if successful
                    $(this).html(defaultBtn); //reset delete btn; if ajax error, then good to go again;
                    doAjax();
                } else {
                    //set current selection to DEL?
                    $(this).html(confirmBtn);
                    //setTimer in which user must confirm deletion
                    G.deltimer = setTimeout(function() {
                        $(".delBtn").html(defaultBtn); //if user somehow selects multiple; reset all;
                    }, 1000);
                }

                return false;
            }
            else {
                return false;
            }

            name = $(parent).find(".name-1").val();
            email = $(parent).find(".email-1").val();
            permissions = $(parent).find(".permissions-1").val();
            hasError = false;

            if (email == "" || !lib.checkEmail(email)) {
                $(parent).find(".email-1").addClass("error");
                hasError = true;
            }

            if (!hasError) {

                btnTextOri = $(this).html();
                $(this).html("SAVING"); //indicate in button that we're saving
                doAjax();
            }
        });
    }

}

function setHeaderSection() {

    $("#authLogout").on("click", function(){
        var p_action  = "authLogout";
        var param = "action=" + p_action;

        $.post(G.ajaxUrl, param, function(result) {
            if (result == "ok") {
                location.reload(); //reload page
            }

        });
    });
}

function setSignupSection() {
    // email signup section
    if ( $(".signupSection").length < 1 ) return false;

    // set our section variable beforehand here
    var
        email_element,
        email,
        source,
        this_btn,
        hasError;

    // var doAjax = function(email, source, email_element) {
    var doAjax = function() {

        var
            p_action  = "emailSignup",
            p_email   = lib.ajaxencode(email),
            p_source   = lib.ajaxencode(source),
            param     = "action=" + p_action +
                        "&source=" + p_source +
                        "&email=" + p_email;
                        // also assume setting status to SUBSCRIBED


        // alert(param); return;
        // lib.doCursor("wait");
        $.post(G.ajaxUrl, param, function(result) {
            // lib.doCursor();

            //reset the email field to blank; if double click, won't work
            $(email_element).val("");
            $(this_btn).removeClass("disabled");

            // return: error, success, not_found, "bad_request" // all lowercase
            // return: error, success, not_found, "bad_request", already_subscribed

            if (result == "success") {
                var message = "Thank you. You're all signed up!<br>" + lib.hent(email);
                lib.doMsgBox("Welcome", message, ["CLOSE"]);
            }
            else if (result == "already_subscribed") {
                var message = "Congrats! Looks like you're already on our mailing list!<br>" + lib.hent(email);
                lib.doMsgBox("You're Subscribed", message, ["CLOSE"]);
            }
            //for anything else, assume error
            else {
                lib.doMsgBox("Error", "Ooops! There was some kind of error. Please try again.", ["CLOSE"]);
            }

        });
    };


    $("#pageDiv").on("click", ".signupSection .signupBtn", function() {

        if ($(this).hasClass("disabled")) return false;

        // set variables
        email_element = $(this).parent().children(".signupEmailField");
        email         = $(email_element).val().trim();
        source        = $(this).parent().attr("source");
        this_btn      = $(this);
        hasError      = false;


        // The html element, when set to email, will also do some basic checks and show error
        if (email == "" || !lib.checkEmail(email)) {
            $(email_element).addClass("error");
            hasError = true;
        }

        if (!hasError) {
            $(this_btn).addClass("disabled");
            doAjax(email, source, email_element);
        }

    });

}

function setCommons() {

    // var doShareBtn = setTimeout(function() {
    (function doShareBtn() {
        // seems that if you don't give the shareThis script time to line up the buttons
        // won't display correctly when it's shown; so need to give it 1.5 or 2 seconds

        var h      = 0,
            w      = 0,
            toggle = true;

        // settimer to check every xsec if share btn is ready
        var getDimensionsTimer = setInterval(function() {
            h = $("#share_this").height();
            w = $("#share_this").width();

            // alert(w + ", " + h);

            if (h != 0 && w != 0) {
                //clear timer once we have h, w values, which means that share btns are raedy
                clearTimeout(getDimensionsTimer);
                // alert(w + ", " + h);

                // show share btn when it's ready
                // $("#shareBtn").fadeIn(100);    // use this if display:none
                // $("#shareBtn").css("opacity", 1); // use this if set opacity:0

                // change from absolute to static position, ie, dfault position
                $("#share_this").css({
                    "position"  : "static",
                    "overflow"  : "hidden",
                    "height"    : h
                });

                $("#shareBtn").on("click", function() {

                    if (toggle) {
                        $("#share_this").css({
                            "opacity": 1,
                            "display": "inline-block",
                            "width": "0"
                        });

                        $(".hmBtn").each(function() {
                            if ( $(this).attr("id") != "shareBtn" ) {
                                $(this).hide(0);
                            }

                        });

                        $("#share_this").animate({
                            "width": w
                        }, 250, "linear");
                        toggle = false;
                    } else {
                        $("#share_this").animate({
                            "width": "0px",
                        }, 150, function() {
                            $("#share_this").css({
                                "opacity": 0,
                                "display": "none",
                                "width": w
                            });
                            $(".hmBtn").each(function() {
                                if ( $(this).attr("id") != "shareBtn" ) {
                                    $(this).fadeIn(100);
                                }
                            });
                        });
                        toggle = true;
                    }
                });
            }
        }, 200);


    })(); //, 3500);

    /////////////////
        /*
            (function doShareBtn() {
                // seems that if you don't give the shareThis script time to line up the buttons
                // won't display correctly when it's shown; so need to give it 1.5 or 2 seconds

                var h      = 0,
                    w      = 0,
                    toggle = true;



                // var pos = $(element).position();
                //   542:                     var top = pos.top - t_offset;
                //   543:                     var left = pos.left - l_offset;


                // alert(sbtn.left);

                // settimer to check every xsec if share btn is ready
                var getDimensionsTimer = setInterval(function() {
                    h = $("#share_this").height();
                    w = $("#share_this").width();

                    // alert(w + ", " + h);

                    if (h != 0 && w != 0) {
                        //clear timer once we have h, w values, which means that share btns are raedy
                        clearTimeout(getDimensionsTimer);
                        // alert(w + ", " + h);

                        // show share btn when it's ready
                        // $("#shareBtn").fadeIn(100);    // use this if display:none
                        // $("#shareBtn").css("opacity", 1); // use this if set opacity:0

                        // change from absolute to static position, ie, dfault position
                        $("#share_this").css({
                            // "position"  : "static",
                            // "left" : sbtn.left,
                            "overflow"  : "hidden",
                            "height"    : h
                        });

                        $("#shareBtn").on("click", function() {


                            var sbtn = $("#shareBtn").position();

                            if (toggle) {
                                $("#share_this").css({
                                    "opacity": 1,
                                    "display": "inline-block",
                                    "width": "0"
                                });

                                $(".hmBtn").each(function() {
                                    if ( $(this).attr("id") != "shareBtn" ) {
                                        $(this).hide(0);
                                    }
                                })

                                $("#share_this").animate({
                                    "width": w,
                                    "left": sbtn.left - w

                                }, 250, "linear");
                                toggle = false;

                            } else {
                                $("#share_this").animate({
                                    "width": "0px",
                                    "left": sbtn.left
                                }, 150, function() {
                                    $("#share_this").css({
                                        "opacity": 0,
                                        "display": "none",
                                        "width": w
                                    });
                                    $(".hmBtn").each(function() {
                                        if ( $(this).attr("id") != "shareBtn" ) {
                                            $(this).fadeIn(100);
                                        }
                                    })
                                });
                                toggle = true;
                            }
                        });
                    }
                }, 200);

            })(); //, 3500);

        */

        /*var doShareBtn = setTimeout(function() {
            // seems that if you don't give the shareThis script time to line up the buttons
            // won't display correctly when it's shown; so need to give it 1.5 or 2 seconds
            var h      = $("#share_this").height(),
                w      = $("#share_this").width(),
                toggle = true;

            $("#share_this").css({
                "width": "0px",
                "position": "static",
                "opacity" : 1,
                "overflow" : "hidden"
            });


            $("#shareBtn").on("click", function() {
                // $("#add_this").toggle(200, "linear");

                if (toggle) {
                    // $("#add_this").fadeOut(200, "linear");
                    // $("#add_this").css("width", 0);
                    $("#share_this").css({
                            "width": w,
                            "height": h
                    }), function() {
                        $("#share_this").css("overflow", "visible");
                    };

                    toggle = false;
                } else {
                    // $("#add_this").fadeIn(200, "linear");
                    // $("#add_this").css("width", "132px");
                    $("#share_this").css({
                        "width": "0px",
                        "overflow" : "hidden"
                    });

                    toggle = true;
                }

            });

        }, 500);
        */


        //to check on add_this button, have to wait for it to run its js
        /*    var doShareBtn = setTimeout(function() {

            //get height of add_this
            // var h = $("#add_this").height();
            var h = $("#share_this").height();

            var toggle = false;
            //if add_this is working, it should have a height
            if (h > 0) {
                // alert("..");

                $("#shareBtn").fadeIn(100);
                $("#shareBtn").on("click", function() {
                    // $("#add_this").toggle(200, "linear");

                    if (toggle) {
                        // $("#add_this").fadeOut(200, "linear");
                        // $("#add_this").css("width", 0);
                        $("#share_this").css("width", 0);
                        toggle = false;
                    } else {
                        // $("#add_this").fadeIn(200, "linear");
                        // $("#add_this").css("width", "132px");
                        $("#share_this").css("width", "132px");
                        toggle = true;
                    }
                    // $("#add_this").toggle(0).css("width", "default");
                    return false;
                });
            }
        }, 1000);
        */

        //universal input behavior; press esc, then erase content
        // $("#pageDiv").on("keyup", "input", function(event) {
        //     // pressed escape key
        //     if (event.which == 27)  {
        //         $(this).val("");
        //         return false;
        //     }
        // });


    var doSearch = function() {
        var keywords = lib.ajaxencode( $("#searchField").val().trim() );
        if (keywords == "") return;
        window.location.href = G.baseUrl + "/browse/search/" + keywords + "/";

    };

    $("#searchContainerDiv").on("click", "#searchBtnDiv", function() {
        doSearch();
    });

    $("#searchContainerDiv").on("keydown", "#searchField, #searchBtnDiv", function(event) {
        // press Return
        if (event.which == 13)  {
            doSearch();
        }
    });


    //not sure if this is a good universal behavior to remove error styling
    // $("input, textarea").on("focus", function() {
    // this hook seems to be much too broad, #pageDiv
    $("#pageDiv").on("focus", "input, textarea", function() {
        if ($(this).hasClass("error")) {
            $(this).removeClass("error");
        }
    });


    $(window).scroll(function(){
        //get scroll position
        G.scroll_top = $(window).scrollTop(); //get vertical position of scroll; when at top, then 0
        //if (scroll_top + 800 >= document_height) {
        //        alert(document_height + ", " + G.scroll_top);
        //}

        // run any parallax stuff for home page
        if ( $("#homeArticle").length > 0 ) Parallax.home();

    });


    // not sure if the lazy load gets triggered automatically or gets triggered on start here??
    shared.doLazy();

}

function initEvents() {

    setCommons();
    setHeaderSection();
    setHomeSection();
    setBookSection();
    setContactSection();
    setAuthSection();
    setSignupSection();

    //////
        // these functions will initialize more events
        //setCommons();
        //setMainSection();

        //$(".delBtn").on("click", delBtnClickfunction() {
        // $(".delBtn").on("click", delBtnClick);
        //have to hook the event to contentSEction, not delBtn because when
        //page is refreshed, events would get unhooked... not efficient
        /*$("#contentSection").on("click", ".delBtn", delBtnClick);
        $("#contentSection").on("click", ".file_copy", copyBtnClick);

        //click on the file name or download button
        $("#contentSection").on("click", ".private_link", privatelinkClick);

        //toggle display of greeting or login when clicked
        $("#logoDiv").on("click", function() {

            var user = $("#greetingDiv span").html();
            if (!user) return;

            $("#greetingDiv").toggle();
            $("#loginDiv").toggle();

            $("#loginField").val(""); //reset login value
            $("#loginField").focus(); //focus

        });

        $("#loginDiv").on("keydown", "input", function(event) {
            // press Return
            if (event.which == 13)  {
                var logid = $("#loginField").val().trim();
                if (logid == "") return;
                //call function to validate the ID
                validateID(logid);
            }
        });*/

        /*var imgUrl = "/upub/media/Boy9.apng";
        var images1 = new Image()
        images1.src = imgUrl;


        //clunky effect!
        var temp_apng = setTimeout(function() {
            $("#mainSection").css("background-image", "url(/upub/media/Boy9.apng)");
        }, 4000);
        */

}

function initVars() {
    //G.is_ssl = location.protocol === "https:" ? true : false;
    //G.baseUrl = "http://" + document.location.host;
    // G.baseUrlS = "https://" + document.location.host;
    G.baseUrl = "https://" + document.location.host;
    G.viewportal_width = $(window).width(); //browser width

    // /browse/search/trish/
    // get substring from 1 index; skip first /; then split/explode into array
    G.urlParams = ( location.pathname.substr(1) ).split("/"); //.substr(1) would that be.
    // alert(arr[0]); // browse
    // alert(arr[1]); // search
    // alert(arr[2]); // trish
    // alert(arr[3]); //



    // G.baseUrlX = getBaseUrl();
    // G.ajaxUrl = G.baseUrlX + "/ajax/";
    G.ajaxUrl = G.baseUrl + "/ajax/";
}

(function start() {
    initVars();     // initialize global variables
    initEvents();   // initialize events
    //setGreeting();
    // checkUser();

})();


/////////////////////////////////////////////////////////////////
});

/////////////////////////////////////////////////////////////////


var shared = {


    setMediaBtns : function () {

        var nameElement = $(G.lastFocusedElement).attr("name"); //imgUrl or textBody

        $(".fileOperation_container span").each(function() {
            $(this).removeClass("disabled");
        });

        if (nameElement == "imgUrl") {
            $(".fileOperation_container .htmlBtn, .fileOperation_container .mdBtn").each(function() {
                $(this).addClass("disabled");
            });
        } else {
            $(".fileOperation_container .fnBtn").each(function() {
                $(this).addClass("disabled");
            });
        }

    },

    doLazy: function() {
        // http://jquery.eisbehr.de/lazy/

        $(".lazy").Lazy({
            // your configuration goes here
            // scrollDirection: 'vertical', //default both
            effect: "fadeIn",  // show effect
            effectTime: 200,   // time to view image
            threshold: 200,    // when lazy gets trigger below viewport in pixels
            visibleOnly: true, // Determine if only visible elements should be load.
            onError: function(element) {
                // console.log('error loading ' + element.data('src'));
                //alert('error loading ' + element.data('src'));
            }
        });

    }
};


/////////////////////////////////////////////////////////////////

$(function() {
//////////

    if ( $(".userPageSection").length < 1 ) return false;

    // mouseenter, mouseleave (triggered only by indicated element?)
    // mouseover, mouseout (triggered by outer and inner elements)

    var thisUserPage, // save object to THIS user page class
        userPageNo,
        userSectionNo,
        newText,
        //variable to save original section text; object variable to save multiple sections; each section
        //will be saved in separate object variable;
        originalText = {};


    var doAjax = function() {

        var sender = "userPageSection";

        var param =
            "action="           + sender +
            "&userPageNo="      + lib.ajaxencode(userPageNo) +
            "&userSectionNo="   + lib.ajaxencode(userSectionNo) +
            "&newText="         + lib.ajaxencode(newText);


        $.post(G.ajaxUrl, param, function(result) {
            // alert( lib.ajaxdecode(result));

            // var arr           = result.split(";"),
            //     result_status = arr[0];

            // posting result
            if (result == "ok") {
                var msg = "Changes were posted.",
                caption = "SAVED",
                customFn = function() {
                    setTimeout(function() {
                        lib.doMsgBox();
                    }, 1500);
                };

                var newtext = $(thisUserPage).find("textarea").val();
                $(thisUserPage).find(".userSectionTextDiv").html(newtext);
                $(thisUserPage).find("textarea").val("");
                // originalText = ""; //reset
                delete originalText[userSectionNo]; // delete is supposed to delete the variable
                closeModal();

                lib.doMsgBox(caption, msg, [], customFn);


            }
            else {

                var msg = "There was an error.";
                lib.doMsgBox("Ooops!", msg, ["close"]);
            }


        });
    }; //ajax



    var userPageSectionEvent = function() {

        // mouseover and mouseout triggers constantly

        $(".userPageSection.auth")
        // .on("mouseover", function() {
        .on("mouseenter", function() {
            $(this).css("background-color", "#EAEAEA");
            $(this).find(".userPageBtnContainer").show();
        })
        // .on("mouseout", function() { //seems to trigger constantly
        .on("mouseleave", function() {
            $(this).css("background-color", "");
            $(this).find(".userPageBtnContainer").hide();

        });
    };

    var closeModal = function() {
        $(thisUserPage).removeClass("modal");
        userPageSectionEvent(); //hook the events back again that we disabled on edit
        lib.dobg(); // show or hide background
    };

    $(".userPageBtnContainer").on("click", ".edit", function(){
        // get the userPageSection class that is the parent of this edit button only
        thisUserPage = $(this).closest(".userPageSection");

        $(thisUserPage).addClass("modal");
        var text = $(thisUserPage).find(".userSectionTextDiv").html();
        $(thisUserPage).find("textarea").val(text);
        userSectionNo = $(thisUserPage).attr("userSectionNo");

        if (!originalText[userSectionNo]) originalText[userSectionNo] = text; //save original text; only do on first edit

        $(thisUserPage).off("mouseleave");
        lib.dobg(); // show or hide background
    });

    $(".userPageBtnContainer").on("click", ".preview", function(){
        var newtext = $(thisUserPage).find("textarea").val();
        $(thisUserPage).find(".userSectionTextDiv").html(newtext);
        $(thisUserPage).find("textarea").val("");
        closeModal();
    });

    $(".userPageBtnContainer").on("click", ".post", function(){
        userPageNo      = $(thisUserPage).attr("userPageNo"),
        //userSectionNo   = $(thisUserPage).attr("userSectionNo"),
        newText         = $(thisUserPage).find("textarea").val();
        doAjax();
    });

    $(".userPageBtnContainer").on("click", ".cancel", function(){
        // on cancel, set back to original
        $(thisUserPage).find(".userSectionTextDiv").html(originalText[userSectionNo]);
        // originalText[userSectionNo] = ""; //reset variable for original text
        delete originalText[userSectionNo]; // delete is supposed to delete the variable
        // alert(originalText[userSectionNo]); //comes back undefined
        closeModal();
    });

    userPageSectionEvent();


//////////
});


/////////////////////////////////////////////////////////////////

var Parallax = {

    home: function(ths, name) {
        //return if not at home page
        if ( $("#homeArticle").length < 1 ) return;

        // slowing down the scroll of sectionA, not speeding up sectionB
        // var banner_parallax = $("#sectionA");
        var banner_parallax = $("#sectionB");

        if (G.start_y === undefined) {
            var start_y = parseInt( $(banner_parallax).css("top") );
            G.start_y = start_y;
        }

        if (G.margin_bottom == undefined) {
            G.margin_bottom = 0;
        }


        // var width = G.viewportal_width;
        // var move_up_ratio = (width <= 414) ? .1 : .4; //0.6; //.4;

        // var move_up_ratio = .4; //0.6; //.4;
        var move_up_ratio = .3; //0.6; //.4;

        var parallax_y = Number(G.start_y) - Number(G.scroll_top * move_up_ratio);
        // var parallax_y = Number(G.start_y) + Number(G.scroll_top * move_up_ratio);


        // also have to reduce the margin bottom for the moving parallax element; don't want the margin to get too big
        // unless we want it to becuase we have a background image to show
        G.margin_bottom = G.margin_bottom ? parseInt(parallax_y) :  parseInt(G.margin_bottom) + parseInt(parallax_y);

        // alert(G.margin_bottom);

        // ** end init **
        ////////////////////////////////////////////////////////////////////////////


        (function doBanner_parallax() {

            // var aPos = $("#hide_anchor").position();
            // var anchor = parseInt(aPos.top) + 100;

            // //banner_parallax settings
            // // var z = G.scroll_top > anchor ? -3 : -1; //not sure if this makes a diff
            // var disp = G.scroll_top < anchor ? "inline" : "none";

            // var opac = 1;
            // if (G.scroll_top > anchor) {
            //     opac = ( 200 - (G.scroll_top - anchor) ) / 200;
            //     opac = opac < .1 ? 0 : opac;
            // }

            $(banner_parallax).css({
                "top":parallax_y,
                "margin-bottom" : G.margin_bottom
                // "z-index": 1 //this doesn't seem to make a difference?
                // ,
                // "opacity": opac
                // "display": disp
            });

        })();

        // (function doPmoveImg() {

        //     if ( $("#pmove").length < 1 ) return;


        //     var pmoveImg = $("#pmove"); //this is the surfer image
        //     var pmoveImg_width = parseInt( $("#pmove img").css("width") );


        //     //move foreground image across screen
        //     var pmoveImg_left = G.scroll_top * .6;
        //     var main_pos = $("#mainDiv").position(); //get element position property; getting css doesn't work if "auto";
        //     //don't let img go off to the left beyond site borders;
        //     pmoveImg_left = pmoveImg_left < main_pos.left ? main_pos.left : pmoveImg_left;

        //     var left_width = parseFloat(pmoveImg_left + pmoveImg_width);
        //     if ( left_width > pageWidth ) {
        //             pmoveImg_width = pageWidth - pmoveImg_left;
        //             // if (pmoveImg_width < 0) show = false;

        //     }

        //     //var pmoveImg_left = G.scroll_top > 1200 ? G.scroll_top * .5 : G.scroll_top * .6;

        //     //var margin_bottom = parseInt( $("#billboardHome_site .billboard#billboardR").css("margin-bottom") );
        //     //var mbottom = parseInt( $("#billboardHome_site .billboard#billboardR").css("margin-bottom") );
        //     var board_height = parseInt( $(banner_parallax).css("height") );
        //     if (G.pmoveImg_top_start_variable === undefined) {
        //             // var factor = is_mobile ? 6/13 : 3/7 ;
        //             var factor = 3 / 7;
        //             G.pmoveImg_top_start_variable = G.start_y + (G.start_y + board_height) * factor;
        //     }
        //     //var pmoveImg_top = 900 - parallax_y * Math.pow(1.5, 1.8);// * Math.pow(1.2,2);
        //     // var base = 1.5;
        //     //var base = 1.5;
        //     //var exponent = 1.8;
        //     //var pmoveImg_top = G.pmoveImg_top_start_variable - parallax_y * Math.pow(base, exponent);// * Math.pow(1.2,2);

        //     var inflection_point = 800; //is_mobile ? 600 : 800; //when pMoveImg changes direction a bit; we calculate differently
        //     var divisor = 1800; //1200; //2500 //the degree of this change; lower the more sideways it goes;
        //     var slope = 1.9; //2.5; //2.1
        //     var mult = G.scroll_top > inflection_point ? slope - (G.scroll_top - inflection_point) / divisor : slope;
        //     var pmoveImg_top = G.pmoveImg_top_start_variable - parallax_y * mult;


        //     var disappear_point1 = 100;  //when at near top, then hide surfer; sometimes, depending on billboard rotoate style, will be visible
        //     var disappear_point2 = 2000;
        //     var z = G.scroll_top > disappear_point2 || G.scroll_top < disappear_point1 ? -3 : -1;
        //     // var disp = G.scroll_top > disappear_point2 || G.scroll_top < disappear_point1 ? "none" : "inline";

        //     var top_height = pmoveImg_top + parseInt( $("#pmove").css("height") );
        //     var disp =  top_height < G.scroll_top || pmoveImg_width < 0 || G.scroll_top > disappear_point2 || G.scroll_top < disappear_point1 ? "none" : "inline";
        //     var disp =  top_height < G.scroll_top || pmoveImg_width < 0 || z == -3 ? "none" : "inline";

        //     //var z = G.scroll_top > disappear_point2 ? -3 : -1;
        //     //var disp = G.scroll_top > disappear_point2 ? "none" : "inline";


        //     //## zoom effect
        //     if (G.pmove_zoom_ori === undefined) {
        //             //keep track of original width
        //             G.pmove_zoom_ori = parseInt( $("#pmove").css("width") );
        //     }
        //     var zoom = parseInt( Number(G.pmove_zoom_ori) + Number(G.scroll_top) / 8 ); //zoom amount


        //     //## do pmove rotation effect
        //     if (G.top_old === undefined) {
        //             G.top_old = G.scroll_top;
        //     }
        //     var diff = Math.abs(G.scroll_top - G.top_old);
        //     //do rotation only at ever 300px interval
        //     if (diff > 300) {

        //             var doRotate = function() {
        //                     degree_current = degree_old + step;
        //                     degree_old = degree_current;
        //                     var rotate = "rotate(" + degree_current + "deg)";
        //                     $(pmoveImg).css({"transform": rotate});

        //                     if (step > 0 && degree_current >= degree_new ||
        //                         step < 0 && degree_current <= degree_new ) {
        //                             G.degree_old = degree_new;
        //                             clearInterval(rotateTimer);
        //                     }

        //             };

        //             if (rotateTimer !== undefined) {
        //                     G.degree_old = degree_current;
        //                     clearInterval(rotateTimer);
        //             }

        //             G.top_old = G.scroll_top; //set new marker
        //             var sign  = Math.floor( Math.random() * 10 ); //get random index number for our array;
        //             var num = sign > 4 ? 50 : -50; //negative or positive rotation degree; multiply this with random result;
        //             var degree_new  = Math.floor( Math.random() * num ); //get random index number for our array;
        //             var degree_current;

        //             if (G.degree_old === undefined) {
        //                     var degree_old = 0;
        //             } else {
        //                     var degree_old = G.degree_old;
        //             }

        //             var diff = degree_new - degree_old;
        //             //rotation step; better to use value greater than 1; 1 is too slow;
        //             if (diff > 0) {
        //                     var step = 5;
        //             } else {
        //                     var step = -5;
        //             }


        //             var rotateTimer = setInterval(doRotate, 1); //the interval seems to make no difference here! Can't go fast.

        //             // var rotate = "rotate(" + degree_new + "deg)";
        //             //$(pmoveImg).stop().animate({transform: "rotate(50deg)"}, 250); //can't get it to animate; doesn't work
        //             // $(pmoveImg).css({"transform": rotate});

        //     }


        //     //## implement CSS changes to create effect
        //     $(pmoveImg).css({
        //             "width" : pmoveImg_width,
        //             //"left": pmoveImg_left,
        //             "top": pmoveImg_top,
        //             "z-index": z,
        //             "display":disp //show or not show
        //     });


        //     // Doing zoom below
        //     // //## implement CSS changes to create effect
        //     // $(pmoveImg).css({
        //     //         "left": pmoveImg_left,
        //     //         "top": pmoveImg_top,
        //     //         "width": zoom + "px", //change zoom width for img parent
        //     //         "z-index": z,
        //     //         "display":disp //show or not show
        //     // })
        //     // //change zoom width for img
        //     // .find("img").css("width", zoom + "px");

        // })(); //doPmoveImg


        // (function do_last_wallpaper_billboard() {
        // //last wallpaper billboard; #5 child


        //         var bannerbg = $("#billboardHome_site .billboard#billboard_bottom_bg"); //last wallpaper

        //         var aPos = $("#billboard_bottom_fg").position();
        //         var tp = parseInt(aPos.top) - 300;

        //         var bott = G.scroll_top + G.viewportal_height;

        //         // alert(tp + ", " + bott);

        //         var when_show = bott;
        //         var z = tp < when_show ? -1 : -3;
        //         var disp = tp < when_show ? "inline" : "none";
        //         $(bannerbg).css({
        //                 "z-index": z,
        //                 "display": disp,
        //                 "top":"0px"
        //         });

        // })();


        //
            //note: both using div and bg has issues; using div, can't click;
            //using bg, then have to repeat the image twice in the div, make
            //opacity 0, and have to set bg in js or remove bg when at
            //different page;

            // if trying to use background instead
            //var y_pos = parseFloat( $(d).css("top") );
            //var y_pos = -450;
            //var y1 = 200 - Number(scrolled * 0.25);
            //var y2 = -450 + Number(scrolled * 0.6);
            //var pos1 = $("body").css("background-position");
            //var y_pos = pos1.split(" ");
            //y_pos = parseFloat( y_pos[1] );
            //$("body").css("background-position", "0px " + y1 + "px");

    }

};


/////////////////////////////////////////////////////////////////


var G = {
    // is_ssl : null,
    // baseUrl : null,
    // baseUrlS : null,
    // viewportal_width : null
};

var lib = {
    // Note: Not all lib functions are here; many removed for brevity; check mudloft and others

    doLinkCopy : function (linkVal, ths) {

        //create temporary html element; throw in our variable; select it;
        // var tempHtml = $("<input id=\"tempInput\" type=\"text\">").val(linkVal).appendTo("#fileSection").select();
        var tempHtml = $("<input id=\"tempInput\" type=\"text\">").val(linkVal).appendTo("#contentDiv").select();

        //then copy that selection to clipboard
        document.execCommand("copy");

        //remove temp element
        // $("#homeArticle").empty("#tempInput");
        $("#tempInput").remove();

        //not sure what the problem is; delay doesn't seem to be working; and when I try to
        //use "this" inside the settimeout function, doesn't work;
        //https://stackoverflow.com/questions/4544126/jquery-delay-not-working
        //apparently, addClass doesn't work in a "queue"
        // var ths = $(this);
        //delay is jquery; setTimeout is js;
        // $(this).addClass("file_linkcopy_clicked"); //.delay(400).parent("file_copy").removeClass("file_linkcopy_clicked");

        //change the copy LInk text to red by adding a class; then remove it with settimeout

        // var addremove = $(ths).addClass("file_linkcopy_clicked");
        // setTimeout(function(){
        //     //remove the class and put back the original copy link text
        //     addremove.removeClass("file_linkcopy_clicked"); //setting a variable seems to work; not sure why...
        // }, 400);
    },

    hasAttr: function(ths, name) {
        //pass in $(this) and attr name (eg, required)

        //if attr exists, then typeof should be "string"; if not exist, then "undefined"
        var $result = typeof( $(ths).attr(name)) != "undefined" ? true : false;
        return $result;
    },

    formInputCheck : function(domParent) {
        //pass in the dom parent; this method checks all child input and textarea fields
        //that it has a value;  if not, adds "error" class;
        //only checks elements where display is not NONE and has attr REQUIRED
        //domParent should be an ID; tried passing in #formSection, but passing in #
        //doesn't seem to work

        var allGood = true,
            password = false;

        $("#" + domParent + " input, #" + domParent + " textarea").each(function() {

            if ( $(this).css("display") != "none" && lib.hasAttr($(this), "required") ) {

                //note: this method doesn't check for spaces before and after text

                //check for blank
                if (!$(this).val().trim()) {
                    $(this).addClass("error");
                    allGood = false;
                }

                //do email checks on input type email
                if ($(this).attr("type") == "email") {
                    var result = lib.checkEmail($(this).val());
                    if (!result) allGood = false;
                }

                if ($(this).attr("type") == "password" && !password) {
                    //store our first password; then check if
                    //there's another that we must check against
                    password = $(this).val();
                }
                //if we already have a prior stored password
                else if ($(this).attr("type") == "password" && password)  {
                    var password2 = $(this).val(); //this is our 2nd password
                    if (password !== password2) {
                        $(this).addClass("error");
                        allGood = false;
                    }
                }
            }
        });

        return allGood;
    },

    refreshMain : function(url) {

        (function doAjax() {

            //var url = getBaseUrl() + "/ajax/";
            //var url = G.ajaxUrl;

            var p_action  = "refreshMainFiles";
            var param     = "action=" + p_action;

            $.post(url, param, function(result) {

                var marr = result.split(";");
                if (marr[0] != "ok") {
                    //document.body.style.cursor = "wait";
                    return; //there was an error...
                }

                //our new main files
                var $html = lib.ajaxdecode( marr[1] );

                $("#contentDiv").hide();
                // $("#contentDiv").html($html).fadeIn(0);
                $("#contentDiv").html($html).show(0);
                //$("#contentSection").html($html).slideDown();
            }).fail(function(request, status, err) {
                //status: "timeout", "error", "abort", and "parsererror"
                //error: textual portion of the HTTP status
                alert(request);
                alert(status);
                alert(err);
            });

        })();

    },

    checkEmail : function(str) {
      /// check for invalid email; called by signin and register
            /// S = non white character
            /// + = match 1 or more
            var pattern = /\S+@\S+\.\S+/;

            var result = pattern.test(str); /// return true/false

            return result;
    },

    lcFirst : function(str) {
    // converts first letter of string to lowercase

            var newStr = str.charAt(0).toLowerCase() + str.substr(1);
            return newStr;
    },

    ucFirst: function(str) {
    // converts first letter of string to uppcase

            var newStr = str.charAt(0).toUpperCase() + str.substr(1);
            return newStr;

    },

    tab_to_next_input : function(elemInput, thisName) {
    // elemInput = the element to loop over with .each
    // thisName = name of input element we keyed down

        var name0 = thisName;
        var name1;
        var found = false;
        var arr = new Array();
        var inputFilled = true;

        $(elemInput).each(function() {  //$(".formInputDiv :input").each(function() {
                if ( $(this).is(":visible") ) {
                        var iValue = $.trim( $(this).val() );
                        if (iValue == "") {
                                inputFilled = false;
                        }

                        name1 = $(this).attr("name");
                        arr.push(name1);
                }
        });

        if (inputFilled == true)    return true;

        for (var i = 0; i < arr.length; i++) {
                name1 = arr[i];
                if (found) {
                        // the small delay will allow the default behavior
                        // to take place before we tab; the default might be autofill;
                        setTimeout(function() {
                                $("input[name=" + name1 + "]").focus();
                        }, 50);
                        return false;
                }

                found = (name1 == name0) ? true : false;
                i = (i == arr.length - 1) ? -1 : i;
        };

    },

    ///////////////////////////////////////////
    imgRowCell : function() {

    },

    imgRowCellRndMove : function() {

            if ( $(".productRowDiv").length < 1 ) return false;
            /*
            //this makes the rows artificially tighter or higher up than normallly
            var count = 0;
            $(".productRowDiv").each(function() {
                    var v = 10;
                    count = count - v;

                    $(this).css({
                            "position": "relative",
                            //"left": l,
                            "top": count
                    });
            });
            */
            //this randomizes the cell position inside the rows
            //var c = $(".productRowDiv:first .productListCellDiv").length;
            //var count = -1;
            $(".productListCellDiv").each(function() {

                    var hOffset = 17;
                    var vOffset = 25;
                    var l = Math.floor( Math.random() * hOffset ); //horizontal offset
                    var t = Math.floor( Math.random() * vOffset ); //vertical offset
                    var z = Math.floor(Math.random() * 50); // set random z-index for cells
                    var sign_l = Math.floor(Math.random() * 2 + 1); //1 or 2
                    var sign_t = Math.floor(Math.random() * 2 + 1); //1 or 2

                    //sign_l = sign_l == 1 && count != 0 ? -1 : 1;
                    sign_l = sign_l == 1 ? -1 : 1;
                    sign_t = sign_t == 1 ? -1 : 1;
                    //z = z == 1 ? 10 : "default"; //randomize z-dinex; some on top; some bottom
                    //z = "default"; //randomize z-dinex; some on top; some bottom

                    l = l * sign_l;
                    t = t * sign_t;

                    $(this).css({
                            "position": "relative",
                            "left": l,
                            "top": t,
                            "z-index" : z
                    });
            });
    },

    imgFadeTo : function(i, run_imgRowCellRndMove) {
    //i=0 or 1; 0=fadeTo 0; 1= fadeTo 1
    // fadeTo images effect for all images between header and footer;
    // all images within #contentSection (excludes header, footer generally; but depends
    // on one's html design in schema html) are by default opacity < 1 in css; and only
    // by js do we make all images appear visible, creating that affect; and preventin
    // long load time affect for larger images or firs time visitors;

    // ** Note: since I put the billboards outside contentSEction, it's no longer
    // relevant to banenrs; and maybe I'll just keep it this way for now;

            // if i isn't passed, then assume 1;
            i = i === undefined ? 1 : i;
            // below, creating effect where images will load at
            //different speeds; not all at the same time;
            var n = 0;
            $("main img").each(function() {
            //$("#contentSection img").each(function() {
                    //I want to get a random number, but not too big or small;
                    do {
                        n = Math.random() * 10; //.200 * 10
                    }
                    while (n < 2 || n > 8); // 3 and 6

                    Math.floor(n); //make # an integer between 3 and 6; //7;
                    n = n * 100 + 50; // will be number between 350 and 550; //750;
                    $(this).fadeTo(n, i);
            });


            // whether to run this method; if undefined, then run; only if user
            //explicitly states FALSE do we not run this; will not run it when
            // "setProductCatSearchWidth" and lig.imgFadeTo methods are run
            // within same method or process; so don't want to repeat;
            if (run_imgRowCellRndMove !== false) {

                    lib.imgRowCellRndMove();
            }


            // **note: this js operation will actually insert a style="opacity: 1" attribute into all img elements
    },

    doMsgBox : function(title, msg, buttonsArr, fn) {
    // title of the dialog box, msg=message to display, buttons=buttons to display
    // fn is a param that is a custom function that will be called after usere clicks on buttons
    // buttonsArr is optional; fn is optional; but ifno buttons, then make sure you put a timer in fn to close

        var show = function() {

            var doButtons = function() {
            // accepted buttons are: okay, cancel
                var okay_btn   = "<div class=\"sBtn\" id=\"msgBox_okay_btn\">OK</div>";
                var cancel_btn = "<div class=\"sBtn\" id=\"msgBox_cancel_btn\">CANCEL</div>";
                var close_btn  = "<div class=\"sBtn\" id=\"msgBox_close_btn\">CLOSE</div>";


                var html = "";
                if ( buttonsArr instanceof Array && buttonsArr.length > 0 ) {
                    for (var i = 0; i < buttonsArr.length; i++) {
                        if ( buttonsArr[i] == "OK" ) {
                                html += okay_btn;
                        }
                        else if ( buttonsArr[i] == "CANCEL" ) {
                                html += cancel_btn;
                        }
                        else if ( buttonsArr[i] == "CLOSE" ) {
                                html += close_btn;
                        }
                        //We could also allow custom buttons...
                    };
                }

                // if not array, or user put in no accepted parameters, & no function, then use default;
                if (!fn && html == "") {
                    html = okay_btn;
                }
                return html;

            };

            var attach_events = function() {

                $("#msgBox").on("click", "#msgBox_cancel_btn, #msgBox_okay_btn, #msgBox_close_btn", function() {
                    //Idont' remember what my original intention was with this function; not sure if there's an
                    //easier wayt o do it than the way I'm doing it below...

                    //if ( buttonsArr instanceof Array && buttonsArr.length > 0 ) {
                    if (fn) {
                        if ( $(this).attr("id") == "msgBox_okay_btn" ) {
                            customFn("OK");
                            // return "okay";
                        }
                        else if ( $(this).attr("id") == "msgBox_cancel_btn" ) {
                            customFn("CANCEL");
                            // return "cancel";
                            ///alert("cancel");
                        }
                        else if ( $(this).attr("id") == "msgBox_close_btn" ) {
                            // alert("attaching");
                            customFn("CLOSE");
                            // return "okay";
                        }
                    }

                    lib.doMsgBox(); //toggle msgBox and background

                });
            };

            // expect sender to hent the string; may want to include html...
            // title = lib.hent(title);
            // msg = lib.hent(msg);

            var h = "";
            h += "<div id=\"msgBox\">";
                h += "<h4>" + title + "</h4>";
                h += "<div id=\"msgBox_msg\">" + msg + "</div>";
                h += "<div id=\"msgBox_btns\">" + doButtons() + "</div>";
            h += "</div>";

            $("body").append(h);
            // $("#msgBox").show(0);
            lib.getViewportCenter("#msgBox", true);
            // $("#msgBox").hide(0);
            attach_events();
            $("#msgBox").fadeIn();

            //if custom function and no buttons, then run function here
            if (fn && buttonsArr.length < 1) {
                customFn();
            }

        }; // show

        var hide = function() {
            $("#msgBox").remove();
        }; // hide

        //if a custom function was sent, then create it; will call it when user clicks on button
        if (fn) {
            var customFn = function(param) {
                //param = okay, cancel or close
                fn(param);
            }
        }

        if ( $("#msgBox").length > 0 ) {
            hide();
            lib.dobg(false); // show or hide background
        } else {
            show();
            lib.dobg(true); // show or hide background
        }

        // lib.dobg(); // show or hide background

    },


    dobg : function(toggle) {
    //Call to this background function will toggle it, creating or removing it from the dom



        // This should work... if no arg passed, then toggle based on .bigDiv element; so if just
        // working with a single modal window, then don't have to pass any arg; use as before;
        // if you explicitly want to create multiple modal windows, then pass true to stack bg
        if (toggle === undefined) {
            toggle = $(".bgDiv").length > 0 ? false : true;
        }


        if (toggle === true) {

            var el = $(".bgDiv").length > 0 ? "bgDiv2" : "bgDiv";

            var bg = "<div class=\"" + el + "\"></div>";
            $("body").append(bg);
            $("." + el).animate({
                opacity: .6
            }, 250)
        }
        else {

            var el = $(".bgDiv2").length > 0 ? "bgDiv2" : "bgDiv";

            $("." + el).animate({
                opacity: 0
            }, 250, function(){
                $("." + el).remove();
            })
        }


        // if ( $(".bgDiv").length > 0 ) {
        //     $(".bgDiv").animate({
        //         opacity: 0
        //     }, 250, function(){
        //         $(".bgDiv").remove();
        //     })
        // }
        // else {
        //     var bg = "<div class=\"bgDiv\"></div>";
        //     $("body").append(bg);
        //     $(".bgDiv").animate({
        //         opacity: .4
        //     }, 250)
        // }


    },

    getViewportCenter : function(element, setCss) {
    // center passed element on viewable browser port or screen

            var h = $(window).height(); // returns height of browser viewport
            var t = $(document).scrollTop(); // get top position relative to browser
            // var center = t + Math.round( h * .5 ); // calculate vertical middle of browser screen
            var center = t + Math.round( h * .3 ); // calculate vertical 1/3 of browser
            // if element is passed, then get height of element and calc center of this element relative to screen coordinates;

            // seems the first formula should be better, but 2nd seems to actually center better... will have to see with
            //more trials... 3/19
            var top = ( typeof element === "undefined" ) ? center : center - ( $(element).height() / 2 );
            // var top = ( typeof element === "undefined" ) ? center : center - ( $(element).height() );


            top = top < 0 ? 0 : top; // if screen height is shorter than image height, then make top of image 0; don't let go into negative

            // whether to set css; if this is not set or false, then false; otherwise, true
            setCss = ( typeof setCss === "undefined" || setCss === false ) ? false : true;

            // vertically and horizontally center element;
            // better to put here? or all in CSS file????
            if ( setCss && typeof element !== "undefined" ) {
                    $(element).css({
                        "top":top
                    });
                    return false;
            } else {
                    return top;
            }

    },
    //doSpinner : function(element, t_offset, l_offset, w) {
    doSpinner : function(obj) {
    // with the spinner, we can either pass in no parameter, and this function will center the spinner with default size;
    // or we can pass in a size; or we can also pass in an element with offsets top and left offset values
            // if spinner exists, then remove it and exit;
            if ( $("#spinnerContainer").length > 0 ) {
                    $("#spinnerContainer").remove();
                    $(".bgtDiv").remove(); //remove transparent background
                    lib.doCursor("default");
                    return false;
            }


            lib.doCursor("wait");
            // create transparent background; do this to prevent user from clicking on anything
            var bg = "<div class=\"bgtDiv\"></div>";
            $("body").append(bg);

            var element  = false; // if not set, then center on screen
            var size     = ""; // if not set, then us css default
            var t_offset = 0; // if element set, then see if top offset is given; other, zero
            var l_offset = 0; // left offset, or zero; if element not set, then not applicable;

            var spinner = "<div id=\"spinnerContainer\"></div>";
            $("body").append(spinner);

            // check if parameter passed in; then use those values;
            // otehrwise, do default;
            if (typeof obj !== "undefined") {

                    // if passed in, callers should have passed in an object parameter like this:
                    // var obj = {
                    //         "pos": "center",
                    //         "element": (name of element),
                    //         "size" : "400px", //width/height
                    //         t_offset: "50",
                    //         l_offset: "50",
                    // };

                    element  = ( obj.element  === "undefined" ) ? element  : obj.element;  // relative to an element
                    t_offset = ( obj.t_offset === "undefined" ) ? t_offset : obj.t_offset; // vertical offset
                    l_offset = ( obj.l_offset === "undefined" ) ? l_offset : obj.l_offset; // horizontal offset
                    size     = ( obj.size     === "undefined" ) ? size     : obj.size;     // size: width, height
            }

            if (element) {
                    var pos = $(element).position();
                    var top = pos.top - t_offset;
                    var left = pos.left - l_offset;
                    $("#spinnerContainer").css({"left":left, "top":top, "width":size, "height":size}).toggle();
            }

            // center spinner
            else if (!element) {
                    // false: tell function not to set css
                    var top = lib.getViewportCenter("#spinnerContainer", false);
                    $("#spinnerContainer").css({"top":top, "width":size, "height":size}).toggle();
            }


    },


    currToNum: function(curr) {
            // make sure passed is being treated as string so we can do the replace procedure
            curr = curr.toString();
            curr = curr.replace("$", "");
            return curr;
    },

    numToCurr: function(num) {

            // make sure the num is being treated as a string; or else get error
            num = num.toString();

            num = num.replace("$", "");  //remove dollar

            var isNeg = num.indexOf("-") === 0 ? true : false; // check if neg sign exists
            num = num.replace("-", ""); //remove - sign
            var arr = num.split("."); //split integer portion and float portion
            var int = arr[0] == undefined || arr[0] == "" ? "0" : arr[0];
            var fl = arr[1] == undefined || arr[1] == ""  ? "00" : arr[1];

            var curr = int + "." + fl;

            // round float point to 2 digits

            curr = Number(curr).toFixed(2);


            curr = curr == "NaN" ? "0.00" : curr; // if result was "NaN", then make zero

            curr = "$" + curr;
            curr = isNeg ? "-" + curr : curr;
            return curr;


    },


    getGuid: function() {
    // returns our unique guid; should match our guid found in FunctionLib.php
    // Not using this for anything at the moment; used it before for ajax;

            //todo:: don't need this!
            var guid = "2E7CF555-AC8B-4780-B3FA-921E5A84B960";
            return guid;
    },


    doCursor: function(kind) {
    // kind = wait or default
            //document.body.style.cursor = kind;
            //if ( document.body.style.cursor === "default" ) {

            var c1 = document.body.style.cursor;
            var c2 = ( c1 == "" || c1 == "default" ) ? "wait" : "default";

            if (kind == "wait") {
                    document.body.style.cursor = "wait";
            } else {
                    document.body.style.cursor = "default";
            }

            return false;
    },


    hent: function(str) {
    // mimicking a little of php's htmlentities function;
    // Since I'm only doing the limited set below, it's equivalent
    // to PHP's htmlspecialchars

    // Note:
    // While text() will output the literal character as the screen renders it and html() will
    // output whatever the original html characters are; effectively, appear
    // the same when shown in an input field;
    // and for some reason, js seems to take the entity version
    // of " and ' and convert back to " and ', respectively; very strange!
    // So again, the hitch is that text() will not give me the literal text for " and ';
    // &quot; becomes --> ", rather than the original! this is a bug here!

            if ( str.indexOf("&amp;") == -1 && str.indexOf("&quot;") == -1 &&
                 str.indexOf("&#039") == -1 && str.indexOf("&lt;") == -1 &&
                 str.indexOf("&gt;") == -1 && str.indexOf("&") >= 0 ) {

                    str = str.replace(/&/g, "&amp;");
            }

            if ( str.indexOf("&lt;") == -1 && str.indexOf("<") >= 0 ) {
                     str = str.replace(/</g, "&lt;");
            }
            if ( str.indexOf("&gt;") == -1 && str.indexOf(">") >= 0 ) {
                    str = str.replace(/>/g, "&gt;");
            }
            //if ( str.indexOf("&quot;") == -1 && str.indexOf('"') >= 0 ) {
            if ( str.indexOf('"') >= 0 ) {
            //    alert("yes");
            //if ( str.indexOf("&quot;") == -1 ) {
                    str = str.replace(/"/g, "&quot;");
            //        alert(str);
            }
            if ( str.indexOf("&#039") == -1 && str.indexOf("'") >= 0 ) {
                    str = str.replace(/'/g, "&#039");
            }

            return str; //.replace(/"/g, "&quot;");


            // for " and ', we always do!
         /*   return str
                       //.replace(/&/g, "&amp;")
                       .replace(/"/g, "&quot;")
                       .replace(/'/g, "&#039")
                       .replace(/</g, "&lt;")
                       .replace(/>/g, "&gt;")
                       ;
        */


    },


    // #### Ajax Functions ####
    // encodeajax: function(str, exclude) {
    ajaxencode: function(str, exclude) {


            //return encodeURIComponent(str);
            var ns = encodeURIComponent(str);
            //substring
            //indexOf

            //if no value given for exclude, then will be "undefined";
            //if (exclude == "/") {

            // ***** 12/18 note: Should I really be removing this???? It screws up the url!
            //note: if user put / in string, then remove it; this, when
            //encoded, will throw an error with apache; see apache notes
            //for more info on this; there is a workaround but my version
            //of apache is not new enough;
            //  if ( ns.indexOf("%2F") > -1 ) {
            //         ns = ns.replace("%2F", "");
            //  }
            //*******************
            //}
            return ns;
    },
    // decodeajax: function(str) {
    ajaxdecode: function(str) {
            return decodeURIComponent(str);
    },


    // #### Cookie functions ####
    // * Modified from Nicholas Zakas *
    // js reads the entire cookie, which is a semicolon separated string; then we have to parse that string;
    // ex: alias=Aquaman2; idNo=%7B8%D; PHPSESSID=gmq11v1unankkbv0
    cookieget: function (name){
        var cookieName = encodeURIComponent(name) + "=",
            cookieStart = document.cookie.indexOf(cookieName),
            cookieValue = null,
            cookieEnd;

        if (cookieStart > -1) {
                cookieEnd = document.cookie.indexOf(";", cookieStart);
                if (cookieEnd == -1) {
                        cookieEnd = document.cookie.length;
                }

                // attempt to decode some character, like %, will result in error for whatever reason
                try {
                        cookieValue = decodeURIComponent( document.cookie.substring(cookieStart + cookieName.length, cookieEnd) );
                }
                catch(e) {
                        cookieValue = "decodeError";
                }
                finally {
                        //var x = (x == undefined) ? "error" : x;
                }

        }
        return cookieValue;
    },
    //set: function (name, value, expires, path, domain, secure) {
    // cookieset: function (name, value, m) {
    cookieset: function (name, value, h) {
        // 11/19; changes minutes to hours
        // m = minutes till expiration
        // h = hours till expiration

        //if (expires instanceof Date) { cookieText += "; expires=" + expires.toUTCString(); }
        //if (path) { cookieText += "; path=" + path; }
        //if (domain) { cookieText += "; domain=" + domain; }
        //// tells browser to only transmit if over ssl connection
        //if (secure) { cookieText += "; secure"; }
        //var now2 = now.getTime();       // convert date object to milliseconds
        //document.cookie = "searchSortBy=date;max-age=" + (60*60*24*365); // in seconds
        //if (expires instanceof Date == false) {
        //-----------------------------------------------------------------------------


        var cookieText  = encodeURIComponent(name) + "=" + encodeURIComponent(value);
            cookieText += "; path=/"; // set path to root
            cookieText += "; secure";
            cookieText += "; domain=" + document.location.host;

        //if (domain) { cookieText += "; domain=" + domain; }

        // assuming h is set, then set day and hrs to 1
        var d = 1;
        var m = 60;

        // if m is not set, then set default values: 180days
        if ( typeof h != "number" ) {
                d = 180;
                h = 24;
                m = 60;
        }

        //           ms   seconds
        var offset = 1000 * 60 * m * h * d;         // time in milliseconds, in days
        var dateMs = Date.now() + offset; // today's date in milliseconds + offset

        var expires = new Date(dateMs);                 // translate our millisecond as a date object, standard date format

        expires = expires.toUTCString()             // convert local time to UTC time
        cookieText += "; expires=" + expires;       // add our exp. date to cookie;
        document.cookie = cookieText;               // save our unencrypted string to cookie
        return true;
    },

    //unset: function (name, path, domain, secure){
    cookieunset: function (name){
        // 11/19: NOTE:: haven't tested this
        //this.set(name, "", new Date(0), path, domain, secure);
        // this.cookieset(name, "", new Date(0)); // this should prob be a negative number
        this.cookieset(name, "", -100); // this should prob be a negative number
        return true;
    }

};

/////////////////////////////////////////////////////////////////

// Drag & Drop
$(function() {

    // setTimeout(function() {
    if ( $("#dropSection").length < 1 ) return false;

    var
        // holder = $(".dropBox");
        xhr = null,

        tests = {

            // Whether typof FileReader object is not undefined??
            can_filereader: typeof FileReader != 'undefined',

            // Test whether elements are draggable
            can_draggable: "draggable" in document.createElement('span'),

            //whether the window has a FormData object?? I think...
            can_formdata: !!window.FormData,

            //https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/in
            //The in operator returns true if the specified property is in the specified object or its prototype chain.
            can_progress: "upload" in new XMLHttpRequest
        };

        //////
            /*support = {
                filereader: document.getElementById('filereader'),
                formdata:   document.getElementById('formdata'),
                progress:   document.getElementById('progress')
            },*/

            /*acceptedTypes = {
                'image/png':  true,
                'image/jpeg': true,
                'image/gif':  true
            },*/
            //progress = document.getElementById('uploadprogress'),
            //classic_fileupload = document.getElementById('upload');

    function readfiles_error (response) {
    //var readfiles_error = function (response) {
        //check for errors on drag/drop and upload

        if (response === "filesize_zero") {
            var msg = "Unknown file error.";
            lib.doMsgBox("File Error", msg, ["close"]);
            return false;
        }
        if (response === "filename_toolong") {
            var msg = "File name is too long.";
            lib.doMsgBox("File Error", msg, ["close"]);
            return false;
        }
        if (response === "filesize_toobig") {
             var msg = "File is too big.";
            lib.doMsgBox("Size Limit", msg, ["close"]);
            return false;
        }
        if (response === "files_onlyonefilepermitted") {
             var msg = "Please select one file to upload. Signup to upload multiple files.";
            lib.doMsgBox("File limit", msg, ["close"]);
            return false;
        }
        if (response === "formdata_error") {
             var msg = "Browser form data error.";
            lib.doMsgBox("Form Data", msg, ["close"]);
            return false;
        }
        if (response === false) {
            var msg = "Sorry. Unknown error.";
            lib.doMsgBox("Unknown Error", msg, ["close"]);
            return false;
        }

        return true;
    }

    function readfiles(files, ths, sender) {
    //var readfiles = function(files, ths, sender) {
        /*
            ths = .dropBox element
            The debugger statement invokes any available debugging functionality,
            such as setting a breakpoint. If no debugging functionality is available,
            this statement has no effect. Acts like a breakpoint in the script source.
            debugger;
            sender = dragdrop or browse; doing this because mobile has some issues with uploading
            if there's an error with size=0 on mobile, then would rather show error message
            it seems this will be 0 if user drags a browser image into the dropbox;
            if it's a good file, then the implicit return is UNDEFINED; so when we check
            for response, we have to check specifically for false, precluding undefined
        */


        //if no files or somehow reads as empty (due to incompatibility), then return
        if (files.length < 1) return false;

        //if in home page, then check if user is logged in
        // var isSession = $("#dropSection").attr("sess");

        //if not signed in, then only allow 1 file at a time to be uploaded
        // if (!isSession && files.length > 1) {
        //     return "files_onlyonefilepermitted";
        // }

        // check that file name isn't too long and size isn't 0
        // Size may be 0 if user tries to upload a folder or some other weird thing
        // note that I have a limit of 200 str length here, but when displaying, I limit to a shorter size
        var maxstringlength = 100;
        for (var i = 0; i < files.length; i++) {
            // var n = files[i].name;
            if (files[i].name.length > maxstringlength) {
                return "filename_toolong";
            }
            if (files[i].size === 0) {
                //on mobile, many times will have 0 size for whatever reason;
                //don't know how to fix it!
                return "filesize_zero";
            }
        }

        //or give message that browser can't do "FormData";
        if (!tests.can_formdata) {
            return "formdata_error"; //false; //would also need to reset drop form
        }


        var formData = new FormData();

        //## add xhr parameters
        // formData.append("action", "file_upload"); //action param = file_upload
        formData.append("action", "file_articleImgUpload"); //action param = file_upload
        // formData.append("isSession", isSession);    //whether the user is apparently logged in or not

        // dir path for file upload
        formData.append("dir_path", $("#articlesNewEdit").attr("dir_path"));

        // if registered user is in standard file upload page
        //var maxsize = false;
        //if ($("#userFilepageSection").length > 0) {
        //    // disk space available
        //    maxsize = $("#filesTitle").attr("kbAvail");
        //}

        //if user is not in standard upload page, then check the kbAvail attr in filesTitle under Home page
        //remember that the userFilePageSection also has the same #fileTitle element
        // else if ($("#homeArticle #filesTitle").length > 0) {
        //     maxsize = $("#filesTitle").attr("kbAvail");
        // }

        //now check again if we have a maxsize; if not, then use default max size; user may just be
        //an unregistered one-time uploader
        // maxsize = maxsize ? maxsize : $("#dropSection").attr("unregFileMaxSize");

        var maxsize = parseInt($("#dropSection").attr("max_file_size")) * 1024; //convert mb to kb


        var fsize = 0; //upload fize size (excluding headers, etc)
        //insert files to formData object
        for (var i = 0; i < files.length; i++) {
            //alert(files[i].size);
            // formData.append("file_" + i, files[i]);
            //to be able to do multiple, have to pass variable as array
            //https://developer.mozilla.org/en-US/docs/Web/API/FormData/append
            // alert(files[i].name); //name of files
            //alert(files[i].size); //size of files in bytes
            //alert(files[i].type); //MIME type of files, e.g. image/jpeg, text/plain, etc.
            //previewfile(files[i]); //what is this?? don't remember what previewfile is
            fsize += files[i].size;
            formData.append("file[]", files[i]);

        }

        fsize = Math.ceil(fsize / 1024); //convert bytes to kb

        //check that file size doesn't exceed limit
        //here, comparing bytes with bytes
        if (fsize > maxsize) {
            return "filesize_toobig";
        }

        //create our xhr object
        xhr = new XMLHttpRequest();

        //init ajax
        // xhr.open('POST', '/devnull.php');
        xhr.open("POST", G.ajaxUrl, true); //true, by default, asynchronous;

        var progress = $(ths).parent().find("progress");
        var progressContainer = $(ths).parent().children(".progressContainer");
        progressContainer.fadeIn(20);

        //when finished; blank code
        xhr.onload = function() {
            //this event triggers after onreadystatechange

            // progress.value = progress.innerHTML = 100;
            //$(ths).parent().children("progress").html("100");
            // progress.html("100"); //this odesn't seem to do anything
            //alert(progress.html());

            // alert("done");
            // progress.fadeOut(5000);
            //progress.slideUp(1000);

            // progress.animate({
            //     "width": "0px",
            //     "margin-left": "100px"
            // }, 1000, function(){
            //     $(this).fadeOut(0);
            //     $(this).css({"width": "", "margin-left": "0"})
            // });
        };

        if (tests.can_progress) {

            var calc = function(size) {

                var unit;
                if (size >= Math.pow(1024, 3)) {
                    size = (size / Math.pow(1024, 3)).toFixed(3);
                    unit = "GB";
                }
                else if (size >= Math.pow(1024, 2)) {
                    size = (size / Math.pow(1024, 2)).toFixed(2);
                    unit = "MB";
                }
                else if (size >= 1024) {
                    size = (size / 1024).toFixed(1);
                    unit = "KB";
                }
                else {
                    unit = "Bytes";
                    //nothing for B, bytes
                }

                return [size, unit];
            };

            var loaded = 0,
                total  = 0, //total size of all files, excluding headers
                unit_loaded = 0,
                unit_total = 0,
                total2,
                loaded2,
                complete,
                msg,
                arr;

            xhr.upload.onprogress = function (event) {
                //has a length that can be calculated
                if (event.lengthComputable) {
                    // var loaded = Math.round(event.loaded / 1000); //get in KB
                    // var total = Math.round(event.total / 1000); //get in KB

                    // //the | is supposed to be a bitwise "or" operator; not sure
                    // var complete = (loaded / total * 100 | 0);
                    // //progress.value = progress.innerHTML = complete;

                    // var msg = complete + "%";
                    // msg += "<br>" + loaded + " of<br>" + total + " KB";

                    // $(ths).children(".section2").html(msg);
                    // // $(ths).parent().children("progress").attr("value", complete);
                    // progress.attr("value", complete);

                    // sizes are in bytes by default
                    total = event.total; //file total + headers, etc
                    loaded = event.loaded;


                    if (!unit_total) {
                        arr = calc(total);
                        total2 = arr[0];
                        unit_total = arr[1];
                    }

                    arr = calc(loaded);
                    loaded2 = arr[0];
                    unit_loaded = arr[1];

                    //the | is supposed to be a bitwise "or" operator; not sure; seems to be some kind of rounding calculation
                    complete = (loaded / total * 100 | 0);

                    msg  = complete + "%" + "<br>"
                               // + loaded + " " + unit + " of" + "<br>"
                               + loaded2 + unit_loaded + " of" + "<br>"
                               // + total + " " + unit;
                               + total2 + unit_total;

                    $(ths).children(".progress_msg").html(msg);
                    progress.attr("value", complete);
                }
            }
        }

        //File was uploaded... waiting for ajax reponse
        xhr.onreadystatechange = function () {

            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                //console.log(xhr.responseText);
                //https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
                var response = xhr.responseText;

                // alert(response);
                var arr = response.split(";");
                var result = arr[0];

                //off: remove the event handler (in this case, all .dropBoxContainer elements)
                $(".dropBoxContainer").off("click", ".upload_abort");
                var original_msg = $(ths).children(".progress_msg2").html();

                if (result === "ok") {
                    var qArr = arr[1].split(",");
                    var uploadedqty = qArr[0];
                    var totalqty = qArr[1];

                    $(ths).children(".progress_msg2").html("Upload complete!<br>" + uploadedqty + " of " + totalqty + " file(s)");

                    //insert updated/refreshed html into our dom
                    var refreshFiles = lib.ajaxdecode(arr[2])
                    $("#fileSection").hide().html(refreshFiles).show(10);

                    //let normal timer below work...
                    var timer = 2200; //set different timers for success and errors

                    //call shared method that sets buttons for files; enable/disable
                    shared.setMediaBtns();
                }

                //there was an error or file size exceeded limit
                else {

                    var type = arr[1];
                    if (type === "size") {
                        var msg = "Size limit error! The file is too big.";
                    }
                    //was apparently logged in but no longer logged in
                    else if (type === "session_mismatch") {
                        var msg = "Sorry, you're logged out. Login and try again."
                    }
                    //for any other kind of error, just generic message
                    else {
                        var msg = "File error! Please try again.";
                    }

                    $(ths).children(".progress_msg2").html(msg);

                    //set different timers for success and errors
                    var timer = 8000;
                }

                //reset our drop box
                setTimeout(function() {
                    $(ths).children(".progress_msg2").html(original_msg); //reset to original msg
                    $(ths).children(".dropToggle1, .dropToggle2").toggle(800);
                    progressContainer.fadeOut(800); //our our progressbar

                    xhr = null; //reset the xhr AFTER the timeout

                }, timer);

            }

        };

        //Abort upload; create abort click event
        $(".dropBoxContainer").on("click", ".upload_abort", function() {
            xhr.abort();
            progressContainer.fadeOut(100);
            //alert(progressContainer.html());
            //$(".progressContainer").fadeOut(100);
            xhr = null;
            $(".dropBoxContainer").off("click", ".upload_abort");

            //reset our message; toggle messages
            $(ths).children(".dropToggle1, .dropToggle2").toggle(200);
        })

        // send the data
        xhr.send(formData);

        //// Help links
            // https://www.html5rocks.com/en/tutorials/file/xhr2/
            // https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html
            // https://www.w3schools.com/js/js_ajax_http.asp  //old version
            // Possible Jquery implementation; haven't tested
            //https://stackoverflow.com/questions/15668339/can-onprogress-functionality-be-added-to-jquery-ajax-by-using-xhrfields
            // $.ajax({
            //     async: true,
            //     contentType: file.type,
            //     data: file,
            //     dataType: 'xml',
            //     processData: false,
            //     success: function(xml){
            //         // Do stuff with the returned xml
            //     },
            //     type: 'post',
            //     url: '/fileuploader/' + file.name,
            //     xhr: function(){
            //         // get the native XmlHttpRequest object
            //         var xhr = $.ajaxSettings.xhr() ;
            //         // set the onprogress event handler
            //         xhr.upload.onprogress = function(evt){
            //             console.log('progress', evt.loaded/evt.total*100)
            //         };
            //         // set the onload event handler
            //         xhr.upload.onload = function(){
            //             console.log('DONE!')
            //         };
            //         // return the customized object
            //         return xhr ;
            //     }
            // });


    }//readfiles


    //our drag/drop events
    if (tests.can_draggable) {

        //////////
            // var drag_leave;

            //make borders green on hover over
            // holder.ondragover = function() {
            // $(".dropBox").on("dragover", function() {

            //dragover fires every cursor move; have to set to false or drop event won't fire
            //false is shorthand way of returning false
            //https://stackoverflow.com/questions/19223352/jquery-ondrop-not-firing
            //unlike here, doesn't seem that I have to do .stopPropagation;

            //hook events to contentSEction because everythign in it will get refreshed and will
            //then lose event binding otherwise.
            //( $(".dropBox")
        ( $("#dropSection")

            //dragexit works for firefox, but not chrome; dragexit constantly fires
            // .on("dragexit, dragleave", function(event) {
            .on("dragleave", ".dropBox", function(event) {
                //event.preventDefault();
                //event.stopPropagation();

                if ( $(this).hasClass("dropBoxHover") ) {
                    $(this).removeClass("dropBoxHover")
                }
                return false;
            })

            //because I'm using dragleave for chrome, which constantly fires, forced to
            //use dragover, which also constantly fires
            // .on("dragenter", function(event) {
            .on("dragover", ".dropBox", function(event) {
                // this.className = 'drophover';
                //event.preventDefault();
                //event.stopPropagation();
                if (xhr !== null) return false;

                if ( !$(this).hasClass("dropBoxHover") ) {
                    $(this).addClass("dropBoxHover");
                }

                return false;
            })

            .on("dragend", ".dropBox", function(event) {
                //this never seems to fire
                // event.preventDefault();
                // event.stopPropagation();
                // alert("end");
            })

            .on("drop", ".dropBox", function(event) {
                event.preventDefault();
                // event.stopPropagation();
                if (xhr !== null) return false;

                //dataTransfer.files: Contains a list of all the local files available on the data transfer.
                //If the drag operation doesn't involve dragging files, this property is an empty list.
                //alert(event.dataTransfer.files);
                // https://stackoverflow.com/questions/15772249/jquery-pass-element-to-datatransfer-property
                //https://api.jquery.com/category/events/event-object/
                var response = readfiles(event.originalEvent.dataTransfer.files, $(this), "dragdrop");

                //remove the hover effect styling
                $(this).removeClass("dropBoxHover");

                //check if we got any error message back from readfile method; if no error, then
                //the readfiles method should be working and the code should asyncrhonously come
                //here; response then should be UNDEFINED; when we test for it, we should then
                //return true since RESPONSE has an undefined value;
                if (!readfiles_error(response)) return false;

                //if everything okay, then we immediately toggle to show the progress html
                //is it possible we get here BEFORE we get back a possible error message??
                $(this).children(".dropToggle1, .dropToggle2").toggle(200);
            })

        );//end .dropBox

    }//tests.can_draggable

    var init_other_events = function() {
        //We're hiding the standard html upload button and using js to click the hidden button when
        //user clicks on our alternate upload link
        ($("#dropSection")

            .on("click", ".imgMsg", function() {
                if (xhr !== null) return false;

                // $("#spinner").toggle();
                $("#uploadFileBtn").click();
            })
            .on("click", ".uploadFile_msg", function() {

                // $(this).parent().children("input[name=\"uploadFileBtn\"]").click();
                if (xhr !== null) return false;
                // $("#spinner").toggle();
                $(this).siblings("input[name=\"uploadFileBtn\"]").click();

            })

            // .on("change", "input[name=\"uploadFileBtn\"]", function(){
            .on("change", "#uploadFileBtn", function(){
                //if you want to display file name
                // $(this).siblings(".uploadFileName").html( $(this).val() );
                $(this).siblings(".uploadSubmitBtn").removeClass("disabled");
                // $("#spinner").toggle();

            })

            .on("click", ".uploadSubmitBtn", function() {

                if ( $(this).hasClass("disabled") ) return false;

                //get the files object from form to pass to our function
                //https://stackoverflow.com/questions/5392344/sending-multipart-formdata-with-jquery-ajax
                var ufile = $(this).siblings("input[name=\"uploadFileBtn\"]")[0].files;
                //ufile[0].size = 100;
                //alert(ufile[0].size);
                // alert(ufile.toString());
                // alert(JSON.stringify(ufile));
                //alert(String(ufile));

                var ths = $(this).parents(".dropBox");

                var response = readfiles(ufile, ths, "browse"); //////////////////////////////
                $(this).addClass("disabled");

                //var ths = $(this).parents(".dropBox").children(".dropToggle1, .dropToggle2");
                if (!readfiles_error(response)) return false;

                $(this).parents(".dropBox").children(".dropToggle1, .dropToggle2").toggle(200);

            })

        );//#dropSection
    }();//init_other_events



    // }, 1000);


});//$(function()


/////////////////////////////////////////////////////////////////


$(function() {
//////////////

if ( $(".billboardSection").length < 1 ) return false;

if ( $("#billboardGDPR").length > 0 ) {

    $("#billboardGDPR").on("click", "#okBtn", function(){


        // then: using a promise; wait for fadeout and then detach/delete it; seems to work;
        $("#billboardGDPR").fadeOut(300, function() {
            $(this).remove()
        });

        var name = "privacy",   // name of our gdpr cookie is "privacy"
            value = 1,          // set to true
            h = 24 * 30 * 12 * 2; //set this cookie for 2 years
        lib.cookieset(name, value, h);

    });

}

//////////////
});


/////////////////////////////////////////////////////////////////

$(function() {
//////////////


if ( $("#articleSection").length < 1 ) return false;

if ( $("#articleNewEdit").length > 0 ) {

    function file_delete_Ajax (file_path, row) {

        var p_action = "file_delete",
            p_file_path  = lib.ajaxencode(file_path),
            param    = "action=" + p_action +
                        "&file_path=" + p_file_path;

        $.post(G.ajaxUrl, param, function(result) {

            if (result == "ok" && row) {
                $(row).slideUp(300);
            }
        });
    }

    function toggleMediaSection(action) {
        // Open/close the media modal window

        if (action == "open") {
            //shared method that sets file buttons
            shared.setMediaBtns();
            $("#mediaSection").fadeIn();
        } else {
            $("#mediaSection").fadeOut();
        }

        lib.dobg(); // show or hide background
    };

    // this function does both previewing and posting
    function doPostPreview(sender) {

        var doAjax = function() {

            var param =
                "action="       + sender +
                "&articleNo="   + articleNo +
                "&status="      + status +
                "&pagelinkUrl=" + lib.ajaxencode(pagelinkUrl) +
                "&dateTime="    + lib.ajaxencode(dateTime) +
                "&headline="    + lib.ajaxencode(headline) +
                "&blurb="       + lib.ajaxencode(blurb) +
                "&imgUrl="      + lib.ajaxencode(imgUrl) +
                "&textBody="    + lib.ajaxencode(textBody) +
                "&tags="        + lib.ajaxencode(tags);

            $.post(G.ajaxUrl, param, function(result) {

                // alert( lib.ajaxdecode(result));

                var arr           = result.split(";"),
                    result_status = arr[0];

                // posting result
                if (result_status == "ok_post") {

                    if (arr[1] && !articleNo) {
                        $("input[name=articleNo]").val(arr[1]);
                    }

                    if (status == "D") {
                             var msg = "The article was deleted.",
                             caption = "DELETED",
                             customFn = function() {
                                window.location.href = G.baseUrl + "/browse/article/";
                            };
                            lib.doMsgBox(caption, msg, ["okay"], customFn);
                    }
                    else {

                            var msg = "The article was posted.",
                            caption = "SAVED",
                            customFn = function() {
                                setTimeout(function() {
                                    lib.doMsgBox();
                                }, 1500);
                            };
                            lib.doMsgBox(caption, msg, [], customFn);
                    }

                }

                // preview result
                else if (result_status == "ok_preview") {
                    var previewHtml = lib.ajaxdecode(arr[1]);
                    $("#previewTabSection").html(previewHtml);
                    shared.doLazy(); //trigger lazy
                }

                // error
                else {
                    var msg = "There was an error.";
                    lib.doMsgBox("Ooops!", msg, ["close"]);
                }

            });
        }; //ajax


        var articleNo   = $("input[name=articleNo]").val(),
            // status    = $("input[name=statusRadio]:checked").val(),
            status,
            pagelinkUrl = $("input[name=pagelinkUrl").val(),
            dateTime    = $("input[name=dateTime]").val(),
            headline    = $("textarea[name=headline]").val(),
            blurb       = $("textarea[name=blurb]").val(),
            imgUrl      = $("input[name=imgUrl]").val(),
            textBody    = $("textarea[name=textBody]").val(),
            tags        = $("textarea[name=tags]").val();

        // get status value
        $("#rowStatusRadio div").each(function() {
            var is_selected = $(this).hasClass("selected");

            if (is_selected) {
                var id = $(this).attr("id");
                status = id.split("_")[1]; //id name is formatted: status_A, status_N, etc
            }
        })

        doAjax();

    } // doPostPreview


    $("#contentTabSection").on("focus", ".rowField", function(){
    // record name of focused element; use for inserting html tags
    // actually, set global variable to the focused element

        //reset our last focused element name; use this variable to store our current focused element
        G.lastFocusedElement = "undefined";
        var idName = $(this).attr("id"); //get id name
        // only care if the id is imgUrl (blurb) or textBody
        if (idName == "imgUrl") {
            G.lastFocusedElement = $("input[name=imgUrl]");
        }
        else if (idName == "textBody") {
            G.lastFocusedElement = $("textarea[name=textBody]");
        }
    });

    // click on one of the status "radio" buttons
    $("#rowStatusRadio").on("click", "div", function(){
        $("#rowStatusRadio div").each(function() {
            $(this).removeClass("selected");
        })
        $(this).addClass("selected");

    });


    // $("#contentTabSection").on("blur", ".rowField", function(){

    //     var o = $("#mediaSection").css("opacity");
    //     var d = $("#mediaSection").css("display");

    //     alert(d);

    //     if (d == 0) {
    //         G.lastFocusedElement = "undefined";
    //     }
    // });


    $("#fileSection").on("click", ".delBtn", function(){

        // reset all delete questio marks to default X
        var delBtn_reset = function() {
            $(".delBtn").each(function() {
                $(this).html(defaultBtn);
            });
        };

        //get current value of button
        var currVal = $(this).html();

        //get default values for delete and confirm buttons
        var defaultBtn = $("#fileSection").attr("defaultBtn"); // X symbol
        var confirmBtn = $("#fileSection").attr("confirmBtn"); // ? symbol

        clearTimeout(G.deltimer);

        if (currVal == confirmBtn) {
            // parent: one element up, closest: first matching element up, parents: all matching elements up
            //https://stackoverflow.com/questions/9193212/difference-between-jquery-parent-parents-and-closest-functions

                       //get the file that is being deleted
            // var rowParent = $(this).closest(".file_row"); //.closest: traverse up and get first element that matches
            // var file_name_element = $(rowParent).children(".file_name");
            // var href = $(file_name_element).children("a").attr("href");

            //get folder/file combination name
            //closest finds the first matched parent or self; parent moves one dom up; parents selects ALL matching
            // var folder_file = $(this).closest(".fileinfo_container").attr("f_file");


            // /upub/media/articles/A01/1012/xx.png
            var file_path = $(this).closest(".file_row").children(".file_name").attr("file_path");
            var row = $(this).closest(".file_row"); //the row block eleement

            //do ajax to delete file; pass folder/file info for db; and html row to remove if successful
            // doAjax(folder_file, row);
            file_delete_Ajax(file_path, row);
            delBtn_reset(); //reset now; if ajax error, then good to go again

        } else {

            //if current selection is X, then reset other possible DEL?
            delBtn_reset();
            //set current selection to DEL?
            $(this).html(confirmBtn);
            //setTimer in which user must confirm deletion
            G.deltimer = setTimeout(function() {
                $(".delBtn").html(defaultBtn); // $(this) doesn't work inside this function
            }, 1000);
        }

    });

    // click filename, html tag, MD tag or delete
    // $(".fileOperation_container span, .file_name").on("click", function(){
    $("#fileSection").on("click", ".fnBtn, .htmlBtn, .mdBtn", function(){

        // var filename = $(this).parent().attr("filename");
        // var filename = $(this).closest(".file_name").html();
        var className = $(this).attr("class"),
            filename,
            img_url,
            img_alt,
            img_title,
            mdTag,
            imgTag,
            copyToClipboard;

        var doInsert = function(insertString) {
            ///
                // http://jsfiddle.net/4abr7jc5/2/

                // should have focused on something
                //if (G.lastFocusedElement == "undefined") return false;

                // var elementName = G.lastFocusedElement).attr("name");
                // var focused = document.activeElement;
                // var focused = G.lastFocusedElement;
                 // textBody  = $("textarea[name=textBody]").val(),
                // var insertString = $(this).val();
                // var textElement  = $("textarea[name=textBody]");
                // how to select inserted text?
                // $(textElement).val(textBefore + insertString + textAfter).select();
                // $(textElement).val(textBefore + insertString + textAfter);
                // $(textElement).setSelectionRange(0, 100);
                // $(textElement).focus();
                // $(textElement).selectionStart = 0;
                // $(textElement).selectionEnd = 2;
                // $("#xxx").select();
                // var index = textarea.innerText.indexOf("@twitter");
                // textarea.setSelectionRange(index, index + 8);

            var textElement  = G.lastFocusedElement;
            var nameElement = $(textElement).attr("name"); //imgUrl or textBody

            if (nameElement == "imgUrl") {
                $(textElement).val(insertString); //if imgUrl input element, then replace anything there;
            }
            else {

                var cursorPosStart = $(textElement).prop("selectionStart");
                var cursorPosEnd = $(textElement).prop("selectionEnd");

                var textString = $(textElement).val();
                var textBefore = textString.substring(0, cursorPosStart);
                var textAfter  = textString.substring(cursorPosEnd, textString.length);

                $(textElement).val(textBefore + insertString + textAfter);

            }
            toggleMediaSection("close");
        };

        filename = $(this).parent().siblings(".file_name").html();

        // img_url   = "default//" + filename;
        img_url   = filename;
        img_alt   = "image_alt";
        img_title = "image_title";


        if (className == "fnBtn") {
            copyToClipboard = filename;
        }
        else if (className == "htmlBtn") {
            imgTag = "<img src=\"" + img_url + "\" style=\"\" title=\"" + img_title + "\" alt=\"" + img_alt + "\">";
            copyToClipboard = imgTag;
        }
        else if (className == "mdBtn") {
            mdTag = "![" + img_alt + "](" + img_url + " \"" + img_title + "\")";
            copyToClipboard = mdTag;
        }
        else {
            // if class also also 'disabled', then should come here
            return false;
        }

        doInsert(copyToClipboard);

    });


    $("#mediaSection").on("click", "#mediaSectionCloseBtn", function(){
        toggleMediaSection("close");
    });


    // click one of the top tabs: edit, media, preview
    $("#editTabBox").on("click", ".tab", function(){

        //get clicked tab id name
        var idName = $(this).attr("id");

        // if clicked on already selected, then do nothing
        if ($("#" + idName).hasClass("selected")) return;

        // remove .selected class for all tabs
        $("#editTabBox div").each(function(){
            $(this).removeClass("selected");
        })

        // add selected class to clicked tab
        $("#" + idName).addClass("selected");

        // var tabArr = ["editTabSection", "mediaTabSection", "previewTabSection"];

        var selectedTab = idName + "Section";

        $(".tabSection").each(function(){
            var idTabSection = $(this).attr("id");
            if (idTabSection != selectedTab) {
                // $("#" + idTabSection).css("display", "none")
                $("#" + idTabSection).fadeOut(0);
            }
        });
        $("#" + selectedTab).fadeIn(270, "linear"); //css("display", "block");

        if (idName == "detailsTab") {
            $("#postBtn").show();
            // Nothing to do
        }
        else if (idName == "contentTab") {
            $("#imgUrl input").focus();
            $("#postBtn").show();
            // Nothing to do
        }
        else if (idName == "previewTab") {

            $("#postBtn").hide();
            doPostPreview("articlePreview");
        }

    });

    $("#contentTabSection").on("click", "#mediaBtn", function(){

        ////////
            //  if ($("#textBody textarea").setSelectionRange) {
            //  // if ($("#textBody").find("textarea").setSelectionRange()) {
            //     alert("yes");
            //  } else {
            //     alert("no");
            //  }

            // return false;

            // $("#textBody").innterText.setSelectionRange(2, 10);
            // $("#textBody textarea").select();
            // $("#textBody textarea").focus();
            // $("#textBody textarea").innerText.setSelectionRange(0, 100);

            // $("#imgUrl input").focus();
            // $("#imgUrl input").setSelectionRange(0, 10);
            // $("#imgUrl input").select();


            // return false;

            // if (G.lastFocusedElement == "undefined") {
            //     $(".fileOperation_container .htmlBtn, .fileOperation_container .mdBtn").each(function() {
            //         $(this).addClass("disabled");
            //     })

            //     alert("disabled");
            // } else{
            //     alert("enabled");
            // }

            //var elementName = $(G.lastFocusedElement).attr("name");
        toggleMediaSection("open");
    });


    // Post changes
    $("#articleNewEdit").on("click", "#postBtn", function(){
        doPostPreview("articlePost");
    });

    // open url to article#
    $("#articleNewEdit").on("click", "#articleNoBtn", function(){
        var articleNo = $("input[name=articleNo]").val();
        if (articleNo > 0) {
            // window.location.href = "http://stackoverflow.com"
            // var goUrl = G.baseUrl + "/blog/article/" + articleNo + "/";
            // var win = window.open(goUrl, '_blank');
            // win.focus();
            var goUrl = G.baseUrl + "/article/" + articleNo + "/";
            // var goUrl = G.baseUrl + "/articles/" + articleNo + "/";
            // window.open(goUrl, '_blank');
            window.open(goUrl); //wheether blank or not, both seem to work same
        }
        else {
            var msg = "You must save the article before you can view in browser. Or try the preview tab.";
            lib.doMsgBox("Alert", msg, ["close"]);
        }

    });

    // update datetime
    $("#articleNewEdit").on("click", "#dateTimeBtn", function(){
        var d = new Date(),
            year = d.getFullYear(),
            month = d.getMonth() + 1, //month begins with zero
            day = d.getDate(),
            hr = d.getHours(),
            m = d.getMinutes(),
            s = d.getSeconds(),
            nowDateTime = year + "-" + (month < 10 ? "0" + month : month) + "-" +
                                       (day < 10 ? "0" + day : day) + " " +
                                       (hr < 10 ? "0" + hr : hr) + ":" +
                                       (m < 10 ? "0" + m : m) + ":" +
                                       (s < 10 ? "0" + s : s);
                                       // put zeros in front of single digits; not necessary though

        $("input[name=dateTime]").val(nowDateTime);

    });

}

/*function doMediaTab(sender) {

    var folderName = "xyz"; //grab folder name for this article

    var param =
        "action="       + "article_media_files" +
        "&folder="      + folderName;

    $.post(G.ajaxUrl, param, function(result) {

        alert(result);
        return;

        var arr           = result.split(";"),
            result_status = arr[0];

        // posting result
        if (result_status == "ok_post") {

            if (arr[1] && !articleNo) {
                $("input[name=articleNo]").val(arr[1]);
            }

            if (status == "D") {
                var msg      = "The article was deleted.",
                    caption  = "DELETED",
                    customFn = function() {
                        window.location.href = G.baseUrl + "/blog/";
                    };
                    lib.doMsgBox(caption, msg, ["okay"], customFn);
            }
            else {
                var msg     = "The article was posted.",
                    caption = "SAVED";
                    customFn = function() {
                        setTimeout(function() {
                            lib.doMsgBox();
                        }, 1500);
                    };
                    lib.doMsgBox(caption, msg, [], customFn);
            }

        }

        // preview result
        else if (result_status == "ok_preview") {
            var previewHtml = lib.ajaxdecode(arr[1]);
            $("#previewTabSection").html(previewHtml);
        }

        // error
        else {
            var msg = "There was an error.";
            lib.doMsgBox("Ooops!", msg, ["close"]);
        }

    });


} // doMediaTab*/


if ( $("#browseSection #articleSection").length > 0 ) {

    var doAjax = function(ths, btnType, pageNo, type) {

        var action   = G.urlParams[1] + "ListMore";  //get search or article from url
        var keywords = G.urlParams[2];   // get search keywords from url

        var param =
            // "action="       + "articleListMore" +
            "action="       + lib.ajaxencode(action) +
            "&keywords="     + lib.ajaxencode(keywords) +
            "&pageNo="      + lib.ajaxencode(pageNo) +
            "&btnType="     + lib.ajaxencode(btnType);

        // alert(param);

        $.post(G.ajaxUrl, param, function(result) {

            // alert( lib.ajaxdecode(result) );

            var arr    = result.split(";"),
                status = arr[0];

            if (status == "ok") {
                var listHtml = lib.ajaxdecode(arr[1]);

                //can use detach or remove to delete; detach preserves events; but since our
                //element event is not attached to the btn, either works.
                $(ths).remove(); //detach();

                if (btnType == "more") {
                    $("#articleSection #listwrapper").append(listHtml);
                } else {
                    $("#articleSection #listwrapper").prepend(listHtml);
                }
                shared.doLazy(); //trigger lazy

                // lib.url.pushState_pageNo(pageNo);

                if (G.urlParams[1] === "article") {
                    var newPath = "/browse/article/" + pageNo + "/";
                }
                //type == "search"
                else {
                    var keyword = G.urlParams[2];
                    var newPath = "/browse/search/" + keyword + "/" + pageNo + "/";
                }

                // window.history.pushState("", "", newPath);
                window.history.pushState("obj_or_str", "my_title", newPath); // these first 2 params don't seem to matter...

                var old_title = $(document).prop("title");

                var arr = old_title.split("|"); //should be 3 sections
                var lastIndex = arr.length - 1;

                // for page 1, don't show that page in title;
                var new_title = pageNo > 1 ? arr[0] + " | " + pageNo + " | " + arr[lastIndex] : arr[0] + " | " + arr[lastIndex];
                $(document).prop("title", new_title); //push our new page title

            }

            // error
            else {
                var msg = "There was an error.";
                lib.doMsgBox("Ooops!", msg, ["close"]);
            }

        });
    }; //ajax


    // Need to combine these 2 functions below!! Repeating code

    $("#articleSection").on("click", "#browseMoreBtn", function(){
        var pageNo = $(this).attr("pageNo");
        // var type = $(this).attr("type");
        var ths = $(this);
        doAjax(ths, "more", pageNo);
    });

    $("#articleSection").on("click", "#browsePrevBtn", function(){
        var pageNo = $(this).attr("pageNo");
        // var type = $(this).attr("type");
        var ths = $(this);
        doAjax(ths, "prev", pageNo);
    });


}



///////////////////////////
});


/////////////////////////////////////////////////////////////////
