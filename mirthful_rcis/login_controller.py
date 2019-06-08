import mirthful_rcis.authentication as auth
from mirthful_rcis.custom_exceptions import BadRequest

from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('login', __name__)

## LOGIN

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in a user by creating a new session for them in the database

    The session id is sent back in a cookie called `session`
    """
    # If this is a get request, just spit back the login form 
    if request.method == 'GET':
        return render_template('login/login.html', error={})

    # If not, this is an attempt to login
    username = request.form['username']
    password = request.form['password']

    if auth.validate(username, password):
        session_id = auth.start_session(username)

        response = make_response(redirect(url_for('rcis.dashboard')))

        response.headers['Set-Cookie'] = 'session={}'.format(session_id)

        return response
    else:
        error = {
            'message': 'Invalid login. Please try again.',
            'username': username,
            'password': password
        }

        return render_template('login/login.html', error=error)


@bp.route('/logout', methods=['GET'])
@auth.login_required
def logout():
    """
    Logout the existing user by deleting their session from the database
    """

    rci_session = request.cookies.get('session')

    auth.end_session(rci_session)

    return redirect(url_for('login.login'))
