var newRciForm = document.querySelector("form#new-rci-form");
var buildingSelect = document.querySelector("select#building-select");
var roomSelect = document.querySelector("select#room-select");

http.get("http://localhost:5000/api/rooms",
    function(result) {
        onRoomDataLoad(result);
    },
    function(status_code, error) {
        console.log(status_code, error);
    });



function onRoomDataLoad(buildingManifest) {
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

    newRciForm.addEventListener("submit", onFormSubmit);
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
    
    console.log(url);
    
    http.post(url,
        null,
        null,
        function(result) {
            var qs = "?rci_id=" + encodeURIComponent(result["rci_id"]);
            window.location.href = "existing_rci.html" + qs;
        },
        function(status_code, error_message) {
            console.log(status_code, error_message);
        }
    );
}
