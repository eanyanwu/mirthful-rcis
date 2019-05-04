var http = (function() {
    function createHttpRequestObject() {
        var httpRequest = new XMLHttpRequest();

        httpRequest.withCredentials = true;
        httpRequest.responseType = 'text'; // json is not fully supported

        return httpRequest;
    }

    function handleHttpResponse(httpRequest, success, error) {
        try {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                result = httpRequest.response;

                responseHeaders = httpRequest.getAllResponseHeaders();

                console.log(responseHeaders);

                if (httpRequest.status === 200) {
                    if (success) {
                        console.log(result);
                        success(JSON.parse(result));
                    }
                } else {
                    if (error) {
                        error(httpRequest.status, JSON.parse(result));
                    }
                }
            } else {
                // do nothing
            }
        } 
        catch (e) {
            console.log("Exception while handling response", e);
        }
    }

    function httpGet(url, successCallback, errorCallback) {
        var httpRequest = createHttpRequestObject();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest,
                successCallback,
                errorCallback);
        };

        httpRequest.open('GET', url, true);

        httpRequest.send();
    }

    function httpPost(url,
        data,
        contentType,
        successCallback,
        errorCallback) 
    {
        var httpRequest = createHttpRequestObject();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest,
                successCallback,
                errorCallback);
        };

        httpRequest.open('POST', url);

        httpRequest.setRequestHeader('Content-Type', contentType);

        httpRequest.send(data);
    }

    function httpDelete(url, successCallback, errorCallback)
    {
        var httpRequest = createhttpRequestObject();

        httpRequest.onreadystatechange = function() {
            handleHttpResponse(httpRequest,
                successCallback,
                errorCallback);
        };

        httpRequest.open('DELETE', url);

        httpRequest.send();
    }

    return {
        get: function(url, success, error) {
            httpGet(url, success, error);
        },
        post: function(url, data, contentType, success, error) {
            httpPost(url, data, contentType, success, error);
        },
        put: function() {
        },
        delete: function(url, success, error) {
            httpDelete(url, success, error);
        }
    }
})()


