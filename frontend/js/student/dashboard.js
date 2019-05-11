// Relevant globals
var logoutLink = document.querySelector("li#logout>a");
var newRciLink = document.querySelector("li#new-rci>a");
var mainSection = document.querySelector("main");
var newRciTemplate = document.querySelector("template#rci-template");
var user_id = window.localStorage.getItem('user_id');
var userRcisResult = http.get('/api/user/'+user_id+'/rcis');

// Register DOM listeners
logoutLink.addEventListener('click', onLogoutClick);
newRciLink.addEventListener('click', onNewRciClick);

// Register Data listeners
userRcisResult.subscribe(onUserRcisLoaded);

// Data Listeners

/**
 * 
 * @param {httpResponse} result 
 */
function onUserRcisLoaded(result) {
    if (!result.success) { 
        console.log(result.statusCode, result.error);
        return;
    }

    var rciElements = result.response.map(function(rci) {
        var domFragment = document.importNode(newRciTemplate.content, true);
        var displayText = rci["building_name"] + ": " + rci["room_name"]; 
        var rciId = rci['rci_id'];
        var element = domFragment.querySelector(".rci");
        element.textContent = displayText;
        element.setAttribute("href", "/student/existing_rci.html?rci_id="+rciId);

        return domFragment;
    });

    rciElements.forEach(function(elem) { mainSection.appendChild(elem); });
}

// DOM Listeners

/**
 * 
 * @param {Event} event 
 */
function onLogoutClick(event) {
    event.preventDefault();

    var logoutResult = authentication.logout();

    logoutResult.subscribe(function(result) {
        if (!result.success) {
            console.log('ERROR LOGGING OUT', result.statusCode, result.error);
            return;
        }

        window.location.href = "/";
    });
}

/**
 * 
 * @param {Event} event 
 */
function onNewRciClick(event) {
    event.preventDefault();
    window.location.href = "/student/new_rci.html";
}
