var usernameField = document.getElementById('username');
var emailField    = document.getElementById('email');
var passwordField = document.getElementById('password');

var usernameLabel = document.getElementById('unameLabel');
var emailLabel    = document.getElementById('emailLabel');
var passwordLabel = document.getElementById('passwordLabel');

// Add input event listeners to the input fields
usernameField.addEventListener('input', handleInputChange);
emailField.addEventListener('input', handleInputChange);
passwordField.addEventListener('input', handleInputChange);

function handleInputChange() {

    // Check if the username field has any value
    if (usernameField.value.trim() !== '') {
        usernameLabel.classList.add('field--not-empty');
    } else {
        usernameLabel.classList.remove('field--not-empty');
    }

    // Check if the email field has any value
    if (emailField.value.trim() !== '') {
        emailLabel.classList.add('field--not-empty');
    } else {
        emailLabel.classList.remove('field--not-empty');
    }

    // Check if the password field has any value
    if (passwordField.value.trim() !== '') {
        passwordLabel.classList.add('field--not-empty');
    } else {
        passwordLabel.classList.remove('field--not-empty');
    }

}