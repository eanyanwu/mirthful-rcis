var logoutLink = document.querySelector("li#logout>a");
var newRciLink = document.querySelector("li#new-rci>a");
var mainSection = document.querySelector("main");

var user_id = window.localStorage.getItem('user_id');

http.get('http://localhost:5000/api/user/'+user_id+'/rcis',
    function(result) {
        console.log(result);
        onExistingRcisLoaded(result);
    },
    function(status_code, error) {
        console.log(status_code, error);
    }
);



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

function onExistingRcisLoaded(rcis) {
    var rciElements = rcis.map(function(currentValue) {
        var element = document.createElement("p");
        element.textContent = currentValue['rci_id'];
        return element.outerHTML;
    });

    mainSection.innerHTML = rciElements.join("\n");
}
