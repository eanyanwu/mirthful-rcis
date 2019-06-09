from mirthful_rcis.lib import libroom 
from mirthful_rcis.lib import librci
from mirthful_rcis.lib.authentication import login_required

from flask import Blueprint
from flask import render_template 
from flask import g

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=['GET'])
@login_required
def main():
    """
    The dashboard always shows a list of rcis.
    What rcis are listed depends on the user's role and settings

    - student: only list rcis for which they are a collaborator

    - res_life_staff and admin: list all rcis by building. If building
      preferences have been set, use those to filter 
    """

    user = g.get('user')

    rci_list = []

    if user.get('role') == 'student':
        rci_list = librci.get_rcis_for_user(user_id=user['user_id'])

        return render_template('dashboard/main.html', rcis=rci_list)

    elif user.get('role') == 'admin' or user.get('role') == 'res_life_staff':
        buildings = list(libroom.get_building_manifest().keys())
        rci_list = librci.get_rcis_for_buildings(buildings=buildings)

        return render_template('dashboard/main.html', rcis=rci_list)

