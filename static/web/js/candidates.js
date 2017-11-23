$(document).ready(function() {

    $("#searchBy li").click(function () {
        var task = $(this).attr('data-board-id');
        $.ajax({
            type: "GET",
            url: "/candidates/",
            data: {
                'task_id': task
            },
            success: function (data) {
            }
        });
    });
});