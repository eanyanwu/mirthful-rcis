from mirthful_rcis.lib.authentication import (
    login_required,
    admin_required
)

from flask import (
    Blueprint,
    render_template
)

bp = Blueprint('settings', __name__, url_prefix='/settings')

# TODO: Explain decorator order
@bp.route('/system', methods=['GET'])
@login_required
@admin_required
def system_settings():
    """
    Displays the main system settings page
    """

    return render_template('settings/system_settings.html')




