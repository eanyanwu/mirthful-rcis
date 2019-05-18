var bldg = (new URL(document.location)).searchParams.get('q'); 
var mainSection = document.querySelector("main");
var rciTemplate = document.querySelector("#rci-template");

var rcisResult = http.get("/api/buildings/"+bldg+"/rcis");


rcisResult.subscribe(onRcisLoaded);


function onRcisLoaded(result) {
    if (!result.success) {
        console.log(result.error)
        throw result.error
    }

    rcis = result.response;

    rcis.forEach(function(rci) {
        var documentFragment = document.importNode(rciTemplate.content, true);

        var rciElement = documentFragment.querySelector(".rci");

        var rciTextContent = rci["building_name"] + ": " + rci["room_name"];
        var rciLink = "/student/existing_rci.html?rciId="+rci["rci_id"];

        rciElement.textContent = rciTextContent;
        rciElement.setAttribute("href", rciLink);

        mainSection.appendChild(documentFragment);
    });


}
