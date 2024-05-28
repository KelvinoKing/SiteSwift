$(document).ready(function () {
  $('form').on('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    var formData = new FormData(this); // Create a FormData object with the form's data

    $.ajax({
      url: 'http://127.0.0.1:5000/api/v1/users/' + formData.get('id_user'), // Assuming the user ID is stored in a hidden input field
      type: 'PUT',
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        alert('Profile updated successfully!');
        // Optionally, you can update the page with the new user information here
        // Get back to the dashboard
        window.location.href = 'account'
        window.location.href = 'account'
      },
      error: function (xhr, status, error) {
        alert('Error: ' + xhr.responseText);
      }
    });
  });
});
