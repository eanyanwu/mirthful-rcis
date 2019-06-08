import mirthful_rcis.rcicore as core
import mirthful_rcis.authentication as auth
from mirthful_rcis.custom_exceptions import Unauthorized, BadRequest

import json
import uuid
from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask import g

bp = Blueprint('rcis', __name__)

# ROUTING 

@bp.route('/', methods=['GET'])
@auth.login_required
def dashboard():
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
        rci_list = core.get_user_rcis(user_id=user['user_id'])

        return render_template('rcis/dashboard.html', rcis=rci_list)

    elif user.get('role') == 'admin' or user.get('role') == 'res_life_staff':
        buildings = list(core.get_building_manifest().keys())
        rci_list = core.get_building_rcis(buildings=buildings)

        return render_template('rcis/dashboard.html', rcis=rci_list)


@bp.route('/new', methods=['GET', 'POST'])
@auth.login_required
def new():
    """
    This view allows for creating a new rci
    """
    building_manifest = core.get_building_manifest() 
    users = core.get_users()

    if request.method == 'GET':

        return render_template('rcis/new_rci_building_select.html',
                               building_manifest=building_manifest,
                               users=users)

    # Get the form contents
    user_id = request.form.get('user_id', None)
    building_name = request.form.get('building_name', None)
    room_name = request.form.get('room_name', None)


    # Can't create rci just yet, missing info...
    if user_id is None or building_name is None :
        return render_template('rcis/new_rci_building_select.html',
                               building_manifest=building_manifest,
                               users=users)

    # Can't create rci just yet, missing info..
    elif room_name is None:
        user = core.get_user_record(user_id)
        new_rci = {
            'user_id': user_id,
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'building_name': building_name,
            'rooms': [ 
                x['room_name'] for x in building_manifest[building_name]
            ]
        }

        return render_template('rcis/new_rci_room_select.html',
                               new_rci=new_rci)

    # We have all the information we need, create the rci...
    else:
        rci = core.create_rci(user_id=user_id,
                          building_name=building_name,
                          room_name=room_name)

        return redirect(url_for('rcis.edit', rci_id=rci['rci_id']))


@bp.route('/edit/<uuid:rci_id>', methods=['GET', 'POST'])
@auth.login_required
def edit(rci_id):
    """
    The view for editing the contents of an rci document
    """
    rci_id = str(rci_id)

    if request.method == 'GET':
        rci = core.get_full_rci_document(rci_id)
        return render_template('rcis/edit.html', rci=rci)



@bp.route('/api/rooms', methods=['GET'])
@auth.login_required
def get_rooms():
    return create_json_response(data=core.get_building_manifest(), status_code=200)


@bp.route('/api/rooms/areas', methods=['GET'])
@auth.login_required
def get_room_areas():
    return create_json_response(data=core.get_room_areas(), status_code=200)

## RCIS

@bp.route('/api/rcis/<uuid:rci_id>', methods=['GET'])
@auth.login_required
def get_rci(rci_id):
    """
    Return an existing rci
    """

    rci = core.get_rci(str(rci_id))
    
    return create_json_response(data=rci, status_code=200)

@bp.route('/api/rcis', methods=['GET'])
@auth.login_required
def get_rcis():
    """
    Return a list of rcis that match the filter that was passed in
    """
    query_params = request.args

    if query_params is None:
        raise BadRequest('No filter parameters were defined!')

    filter_type = query_params.get('filter_type')
    filter_values = query_params.getlist('filter_value')

    if filter_type is None:
        raise BadRequest('No filter type was defined!')
    
    filter_type = rci_filter.RciFilterType[filter_type]

    filter_params = {
        'filter_type': filter_type,
        'filter_value': filter_values
    }

    rcis = core.get_rcis(filter_params)

    return create_json_response(data=rcis, status_code=200) 


@bp.route('/api/rcis', methods=['POST'])
@auth.login_required
def post_rci():
    """
    Create a new rci document
    """
    user_id = g.get('user')['user_id']

    # Get posted data
    request_data = request.get_json()  

    if request_data is None:
        raise BadRequest('no data was sent with the request to create rci')

    building_name = request_data.get('building_name', None)
    room_name = request_data.get('room_name', None)

    if room_name is None:
        raise BadRequest('room name not provided in request')

    if building_name is None:
        raise BadRequest('building name not provided in request')

    new_rci = core.post_rci(user_id=user_id, 
                            building_name=building_name, 
                            room_name=room_name)

    return create_json_response(new_rci, 200, {}) 


@bp.route('/api/rcis/<uuid:rci_id>', methods=['DELETE'])
@auth.login_required
def delete_rci(rci_id):
    """
    Delete an rci document
    """
    user = g.get('user')

    rci_id = str(rci_id)

    core.delete_rci(rci_id, user)

    return create_json_response(status_code=200)


@bp.route('/api/rcis/<uuid:rci_id>/lock', methods=['POST'])
@auth.login_required
def lock_rci(rci_id):
    """
    Freeze the rci to prevent it from being modified further
    """
    user = g.get('user')

    rci_id = str(rci_id)

    core.lock_rci(rci_id, user)

    return create_json_response(status_code=200)


@bp.route('/api/rcis/<uuid:rci_id>/lock', methods=['DELETE'])
@auth.login_required
def unlock_rci(rci_id):
    """
    Unlock an rci -- allowing it to be modified
    """
    user = g.get('user')

    rci_id = str(rci_id)

    core.unlock_rci(rci_id, user)

    return create_json_response(status_code=200)


## DAMAGES

@bp.route('/api/rcis/<uuid:rci_id>/damages', methods=['POST'])
@auth.login_required
def post_damage(rci_id):
    """
    Record a damage on the rci
    """
    user = g.get('user') 
    rci_id = str(rci_id)
    data = request.get_json()

    if data is None:
        raise BadRequest('Malformed json {}'.format(request.data))

    item = data.get('item', None)
    text = data.get('text', None)
    url = data.get('image_url', None)

    if item is None:
        raise BadRequest('item is None')

    if text is None:
        raise BadRequest('damage text is None')

    damage = core.post_damage(user, rci_id, item, text, url)

    return create_json_response(damage, 200)


@bp.route('/api/rcis/<uuid:rci_id>/damages/<uuid:damage_id>', methods=['DELETE'])
@auth.login_required
def delete_damage(rci_id, damage_id):
    """
    Delete an rci attachment
    """

    user = g.get('user')
    rci_id = str(rci_id)
    damage_id = str(damage_id)

    core.delete_damage(rci_id, damage_id, user)

    return create_json_response({}, 200)

## UTILITY METHODS
def create_error_response(message=None, 
                          status_code=None,
                          extra_headers=None):

    error = { 'error_message': message }

    if not status_code:
        status_code = 400

    return create_json_response(error, status_code, extra_headers)


def create_json_response(data=None, status_code=None, extra_headers=None):
    if not extra_headers:
        extra_headers = {}

    if not status_code:
        status_code = 200

    # Set the application/json mimetype
    extra_headers['Content-Type'] = 'application/json'

    return (json.dumps(data), status_code, extra_headers)

