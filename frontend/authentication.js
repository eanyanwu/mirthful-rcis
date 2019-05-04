var authentication = (function(http) {

    // Private members
    var loginEndpoint = "http://localhost:5000/login";

    function login_internal(username, password, success, error) {
        var user = encodeURIComponent(username);
        var pass = encodeURIComponent(password);

        var data = "username="+user+"&password="+pass;

        var contentType = 'application/x-www-form-urlencoded';

        var url = loginEndpoint;

        http.post(loginEndpoint, data, contentType, success, error); 
    }

    // Return an object exposing the module's public 
    // api
    return {
        login: function(username, password, success, error) {
            login_internal(username, password, success, error);
        }
    };
})(http) // This module depends on the http module
