document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');

    // Example of simple form validation
    loginForm.addEventListener('submit', function(event) {
        const identifier = loginForm.querySelector('input[name="identifier"]');
        const password = loginForm.querySelector('input[name="password"]');

        if (!identifier.value) {
            alert('Please enter your username or email.');
            event.preventDefault(); // Prevent form submission
            identifier.focus(); // Focus on the identifier input
            return;
        }

        if (!password.value) {
            alert('Please enter your password.');
            event.preventDefault(); // Prevent form submission
            password.focus(); // Focus on the password input
            return;
        }
    });
});