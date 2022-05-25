$(document).ready(function () {
    var table = $('#tbl-admins').DataTable({
        responsive: true,
        LengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'lfrtip',
        DisplayLength: 25,
        ajax: {
            url: "/admins/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "-",
            data: "username",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "created_at",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "last_activity",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "locked",
            className: 'text-center'
        }, {
            data: "actions",
            className: 'text-center'
        }],
        columnDefs: [{
            targets: [4],
            data: null,
            defaultContent: "<button type='button' class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#deleteAdminModal'><i class='fa-solid fa-trash-can'></i></button>"
        }, {
            targets: [3],
            render: function (data, type, row) {
                if (row.locked == "false") {
                    return "<button type='button' class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#lockAdminModal'><i class='fa-solid fa-lock-open'></i></button>";
                } else if (row.locked == "true") {
                    return "<button type='button' class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#lockAdminModal'><i class='fa-solid fa-lock'></i></button>";
                }
            }
        }],
    });


    $('#tbl-admins tbody').on('click', 'tr', function () {
        var tr = $(this).closest('tr');
        var data = $('#tbl-admins').DataTable().row(tr).data();

        if (data.username == "administrator") {
            $("#btnModalDelete, #btnModalLock").prop('disabled', true);
        } else {
            $("#btnModalDelete, #btnModalLock").prop('disabled', false);
        }

        $("#inputDeleteUsername, #inputLockUsername").val(data.username);
        $("#inputLockStatus").val(data.locked);

        if (data.locked == "true") {
            $("#btnModalLock").text("Unlock");
        } else if (data.locked == "false") {
            $("#btnModalLock").text("Lock");
        }

    });

    $('#inputUsername, #inputPassword').on('keypress', function (e) {
        if (e.which == 32)
            return false;
    });

});
