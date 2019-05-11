// Relevant globals
var newRciForm = document.querySelector("form#new-rci-form");
var buildingSelect = document.querySelector("select#building-select");
var buildingOptionTemplate = document.querySelector("template#building-option-template");
var roomSelect = document.querySelector("select#room-select");
var roomOptionTemplate = document.querySelector("template#room-option-template");
var buildingManifestResult = http.get("/api/rooms");

// Register DOM listeners
newRciForm.addEventListener("submit", onFormSubmit);

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
   
    var buildingManifest = result.response;
    
    var buildingNames = Object.getOwnPropertyNames(buildingManifest); 

    var buildingOptionElements = buildingNames.map(function(currentValue) {
        var domFragment = document.importNode(buildingOptionTemplate.content, true);

        var option = domFragment.querySelector(".building-option");

        option.setAttribute("value", currentValue);
        option.textContent = currentValue;

        return option;
    });

    buildingOptionElements.forEach(function(currentValue) {
        buildingSelect.add(currentValue);
    });
    
    updateRoomSelectElement(buildingSelect[buildingSelect.selectedIndex].value, buildingManifest);

    // Register the listeners
    buildingSelect.addEventListener("input", function(event) {
        var currentSelection = event.target[event.target.selectedIndex].value;
        updateRoomSelectElement(currentSelection, buildingManifest);
    });
}

/**
 * 
 * @param {string} selectedBuilding 
 * @param {any} buildingManifest 
 */
function updateRoomSelectElement(selectedBuilding, buildingManifest) {
    var rooms = buildingManifest[selectedBuilding];

    var roomOptionElements = rooms.map(function(currentValue) {
        var domFragment = document.importNode(roomOptionTemplate.content, true);

        var optionElement = domFragment.querySelector(".room-option");

        optionElement.setAttribute("value", currentValue["room_id"]);
        optionElement.textContent = currentValue["room_name"];

        return optionElement;
    });

    // Clear the existing option elements
    roomSelect.innerHTML = "";

    roomOptionElements.forEach(function(currentValue) {
        roomSelect.add(currentValue);
    });
}

// DOM Listeners

/**
 * 
 * @param {Event} event 
 */
function onFormSubmit(event) {
    event.preventDefault();

    var roomId = roomSelect[roomSelect.selectedIndex].value;

    var newRciResult = http.post("/api/room/" + roomId + '/rci');

    newRciResult.subscribe(function(result) {
        if (!result.success) {
            console.log(result.statusCode, result.error);
            return;
        }
      
        var rci = result.response;
        var qs = "?rci_id=" + encodeURIComponent(rci["rci_id"]);
        window.location.href = "existing_rci.html" + qs;
    });
}
