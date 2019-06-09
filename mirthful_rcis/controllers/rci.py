from mirthful_rcis.lib import (
    common,
    librci,
    libroom,
    libuser
)
from mirthful_rcis.lib.authentication import login_required 

from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask import g

bp = Blueprint('rci', __name__)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """
    This view allows for creating a new rci
    """
    building_manifest = libroom.get_building_manifest() 
    users = libuser.get_users()

    if request.method == 'GET':

        return render_template('rci/new_rci_building_select.html',
                               building_manifest=building_manifest,
                               users=users)

    # Get the form contents
    user_id = request.form.get('user_id', None)
    building_name = request.form.get('building_name', None)
    room_name = request.form.get('room_name', None)


    # Can't create rci just yet, missing info...
    if user_id is None or building_name is None :
        return render_template('rci/new_rci_building_select.html',
                               building_manifest=building_manifest,
                               users=users)

    # Can't create rci just yet, missing info..
    elif room_name is None:
        user = common.get_user_record(user_id)
        new_rci = {
            'user_id': user_id,
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'building_name': building_name,
            'rooms': [ 
                x['room_name'] for x in building_manifest[building_name]
            ]
        }

        return render_template('rci/new_rci_room_select.html',
                               new_rci=new_rci)

    # We have all the information we need, create the rci...
    else:
        rci = librci.create_rci(user_id=user_id,
                          building_name=building_name,
                          room_name=room_name)

        return redirect(url_for('rci.edit', rci_id=rci['rci_id']))


@bp.route('/edit/<uuid:rci_id>', methods=['GET', 'POST'])
@login_required
def edit(rci_id):
    """
    The view for editing the contents of an rci document
    """
    rci_id = str(rci_id)

    if request.method == 'GET':
        rci = librci.get_rci_by_id(rci_id, full=True)
        return render_template('rci/edit.html', rci=rci)


