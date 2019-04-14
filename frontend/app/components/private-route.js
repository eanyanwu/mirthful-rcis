var React = require('react');
var Redirect = require('react-router-dom').Redirect;

// Higher-order component for making routes only accessible when user is logged in.
// Note: I'm not fond of the ES6 spread operator for passing props, which is why I am am using the `createElement` method
// instread of JSX 
function PrivateRoute(isAuthenticated, WrappedComponent, wrappedComponentProps) {
    // If they are authenticated, simply return the component
    if (isAuthenticated) {
        return React.createElement(
            WrappedComponent,
            wrappedComponentProps
        );
    }
    // If they are not, redirect to the login page
    else {
        return React.createElement(
            Redirect,
            { to: '/login' }
        );
    }
}

module.exports = PrivateRoute;
