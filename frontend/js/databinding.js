var b = (function(observable){
    /**
     * 
     * @param {HTMLInputElement} textInputElement 
     * @param {observable} observable 
     */
    function bindInputElement(textInputElement, observable) {
        textInputElement.value = observable.get();
        observable.subscribe( function(val) { textInputElement.value = val; });

        textInputElement.addEventListener("input", function() { 
            observable.set(textInputElement.value);
        });
    }

    return {
        bindInputElement: bindInputElement
    };

})(observable);