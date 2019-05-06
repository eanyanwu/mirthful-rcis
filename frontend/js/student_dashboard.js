// Relevant globals
var logoutLink = document.querySelector("li#logout>a");
var newRciLink = document.querySelector("li#new-rci>a");
var mainSection = document.querySelector("main");
var user_id = window.localStorage.getItem('user_id');
var userRcisObservable = http.get('http://localhost:5000/api/user/'+user_id+'/rcis');

// Register event listners
logoutLink.addEventListener('click', onLogoutClick);
newRciLink.addEventListener('click', onNewRciClick);
userRcisObservable.subscribe(onUserRcisLoaded);

// Listeners
function onUserRcisLoaded(result) {
    if (result.success) {
        var rcis = result.response;

        var rciElements = rcis.map(function(currentValue) {
            var element = document.createElement("p");
            element.textContent = currentValue['rci_id'];
            return element;
        });
    
        mainSection.innerHTML = rciElements.map(function(elem) { return elem.outerHTML }).join("\n");

    }
    else {
        console.log(result.statusCode, result.error);
    }
}

function onLogoutClick(event) {
    event.preventDefault();

    var logoutResult = authentication.logout();
    
    logoutResult.subscribe(function(result) {
        if (result.success) {
            window.location.href = "/";
        } 
        else {
            console.log('ERROR LOGGING OUT', result.statusCode, result.error);
        }
    });
}

function onNewRciClick(event) {
    event.preventDefault();
    window.location.href = "/new_rci.html";
}