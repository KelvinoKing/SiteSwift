$(document).ready(function() {
  // Order Button Click Event
  $(".pay").click(function() {
    // Retrieve orderid from button
    var orderId = $(this).attr("order_id");

    // Create order object
    var orderData = {
      "status": "complete",
    };

    // Make call to post order information
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
  });
});