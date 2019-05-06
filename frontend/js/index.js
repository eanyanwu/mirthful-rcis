// Relevant globals
var loginFormElement = document.querySelector('form#login-form');
var loginFormContents = {
    username: observable(""),
    password: observable(""),
    output: observable("")
};

// Data-binding 
b.bindInputElement(loginFormElement.querySelector("input[name='username']"), loginFormContents.username);
b.bindInputElement(loginFormElement.querySelector("input[name='password']"), loginFormContents.password);
b.bindInputElement(loginFormElement.querySelector("output[name='login-error']"), loginFormContents.output);

// Register event listners
loginFormElement.addEventListener('submit', onLoginSubmit);

// Listeners

/**
 * 
 * @param {Event} event 
 */
function onLoginSubmit(event) {
    event.preventDefault();
    
    var username = loginFormContents.username.get();
    var password = loginFormContents.password.get();

    var authResult = authentication.login(username, password);
    
    authResult.subscribe(onAuthenticationResult);
}

function onAuthenticationResult(result) {
    // Clear the result of potential previous login attempts
    loginFormContents.output.set("")

    if (!result.success) {
        loginFormContents.output.set(result.error["error_message"]);
        return;
    }

    var response = result.response;

    var dashboardName = response['role'] + "_dashboard.html";

    window.localStorage.setItem('user_id', response['user_id']);

    window.location.href = dashboardName;
}
