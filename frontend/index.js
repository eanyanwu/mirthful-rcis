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

            window.location.href = dashboardName;
        },
        function(status, error) {
            var errorMessage = error['error_message'];
            output.value = errorMessage;
        });
}



