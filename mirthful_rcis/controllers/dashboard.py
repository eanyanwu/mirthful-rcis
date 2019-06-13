from mirthful_rcis.lib import libroom 
from mirthful_rcis.lib import librci
from mirthful_rcis.lib.authentication import login_required

from flask import (
    Blueprint,
    g,
    render_template,
    request
)

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=['GET'])
@login_required
def main():
    """
    The "homepage". This is what a user sees when they first log-in.

    - student: only list rcis for which they are a collaborator

    - res_life_staff and admin: list all rcis by building. If building
      preferences have been set, use those to filter 
    
    - admin: additional actions
    """

    logged_in_user = g.user

    rci_list = []

    if logged_in_user['role'] == 'student':
        rci_list = librci.get_rcis_for_user(user_id=logged_in_user['user_id'])

        return render_template('dashboard/main.html', rcis=rci_list)

    elif logged_in_user['role'] == 'res_life_staff':
        buildings = list(libroom.get_building_manifest().keys())
        rci_list = librci.get_rcis_for_buildings(buildings=buildings)

        return render_template('dashboard/main.html', rcis=rci_list)

    elif logged_in_user['role']  == 'admin':
        return render_template('dashboard/admin.html')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    A view for searching through the rci database
    """

    if request.method == 'GET': 
        # Get request without a query
        return render_template('dashboard/search.html')

    search_string = request.form['search_string']

    results = librci.search_rcis(search_string=search_string)

    return render_template('dashboard/search.html', 
                            search_string=search_string,
                            results=results)

