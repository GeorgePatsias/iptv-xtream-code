$(document).ready(function () {
    var table = $('#tbl-subscribers').DataTable({
        responsive: true,
        LengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'lfrtip',
        DisplayLength: 25,
        ajax: {
            url: "/subscribers2/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "-",
            data: "subscriber",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "username",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "password",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "server",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "created_at",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "expires_at",
            // className: "text-center"
        }, {
            defaultContent: "-",
            data: "notes",
            // className: "text-center"
        }, {
            data: "actions",
            className: "text-center"
        }],
        columnDefs: [{
            targets: [7],
            data: null,
            defaultContent: "<button type='button' id='btnEditSubscriber' data-bs-toggle='modal' data-bs-target='#editSubscriberModal' class='btn btn-primary btn-sm'><i class='fa-solid fa-pencil'></i></button>&nbsp;<button type='button' id='btnDelete' data-bs-toggle='modal' data-bs-target='#deleteSubscriberModal' class='btn btn-danger btn-sm'><i class='fa-solid fa-trash-can'></i></button>"
        }],
    });


    $('#tbl-subscribers tbody').on('click', 'tr', function () {
        var tr = $(this).closest('tr');
        var data = $('#tbl-subscribers').DataTable().row(tr).data();

        var month = getMonth(data.expires_at).toString();
        if (month.length == 1) {
            month = "0" + month;
        }

        var expiring_date = data.expires_at.split(" ");
        expiring_date = expiring_date[3] + "-" + month + "-" + expiring_date[1];

        $("#inputDeleteUsername").val(data.subscriber);
        $("#inputEditSubscriber").val(data.subscriber);
        $("#inputEditOldUsername").val(data.username);
        $("#inputEditUsername").val(data.username);
        $("#inputEditPassword").val(data.password);
        $("#inputEditExpiration").val(expiring_date);
        $("#inputEditNotes").val(data.notes);
        $("#selectEditServer").val(data.server);


    });

    $('#inputUsername, #inputPassword, #inputServer, #inputExpiration, #inputEditUsername, #inputEditPassword, #inputEditServer, #inputEditExpiration').on('keypress', function (e) {
        if (e.which == 32)
            return false;
    });

    $(function () {
        var dtToday = new Date();

        var month = dtToday.getMonth() + 1;
        var day = dtToday.getDate();
        var year = dtToday.getFullYear();
        if (month < 10)
            month = '0' + month.toString();
        if (day < 10)
            day = '0' + day.toString();

        var maxDate = year + '-' + month + '-' + day;
        $('#inputEditExpiration, #inputExpiration').attr('min', maxDate);
    });

});

function getMonth(date) {
    return new Date(Date.parse(date)).getMonth() + 1
}