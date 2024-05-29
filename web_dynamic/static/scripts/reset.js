$(document).ready(function() {
      $(".admin-form-login form").on("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        const email = $("#admin_user_email").val();
        const newPassword = $("#admin_user_pass").val();
        const repeatPassword = $("#admin_user_pass_repeat").val();

        if (newPassword !== repeatPassword) {
          alert("Passwords do not match!");
          return;
        }

        const data = {
          email: email,
          password: newPassword,
        };

        $.ajax({
          url: "/reset_password",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify(data),
          xhrFields: {
            withCredentials: true,
          },
          success: function(response) {
            if (response.success) {
              alert("Password updated successfully. Kindly login to continue.");
              window.location.href = "register";
            } else {
              window.location.href = "register";
            }
          },
          error: function(xhr, status, error) {
            console.error("Error:", status, error);
            alert("Error: " + status + " - " + error);
          }
        });
      });
    });
