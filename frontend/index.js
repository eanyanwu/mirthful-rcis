var loginForm = document.querySelector('form#login-form');

// Register event listners
loginForm.addEventListener('submit', onLoginSubmit);

function onLoginSubmit(event) {
    event.preventDefault();
    var loginForm = event.currentTarget;
    var username = loginForm.querySelector("input[name='username']").value;
    var password = loginForm.querySelector("input[name='password']").value;

    console.log(username, password);

    authentication.login(username, password,
        function(result) {
            console.log('Success', result);
        },
        function(status, error) {
            console.log(status, error);
        });
}



