$(document).ready(function () {
    var table = $('#tbl-servers').DataTable({
        responsive: true,
        LengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'lfrtip',
        DisplayLength: 25,
        ajax: {
            url: "/servers/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "-",
            data: "server",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "username",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "password",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "created_at",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "notes",
            // className: 'text-center'
        }, {
            data: "actions",
            className: 'text-center'
        }],
        columnDefs: [{
            targets: [5],
            data: null,
            defaultContent: "<button type='button' id='btnEditServer' data-bs-toggle='modal' data-bs-target='#editServerModal' class='btn btn-primary btn-sm'><i class='fa-solid fa-pencil'></i></button>&nbsp;<button type='button' class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#deleteServerModal'><i class='fa-solid fa-trash-can'></i></button>"
        }],
    });


    $('#tbl-servers tbody').on('click', 'tr', function () {
        var tr = $(this).closest('tr');
        var data = $('#tbl-servers').DataTable().row(tr).data();

        $("#inputEditServer").val(data.server);
        $("#inputEditUsername").val(data.username);
        $("#inputEditPassword").val(data.password);
        $("#inputEditNotes").val(data.notes);
        $("#inputDeleteServer").val(data.server);
        $("#inputEditOldServer").val(data.server);
    });

    $('#inputServer, #inputUsername, #inputPassword, #inputEditServer, #inputEditUsername, #inputEditPassword').on('keypress', function (e) {
        if (e.which == 32)
            return false;
    });

});
