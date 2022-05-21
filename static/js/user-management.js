$(document).ready(function () {
    var table = $('#tbl-users').DataTable({
        responsive: true,
        LengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'lfrtip',
        DisplayLength: 25,
        ajax: {
            url: "/user/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "-",
            data: "username",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "password",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "server",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "created_at",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "expires_at",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "last_activity",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "notes",
            // className: 'text-center'
        }, {
            data: "actions",
            // className: 'text-center'
        }],
        columnDefs: [{
            targets: [7],
            data: null,
            defaultContent: "<button type='button' id='btnEditUser' class='btn btn-primary btn-sm'>Edit</button><button type='button' id='btnDelete' class='btn btn-danger btn-sm'>Delete</button>"
        }],
    });
});