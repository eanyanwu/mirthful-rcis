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

    console.log(result);

    var rciElements = result.response.map(function(currentValue) {
        var domFragment = document.importNode(newRciTemplate.content, true);
        var rci_id = currentValue["rci_id"]
        var element = domFragment.querySelector(".rci-id");
        element.textContent = currentValue['rci_id'];
        element.setAttribute("href", "/existing_rci.html?rci_id="+rci_id);

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
    window.location.href = "/new_rci.html";
}
