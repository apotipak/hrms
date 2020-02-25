$(function () {

  $(".js-create-approve-priority").click(function () {

    console.log("test");

    $.ajax({
      url: '/system-control/company-approve-priority/create',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-approve-priority").modal("show");
      },
      success: function (data) {
        $("#modal-approve-priority .modal-content").html(data.html_form);
      }
    });

  });

});