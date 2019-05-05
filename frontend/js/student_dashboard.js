var logoutLink = document.querySelector("li#logout>a");
var newRciLink = document.querySelector("li#new-rci>a");
var mainSection = document.querySelector("main");

// Register event listners
logoutLink.addEventListener('click', onLogoutClick);
newRciLink.addEventListener('click', onNewRciClick);

function onLogoutClick(event) {
    event.preventDefault();
    authentication.logout(
        function(result) {
            window.location.href = "/";
        },
        function(status_code, error){
            console.log('ERROR LOGGING OUT', status_code, error);
        });
}

function onNewRciClick(event) {
    event.preventDefault();
    window.location.href = "/new_rci.html";
}



