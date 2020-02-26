$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-company-approve-priority .modal-content").html("");
        $("#modal-company-approve-priority").modal("show");
      },
      success: function (data) {
        $("#modal-company-approve-priority .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#company-approve-priority-table tbody").html(data.html_book_list);
          $("#modal-company-approve-priority").modal("hide");
        }
        else {
          $("#modal-company-approve-priority .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-company-approve-priority").click(loadForm);
  $("#modal-company-approve-priority").on("submit", ".js-company-approve-priority-create-form", saveForm);

});
