var bldg = (new URL(document.location)).searchParams.get('q'); 

var rcisResult = http.get("/api/buildings/"+bldg+"/rcis");


rcisResult.subscribe(onRcisLoaded);


function onRcisLoaded(result) {
    console.log(result);
}
