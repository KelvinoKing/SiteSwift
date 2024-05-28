$(document).ready(function () {
  // Select the account icon button
  const accountButton = $('button[aria-label="Account"]');

  // Add click event listener to the account icon button
  accountButton.on('click', function () {
    // Log out the user via AJAX DELETE request
    $.ajax({
      url: '/admin/sessions',
      type: 'DELETE',
      success: function () {
        // Redirect to the login page
        alert('You have been logged out.');
        window.location.href = '';
      },
      error: function (error) {
        console.log('Error logging out:', error);
      }
    });
  });
});
