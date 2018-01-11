$(".detail").on("click", function () {
    $.ajax({
        type: "GET",
        url: "/tasks/" + $(this).attr('id'),

        success: function (data) {
            var brake_every;
            var brake_on;
            if (data.data.brake_every === null) {
                brake_every = 0;
            } else {
                brake_every = data.data.brake_every;
            }
            if (data.data.brake_on === null) {
                brake_on = 0;
            } else {
                brake_on = data.data.brake_on;
            }
            $('#model_title').text(data.data.task_name);
            $("#task_details").find("td").empty();
            $("#form-modal-body")
                .find('[name="url"]').val(data.data.linkedin_url).end()
                .find('[name="connect_message"]').val(data.data.connect_message_text).end()
                .find('[name="connect_message_note"]').val(data.data.connect_message_note).end()
                .find('[name="forward_message"]').val(data.data.forward_message).end()
                .find('#con').append("<h4>" + data.data.connection_percent + "</h4>").end()
                .find('#b_every').append("<h4>" + brake_every + "</h4>").end()
                .find('#b_on').append("<h4>" + brake_on + "</h4>").end()
                // .find('#c_with_mess').append("<h4>" + data.data.connect_with_message + "</h4>").end()
            $("#c_with_mess").append(
               // $('<input>')
               //    .attr('type', 'checkbox')
               //    .attr('checked', data.data.connect_with_message)
                $('<label>')
                    .attr('id','chbox')
                    .attr('style', 'font-size: 1.9em')
                // <label style="font-size: 1.9em">
                // <input type="checkbox" value="" checked="">
                // </label>
            );
            $("#chbox").append(
                $('<input>')
                .attr('type', 'checkbox')
                .attr('checked', data.data.connect_with_message)
                    .attr('disabled', 'true')
            );
        }
    });
});

$("#points").on("click", function () {
    $.ajax({
        type: "GET",
        url: "/points/",

        success: function (data) {
            $('#point').text(data.data.data);
        }
    });
});

function sendMyMessages(pk,token) {
    data = {
        'stream': "notifications",
        'payload':{
            'action': "update",
            'data': {
                'read': true
            },
            'pk': pk,
            'token': token
        }
    };

    var msg = JSON.stringify(data);
    var wsSend = function(data) {
    if (!ws.readyState) {
        setTimeout(function () {
            wsSend(data);
        }, 100);
    } else {
        ws.send(data);
    }
    };
    wsSend(msg);
    $("[data-board-id="+pk+"]").fadeOut(700, function() { $(this).remove(); });

}
