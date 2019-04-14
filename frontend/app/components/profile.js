var React = require('react');

var Redirect = require('react-router-dom').Redirect;

class Profile extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            // state
        };
    }

    render() {
        return (
            <div>
                <h1>This is the profile page for {this.props.userEmail}</h1>
                <h3>Nav bar could be here</h3>
            </div>
        );
    }
}

module.exports = Profile
