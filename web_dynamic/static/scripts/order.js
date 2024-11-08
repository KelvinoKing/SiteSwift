$(document).ready(function() {
    // Order Button Click Event
    $(".pay").click(function(event) {
      event.preventDefault(); // Prevent form submission

      // Retrieve orderid and other required data
      var orderId = $(this).attr("order_id");

      // Generate a random ip_address
      ip_address = Math.floor(Math.random() * 255) + '.' + Math.floor(Math.random() * 255) + '.' + Math.floor(Math.random() * 255) + '.' + Math.floor(Math.random() * 255);

      var orderData = {
        "status": "complete",
        "ip_address": ip_address
      }

      var amount = 1; // Example amount, replace with actual amount
      var phoneNumber = $("#mobile-number").val(); // Example phone number, replace with actual number

      if (!phoneNumber) {
        alert("Please enter a valid phone number");
        return;
      }

      // Create data object
      var payData = {
        amount: amount,
        phone_number: phoneNumber
      };

      // Make call to initiate payment
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/pay",
        contentType: "application/json",
        data: JSON.stringify(payData),
        xhrFields: {
          withCredentials: true  // Include credentials
        },
        success: function(response) {
          // Handle successful payment initiation
          alert("Payment initiated. Please complete the payment on your phone.");

          // Make call to post order status
          $.ajax({
            type: "PUT",
            url: "http://127.0.0.1:5000/api/v1/orders/" + orderId,
            contentType: "application/json",
            data: JSON.stringify(orderData),
            xhrFields: {
              withCredentials: true  // Include credentials
            },
            success: function(response) {
              window.location.href = "/account";
            },
            error: function(xhr, status, error) {
              var errorMessage = "Error completing order";
            
              if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMessage += ": " + xhr.responseJSON.message;
              } else {
                errorMessage += ": " + status + " - " + error;
              }
            
              alert(errorMessage);
            }
          });
          
          // Optionally, poll the backend to check for payment confirmation
          // Polling or websocket implementation can be done here
        },
        error: function(xhr, status, error) {
          var errorMessage = "Error initiating payment";

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
