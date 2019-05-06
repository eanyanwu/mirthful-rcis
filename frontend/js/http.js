// An observablec wrapping the result of an http request.
var httpResponseObservable = function() {

    // We create an initial structure for the observable object
    var _innerObservable = observable({
        success: false,
        statusCode: 0,
        error: null,
        response: null
    });

    // A flag to indicate if the http request has completed.
    // This will allow us to give the result to listeners who subscribed
    // after the change actually happened
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

var http = (function() {
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

        httpRequest.open('GET', url, true);

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

        httpRequest.open('POST', url);
    
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

        httpRequest.open('DELETE', url);

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


