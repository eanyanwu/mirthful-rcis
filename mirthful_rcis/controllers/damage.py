from mirthful_rcis.lib import (
    common,
    librci,
    libroom,
    libuser,
    libdamage
)
from mirthful_rcis.lib.authentication import login_required 

from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask import g

bp = Blueprint('damage', __name__, url_prefix="/damage")

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """
    This view allows for creating a new damage 
    """
    

    default_room_areas = [ 
        x['room_area_name']
        for x in libroom.get_default_room_areas()
    ]

    if request.method == 'GET':
        # If this is a get request, these will be query parameters
        user_id = request.args['user_id']
        rci_id = request.args['rci_id']

        return render_template('damage/new.html', 
                               room_areas=default_room_areas,
                               user_id=user_id,
                               rci_id=rci_id)

    rci_id = request.form['rci_id']
    item = request.form['item']
    text = request.form['text']
    logged_in_user = g.user

    libdamage.create_damage(logged_in_user=logged_in_user,
                            rci_id=rci_id,
                            item=item,
                            text=text,
                            image_url=None)

    return redirect(url_for('rci.edit', rci_id=rci_id))

@bp.route('/delete/<uuid:damage_id>', methods=['GET'])
@login_required
def delete(damage_id):
    """
    Deletes the damage with the given id
    """
    logged_in_user = g.user
    damage_id = str(damage_id)

    deleted_damage = libdamage.delete_damage(damage_id=damage_id, 
                                             logged_in_user=logged_in_user)

    rci_id = deleted_damage['rci_id']

    return redirect(url_for('rci.edit', rci_id=rci_id))

