import sqlite3
from flask import Flask
from flask import request
from flask import session
from flask import json
from flask import abort

app = Flask(__name__)
app.secret_key = b'qwerty' # TODO: obviously change this

@app.route('/session/<string:user_id>', methods=['GET'])
def start_session(user_id):
    # Connect to the database
    connection = sqlite3.connect('./rci.db')
    
    # Use sqlite3.Row as a row_factory so that we can access our rows by column name
    connection.row_factory = sqlite3.Row

    # What even is a cursor
    cursor = connection.cursor()

    # Find the user in question
    user_record = cursor.execute("""
    SELECT * 
    FROM users
    WHERE user_id = ?""", (user_id,)).fetchone()

    if not user_record:
        abort(401)

    session['user_id'] = user_record['user_id']

    return json.jsonify({})
