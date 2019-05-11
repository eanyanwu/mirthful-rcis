// Globals
var rci_id = (new URL(document.location)).searchParams.get('rci_id');
var rciInfoSection = document.querySelector("section#rci-info");
var rciDamagesSection = document.querySelector("#rci-damages");
var existingDamageTemplate = document.querySelector("#existing-damage-template");
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

    rciInfoSection.querySelector("p#building-name").textContent = rci["building_name"];
    rciInfoSection.querySelector("p#room-name").textContent = rci["room_name"];

    var damages = rci.damages;

    damages.forEach(function(damage) {
        var template = document.importNode(existingDamageTemplate.content, true);

        var damageText = damage.item + ": " + damage.text;

        template.querySelector(".existing-damage").textContent = damageText;

        rciDamagesSection.appendChild(template);
    });
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
        var item = currentElement.querySelector("h1").textContent;
        var text = currentElement.querySelector("textarea").value;

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

    // Loop through the damages and send them
    var lastRequest = "";
    damages.forEach(function(damage) {
        lastRequest = http.post("/api/rci/"+rci_id+"/damage", JSON.stringify(damage), "application/json");
    });

    // Refresh the page
    lastRequest.subscribe(function(result) {
        window.location.reload(true);
    });

}

function onWalkthroughStart(event) {
    event.preventDefault();

    // Reveal the walkthrough
    walkthroughContainer.removeAttribute("hidden", "");

    // Hide the link
    walkthroughLink.setAttribute("hidden", "");
}


