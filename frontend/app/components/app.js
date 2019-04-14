var React = require('react');
var ReactRouter = require('react-router-dom');
var Router = ReactRouter.HashRouter;
var Route = ReactRouter.Route;
var Link = ReactRouter.Link;
var Switch = ReactRouter.Switch;

var Login = require('./login');
var Profile = require('./profile');
var PrivateRoute = require('./private-route');

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isAuthenticated: false,
            userEmail: null,
            userSession: null
        }

        // (╯°□°)╯︵┻━┻ I can't believe I have to do this. 
        // For the curious, look up these terms "javascript function binding"
        this.onUserLogin = this.onUserLogin.bind(this);
        this.renderLogin = this.renderLogin.bind(this);
        this.renderProfile = this.renderProfile.bind(this);
    }

    // Method to be called once user is logged in so we can set the global state
    onUserLogin(email, sessionId) {
        console.log("Call back called with ", email, sessionId);
        this.setState(function() {
            return {
                isAuthenticated: true,
                userEmail: email,
                userSession: sessionId
            };
        });
    }

    // See [1] below
    renderProfile(routeProps) {
        return PrivateRoute(this.state.isAuthenticated,
            Profile, 
            { userEmail: this.state.userEmail }
        );
    }

    // See [1] below
    renderLogin(routeProps) {
        return (
            <Login location={routeProps.location} onUserLogin={this.onUserLogin} />
        );
    }

    // Notes:
    //
    // [1] In oder to pass props to the components associated with the routes.
    // React Router suggestions you use the `render` prop instead of the `component` prop.
    // See https://reacttraining.com/react-router/web/api/Route/render-func
    // Also see https://tylermcginnis.com/react-router-pass-props-to-components
    render() {
        return (
            <Router>
                <div className='container'>
                    <Switch>
                        <Route path="/login" render={this.renderLogin} />

                        <Route render={this.renderProfile} />
                    </Switch>
                </div>
            </Router>
        );
    }
}

module.exports = App;
