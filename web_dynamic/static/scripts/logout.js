$(document).ready(function() {
  // Select the logout button
  $(".btn.btn-primary.mt-2").on("click", function() {
      // Confirm the logout action
      if (confirm("Are you sure you want to log out?")) {
          // Make the AJAX request
          $.ajax({
              url: "/sessions",
              type: "DELETE",
              success: function() {
                  // On success, redirect to the homepage
                  window.location.href = "/";
              },
              error: function(xhr, status, error) {
                  // On error, alert the user
                  alert("Logout failed. Please try again.");
              }
          });
      }
  });
});
