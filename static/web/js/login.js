$(document).ready(function() {
       $("#forgot-submit").submit(function(event){
            $.ajax({
                 type:"POST",
                 url:"/password_reset/",
                 data: {
                        'video': $('#test').val() // from form
                        },
                 success: function(){
                     $('#message').html("<h2>Contact Form Submitted!</h2>")
                 }
            });
            return false; //<---- move it here
       });

});