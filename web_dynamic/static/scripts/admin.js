$(document).ready(function() {
  $(".signout #admin_signout").click(function() {
    $.ajax({
      type: "DELETE",
      url: "http://127.0.0.1/admin/session",
      xhrFields: {
        withCredentials: true
      },
      success: function(response) {
        window.location.href = "/admin";
      },
      error: function(xhr, status, error) {
        var errorMessage = "Error signing out";

        if (xhr.responseJSON && xhr.responseJSON.message) {
          errorMessage += ": " + xhr.responseJSON.message;
        } else {
          errorMessage += ": " + status + " - " + error;
        }

        alert(errorMessage);
      }
    });
  });
});
