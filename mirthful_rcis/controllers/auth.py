from mirthful_rcis.lib.authentication import (
    login_required, 
    validate,
    start_session,
    end_session
)

from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in a user by creating a new session for them in the database

    The session id is sent back in a cookie called `session`
    """
    # If this is a get request, just spit back the login form 
    if request.method == 'GET':
        return render_template('auth/login.html', error={})

    # If not, this is an attempt to login
    username = request.form['username']
    password = request.form['password']

    if validate(username, password):
        session_id = start_session(username)

        response = make_response(redirect(url_for('dashboard.main')))

        response.headers['Set-Cookie'] = 'session={}; Path=/'.format(session_id)

        return response
    else:
        error = {
            'message': 'Invalid login. Please try again.',
            'username': username,
            'password': password
        }

        return render_template('auth/login.html', error=error)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Logout the existing user by deleting their session from the database
    """

    rci_session = request.cookies.get('session')

    end_session(rci_session)

    return redirect(url_for('auth.login'))
