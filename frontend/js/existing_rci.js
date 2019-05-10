// Globals
var rci_id = (new URL(document.location)).searchParams.get('rci_id');
var rciInfoSection = document.querySelector("section#rci-info");

var walkthroughLink = document.querySelector("#walkthrough-link");
var walkthroughSections = document.querySelectorAll("#walkthrough-sections>section");
var walkthroughContainer = document.querySelector("#walkthrough-container");
var activeSectionContainer = document.querySelector("#active-section-container");
var walkthroughNext = walkthroughContainer.querySelector("#walkthrough-next");
var walkthroughPrev = walkthroughContainer.querySelector("#walkthrough-prev");
var walkthroughSave = document.querySelector("#walkthrough-save");

// Setup 

// Disable the previous button
walkthroughPrev.setAttribute("disabled", "");

// Manually move the elements to an array because Nodelist is totally well supported :/
// Additionally Array.from() is not at all supported in IE.
var nextPipe = [];
var prevPipe = [];
Array.prototype.forEach.call(walkthroughSections, function(el) {
    nextPipe.push(el);
});

var firstSection = nextPipe.shift();
activeSectionContainer.appendChild(firstSection);


if (!rci_id) { 
    throw "No rci_id present in url";
}

var rciResult = http.get("/api/rci/"+rci_id);


// Register DOM events
walkthroughLink.addEventListener('click', onWalkthroughStart);
walkthroughNext.addEventListener('click', onWalkthroughNext);
walkthroughPrev.addEventListener('click', onWalkthroughPrev);
walkthroughSave.addEventListener('click', onWalkthroughSave);

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

/**
 * @param {Event} event
 */
function onWalkthroughNext(event) {
    event.preventDefault();

    // Get the active section
    var activeSection = activeSectionContainer.querySelector("section");
    activeSection.parentNode.removeChild(activeSection);

    // If the previous pip is empty. Enable it
    if (prevPipe.length === 0) {
        walkthroughPrev.removeAttribute("disabled");
    }

    // Move it into prevPipe
    prevPipe.push(activeSection);

    // Get the new section from nextPipe
    var newActiveSection = nextPipe.shift();

    // Make it the active section 
    activeSectionContainer.appendChild(newActiveSection);

    if (nextPipe.length === 0) {
        // Disable the next button
        walkthroughNext.setAttribute("disabled", ""); 
    }
}

/**
 * @param {Event} event
 */
function onWalkthroughPrev(event) {
    event.preventDefault();

    // Get the active section
    var activeSection = activeSectionContainer.querySelector("section");
    activeSection.parentNode.removeChild(activeSection);

    // If nextPipe is currently empty. Enable it because it will soon have an item
    if (nextPipe.length === 0) {
        walkthroughNext.removeAttribute("disabled");
    }

    // Move it into nextPipe 
    nextPipe.splice(0, 0, activeSection);

    // Get the new section 
    var newActiveSection = prevPipe.pop();

    // Make it the active section 
    activeSectionContainer.appendChild(newActiveSection);

    // If prevPipe is now empty, disable it.
    if (prevPipe.length === 0) {
        walkthroughPrev.setAttribute("disabled", "");
    }
}

/**
 * @param {Event} event
 */
function onWalkthroughSave(event) {
    event.preventDefault();

    // Collect damages
    var damages = prevPipe.filter(function(currentElement) {
        var damageText = currentElement.querySelector("textarea").value;
        if (damageText) {
            return true;
        }
        return false;
    }).map(function(currentElement) {
        var text = currentElement.querySelector("h1").textContent;
        var item = currentElement.querySelector("textarea").value;

        currentElement.querySelector("textarea").value = "";

        return {
            "item": item,
            "text": text
        };
    });

    // Hide the walkthrough
    walkthroughContainer.setAttribute("hidden", "");

    // Reset the walkthrough
    var activeSection = activeSectionContainer.querySelector("section");
    activeSection.parentNode.removeChild(activeSection);

    prevPipe.push(activeSection);
    nextPipe = prevPipe.splice(0, prevPipe.length);

    activeSectionContainer.appendChild(nextPipe.shift());

    walkthroughNext.removeAttribute("disabled");
    walkthroughPrev.setAttribute("disabled", "");

    // Reveal the walkthrough link
    walkthroughLink.removeAttribute("hidden");

    console.log(damages);
}

function onWalkthroughStart(event) {
    event.preventDefault();

    // Reveal the walkthrough
    walkthroughContainer.removeAttribute("hidden", "");

    // Hide the link
    walkthroughLink.setAttribute("hidden", "");
}


