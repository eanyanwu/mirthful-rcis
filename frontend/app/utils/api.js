var Axios = require('axios');

function login(username, password) {
    return Axios.post('http://localhost:5000/login', {
        username: username,
        password: password
    });
}
module.exports = {
    login: login
}
