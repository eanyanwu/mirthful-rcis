// A module for creating values that can be "observed" 
// Tbh it is more of a "notifier" because it notifies the listeners
// whenever the value changes. 
//
// Note: We are making use of javascript closures so read up on 
// them if you are confused
var observable = function(value) {
    // List of functions to call whenever there is a change
    // to the value being observed
    var listeners = [];

    // Value being observed
    _v = value;

    // Function for notifying listeners of a new value
    function notify(newValue) {
        listeners.forEach(function(listener) { listener(newValue) });
    }

    // Get the current value of the observable.
    function get() { return _v; }

    // Set the observed value.
    // This triggers a notification for all the listeners
    function set(newValue) { 
        _v = newValue;
        notify(_v);
    }

    // Register a listener
    function subscribe(listener) { listeners.push(listener) }

    return {
        get: get,
        set, set,
        subscribe: subscribe
    };
}

