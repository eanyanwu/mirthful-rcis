from mirthful_rcis.lib import (
    libroom,
    librci,
    libuser
)

from mirthful_rcis.lib.authentication import login_required

from mirthful_rcis.lib.exceptions import (
    Unauthorized
)

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
    """
    logged_in_user = g.user

    # 1 - Fetch user settings for default buildings the user can view.
    #     1.1 If such a setting does not exist, default to all buildings
    # 2 - Try to fetch the rcis for the list of buildings we have.
    #     2.1 - If the call fails with `Unauthorized`, the user has no such access
    #           Fetch their own rcis only

    user_settings = libuser.get_user_settings(user_id=
                                              logged_in_user['user_id'])

    building_list = user_settings['default_buildings']

    if building_list is None:
        building_list = list(libroom.get_building_manifest().keys())

    try:
        rcis = librci.get_rcis_for_buildings(buildings=building_list,
                                             logged_in_user=logged_in_user)
    except Unauthorized:
        rcis = librci.get_rcis_for_user(user_id=logged_in_user['user_id'],
                                        logged_in_user=logged_in_user)

    
    user_permissions = libuser.get_user_permissions(user_id=logged_in_user['user_id'])

    permissions = {
        'user': user_permissions,
        'for_search': Permission.MODERATE_RCIS,
        'for_system_settings': Permissions.MODERATE_SYSTEM 
    }

    return render_template('dashboard/main.html',
                           rcis=rcis,
                           permissions=permission)



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

