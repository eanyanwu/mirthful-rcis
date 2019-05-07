var httpResponse = function() {
    return {
        success: false,
        statusCode: 0,
        error: null,
        response: null
    };
};

// An observable wrapping the result of an http request.
// I am slowly understanding that promises are VERY simliary to 1-event observables.
// This is a 1-event observable because an http request only emits an event once it completes.
var httpResponseObservable = function() {

    // We create an initial structure for the observable object
    var _innerObservable = observable(httpResponse());

    // A flag to indicate if the http request has completed.
    // This will allow us to give the result to listeners who subscribed
    // after the change actually happened.
    // This is more of a convenience feature due to the nature of http requests.
    // Without it we would need to create the httpResponseObservable object first,
    // subscribe to it, then pass it to the get/post/delete methods
    var completed = false;

    // If the http request was successful, this method should be called
    function success(statusCode, response) {

        if (completed) {
            throw "The request has already been completed";
        }
        else {
            _innerObservable.set({
                success: true,
                statusCode: statusCode,
                error: null,
                response: response
            });

            completed = true;
        }
    }

    // If the http request was not successful, this method should be called
    function error(statusCode, error) {
        if (completed) {
            throw "The request has already been completed";
        } 
        else {
            _innerObservable.set({
                success: false,
                statusCode: statusCode,
                error: error,
                response: null
            });

            completed = true;
        }
    }

    function subscribe(listener) {
        if (completed) {
            // The request has already been completed. 
            // Give the result right away
            listener(_innerObservable.get());
        }
        else {
            // The request has not been completed.
            _innerObservable.subscribe(listener);
        }
    }

    return {
        success: success,
        error: error,
        subscribe: subscribe 
    };
};

// Http client wrapping the XMLHttpRequest API
// All the methods return an httpResponseObservable
// that can be subscribed to
var http = (function() {
    var apiEndpoint = "http://10.1.203.28:5000";
    apiEndpoint = "http://localhost:5000";

    function createHttpRequestObject() {
        var httpRequest = new XMLHttpRequest();

        httpRequest.withCredentials = true;
        httpRequest.responseType = 'text'; // json is not fully supported

        return httpRequest;
    }

    function handleHttpResponse(httpRequest, httpResponseObservable) {
        try {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                result = httpRequest.response;

                try {
                    result = JSON.parse(result);
                }
                catch (ex) {
                    httpResponseObservable.error(0, ex);
                }

                var status = httpRequest.status;

                var isSuccess = status >= 200 && status < 300 || status === 304;

                if (isSuccess) {
                    httpResponseObservable.success(status, result);
                } else {
                    httpResponseObservable.error(status, result);
                }

            } else {
                // Do nothing
            }
        } 
        catch (e) {
            console.log("Exception while handling response", e);
        }
    }

    function httpGet(url) {
        var httpRequest = createHttpRequestObject();
        var responseObservable = httpResponseObservable();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest, responseObservable);
        };

        httpRequest.open('GET', apiEndpoint + url, true);

        httpRequest.send();

        return responseObservable;
    }

    function httpPost(url, data, contentType)
    {
        var httpRequest = createHttpRequestObject();
        var responseObservable = httpResponseObservable();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest, responseObservable);
        };

        httpRequest.open('POST', apiEndpoint + url);
    
        // If contentType is defined
        if (contentType) {
            httpRequest.setRequestHeader('Content-Type', contentType);
        }

        // A post request doesn't always have to have data
        if (data) {
            httpRequest.send(data);
        } else {
            httpRequest.send();
        }

        return responseObservable;
    }

    function httpDelete(url)
    {
        var httpRequest = createhttpRequestObject();
        var responseObservable = httpResponseObservable();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest, responseObservable);
        };

        httpRequest.open('DELETE', apiEndpoint + url);

        httpRequest.send();

        return responseObservable;
    }

    return {
        get: function(url) {
            return httpGet(url);
        },
        post: function(url, data, contentType) {
            return httpPost(url, data, contentType);
        },
        delete: function(url) {
            return httpDelete(url); 
        }
    };
})();


