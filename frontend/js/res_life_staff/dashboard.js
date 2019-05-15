// Relevant globals
var logoutLink = document.querySelector("li#logout>a");
var newRciLink = document.querySelector("li#new-rci>a");
var mainSection = document.querySelector("main");
var buildingTemplate = document.querySelector("template#building-template");
var buildingManifestResult = http.get('/api/rooms');

// Register DOM listeners
logoutLink.addEventListener('click', onLogoutClick);

// Register Data listeners
buildingManifestResult.subscribe(onBuildingManifestLoaded);

// Data Listeners

/**
 * 
 * @param {httpResponse} result 
 */
function onBuildingManifestLoaded(result) {
    if (!result.success) { 
        console.log(result.statusCode, result.error);
        return;
    }

    var buildings = Object.getOwnPropertyNames(result.response);

    console.log(buildings);

    buildings.forEach(function(bldg) {
        var fragment = document.importNode(buildingTemplate.content, true);
        var bldgElement = fragment.querySelector(".building");

        bldgElement.textContent = bldg;
        var nextPage = "/res_life_staff/existing_rcis.html?q="+bldg;
        bldgElement.setAttribute("href", nextPage);

        mainSection.appendChild(fragment);
    });
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
