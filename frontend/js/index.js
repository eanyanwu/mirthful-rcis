var loginForm = document.querySelector('form#login-form');

// Register event listners
loginForm.addEventListener('submit', onLoginSubmit);


function onLoginSubmit(event) {
    event.preventDefault();
    var loginForm = event.currentTarget;
    var userInput = loginForm.querySelector("input[name='username']");
    var passInput = loginForm.querySelector("input[name='password']");

    var username = userInput.value; 
    var password = passInput.value; 

    var authResultObservable = authentication.login(username, password);
    
    authResultObservable.subscribe(onAuthenticationResult);
}

function onAuthenticationResult(result) {
    var output = loginForm.querySelector("output[name='login-error']");

    // Clear the result of potential previous login attempts
    output.value = "";

    if (result.success) {
        var response = result.response;

        var dashboardName = response['role'] + "_dashboard.html";

        window.localStorage.setItem('user_id', response['user_id']);

        window.location.href = dashboardName;
    }
    else {
        var errorMessage = result.error["error_message"];
        output.value = errorMessage;
    }
}
