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
          console.log(data.message);
          Toast.fire({
            type: 'success',
            title: '',
            text: data.message,
          })         
          $("#company-approve-priority-list-table tbody").html(data.html_company_approve_priority_list);          
          $("#modal-company-approve-priority").modal("hide");
        }
        else {
          console.log("error");
          Toast.fire({
            type: 'error',
            title: '',
            text: data.message,
            html: '',
          })
          $("#modal-company-approve-priority .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create Company Approve Priority
  $(".js-create-company-approve-priority").click(loadForm);
  $("#modal-company-approve-priority").on("submit", ".js-company-approve-priority-create-form", saveForm);

  // Update Company Approve Priority
  $("#company-approve-priority-list-table").on("click", ".js-update-company-approve-priority", loadForm);
  $("#modal-company-approve-priority").on("submit", ".js-company-approve-priority-update-form", saveForm);

  // Delete Company Approve Priority
  $("#company-approve-priority-list-table").on("click", ".js-delete-company-approve-priority", loadForm);
  $("#modal-company-approve-priority").on("submit", ".js-company-approve-priority-delete-form", saveForm);  

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    showCloseButton: false,
    timer: 3000
  });

});

