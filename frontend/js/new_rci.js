// Relevant globals
var newRciForm = document.querySelector("form#new-rci-form");
var buildingSelect = document.querySelector("select#building-select");
var roomSelect = document.querySelector("select#room-select");
var buildingManifestObservable = http.get("http://localhost:5000/api/rooms");

// Register listeners
buildingManifestObservable.subscribe(onBuildingManifestDataLoad);
newRciForm.addEventListener("submit", onFormSubmit);


// Listeners
function onBuildingManifestDataLoad(result) {
    if (result.success) {
        var buildingManifest = result.response;
        
        // Populate the select elements
        var buildingNames = Object.getOwnPropertyNames(buildingManifest); 

        var buildingOptionElements = buildingNames.map(function(currentValue) {
            var optionElement = document.createElement("option");
            optionElement.setAttribute("value", currentValue);
            optionElement.textContent = currentValue;

            return optionElement;
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
    else {
        console.log(result.statusCode, result.error);
    }
}

function updateRoomSelectElement(selectedBuilding, buildingManifest) {
    var rooms = buildingManifest[selectedBuilding];

    var roomOptionElements = rooms.map(function(currentValue) {
        var optionElement = document.createElement("option");
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

function onFormSubmit(event) {
    event.preventDefault();

    var roomId = roomSelect[roomSelect.selectedIndex].value;

    var url = "http://localhost:5000/api/room/" + roomId + '/rci';
    
    var rciObservable = http.post(url);

    rciObservable.subscribe(function(result) {
        if (result.success) {
            var rci = result.response;
            var qs = "?rci_id=" + encodeURIComponent(rci["rci_id"]);
            window.location.href = "existing_rci.html" + qs;
        }
        else {
            console.log(status_code, error_message);
        }
    });
}
