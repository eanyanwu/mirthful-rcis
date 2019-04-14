var React = require('react');
var Redirect = require('react-router-dom').Redirect;

var api = require('../utils/api');

class Login extends React.Component{
    constructor(props){
        super(props);

        this.state = {
            username: '',
            password: '' 
        };

        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleCredentialSubmit = this.handleCredentialSubmit.bind(this);
    }

    handleUsernameChange(event) {
        var value = event.target.value;
        this.setState(function(){
            return {
                username: value 
            };
        });
    }

    handlePasswordChange(event) {
        var value = event.target.value;
        this.setState(function() {
            return {
                password: value
            };
        });
    }

    handleCredentialSubmit(event) {
        event.preventDefault();

        console.log("Authenticating with: ", this.state.username, this.state.password);

        api.login(this.state.username, this.state.password)
            .then(function(result) {
                console.log(result);
            });
    }


    render() {
        return (
            <div>
                <form id='login-form'>
                    <label htmlFor='username'>Username:</label>
                    <input
                        type='text'
                        id='username'
                        name='username'
                        value={this.state.username}
                        onChange={this.handleUsernameChange}
                    />

                    <label htmlFor='password'>Password:</label>
                    <input 
                        type='password'
                        id='password'
                        name='password'
                        value={this.state.password}
                        onChange={this.handlePasswordChange}
                    />
                </form>
                <button
                    form='login-form'
                    type='buttom'
                    onClick={this.handleCredentialSubmit}>Submit</button>
            </div>
        );
    }
}

module.exports = Login
