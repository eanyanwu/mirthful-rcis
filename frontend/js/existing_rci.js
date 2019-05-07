var rci_id = (new URL(document.location)).searchParams.get('rci_id');
var rciInfoSection = document.querySelector("section#rci-info");

if (!rci_id) { 
    throw "No rci_id present in url";
}

var rciResult = http.get("/api/rci/"+rci_id);


// Register DOM events

// Register Data events
rciResult.subscribe(onRciResponse);

/**
 * @param {httpResponse} result
 */
function onRciResponse(result) {
    if (!result.success) {
        console.log(result.statusCode, result.error);
        return;
    }

    var rci = result.response;

    rciInfoSection.querySelector("p#rci-id").textContent  = rci["rci_id"];
    rciInfoSection.querySelector("p#building-name").textContent = rci["building_name"];
    rciInfoSection.querySelector("p#room-name").textContent = rci["room_name"];
}
