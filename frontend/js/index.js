var loginForm = document.querySelector('form#login-form');

// Register event listners
loginForm.addEventListener('submit', onLoginSubmit);

function onLoginSubmit(event) {
    event.preventDefault();
    var loginForm = event.currentTarget;
    var userInput = loginForm.querySelector("input[name='username']");
    var passInput = loginForm.querySelector("input[name='password']");
    var output = loginForm.querySelector("output[name='login-error']");

    var username = userInput.value; 
    var password = passInput.value; 

    // Clear the result of potential previous login attempts
    output.value = "";

    authentication.login(username, password,
        function(result) {
            var dashboardName = result['role'] + "_dashboard.html";

            // Temporary: Store the user_id in local storage
            // Local storage is not alwasy available,
            // so what i'm thinking of doing is storing this in a cookie.
            window.localStorage.setItem('user_id', result['user_id']);

            window.location.href = dashboardName;
        },
        function(status, error) {
            var errorMessage = error['error_message'];
            output.value = errorMessage;
        });
}



