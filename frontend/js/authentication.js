var authentication = (function(http) {

    // Private members
    var loginEndpoint = "http://localhost:5000/login";
    var logoutEndpoint = "http://localhost:5000/logout";

    function login_internal(username, password) {
        var user = encodeURIComponent(username);
        var pass = encodeURIComponent(password);

        var data = "username="+user+"&password="+pass;

        var contentType = 'application/x-www-form-urlencoded';

        var url = loginEndpoint;

        return http.post(loginEndpoint, data, contentType); 
    }

    function logout_internal() {
        return http.post(logoutEndpoint);
    }

    // Return an object exposing the module's public 
    // api
    return {
        login: function(username, password) {
            return login_internal(username, password);
        },
        logout: function() {
            return logout_internal();
        }
    };
})(http) // This module depends on the http module
