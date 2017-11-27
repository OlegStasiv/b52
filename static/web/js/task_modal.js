$(".detail").on("click", function () {
    $.ajax({
        type: "GET",
        url: "/tasks/" + $(this).attr('id'),

        success: function (data) {
            $('#model_title').text(data.data.task_name);
            $("#task_details").find("td").empty();
            $("#form-modal-body")
                .find('[name="url"]').val(data.data.linkedin_url).end()
                .find('[name="connect_message"]').val(data.data.connect_message_text).end()
                .find('[name="forward_message"]').val(data.data.forward_message).end()
                .find('#con').append("<h4>" + data.data.connection_percent + "</h4>").end()
                .find('#b_every').append("<h4>" + data.data.brake_every + "</h4>").end()
                .find('#b_on').append("<h4>" + data.data.brake_on + "</h4>").end()
                .find('#c_with_mess').append("<h4>" + data.data.connect_with_message + "</h4>").end()

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
