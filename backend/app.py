from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS # for cross-origin requests front and back ends
from datetime import timedelta, date
from db import connect_db

import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'drones-dhyoa'
app.config['SECRET_KEY'] = 'drones-dhyoa'   # for encrypting 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)    # session life span
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,    # required for SAMESITE
)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])  # for cross-origin front and back with session credentials


@app.route('/ping')
def ping():
    return jsonify({'message' : 'pong'}),200


'''
@app.route('/')
def home():
    # check if session is active with credentials
    conn = connect_db()
    if 'email' in session:
        email = session['email']
        return jsonify({'message' : 'Already logged in', 'email' : email})
    else:
        resp = jsonify({'message' : 'Unauthorized access'})
        resp.status_code = 401
        return resp
'''


@app.route('/register', methods=['POST'])
def register():
    # receive credentials
    _json = request.json
    _email = _json['email']
    _password = generate_password_hash(_json['password'])
    _full_name = _json['full_name']
    _institution = _json['institution']
    _birthdate = _json['birthdate']
    print(request.json)

    if _email and _password and _institution and _birthdate:
        # connect to database
        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp

        # insert credentials without duplicated emails
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "INSERT INTO pilots (email, psswd, full_name, institution, birthdate) \
                VALUES (%s, %s, %s, %s, %s) \
                ON CONFLICT (email) DO NOTHING \
                RETURNING id"
        query_placer = (_email,_password,_full_name,_institution,_birthdate)

        cursor.execute(query, query_placer)
        conn.commit()

        if cursor.rowcount == 0:    # empty query response
            cursor.close()
            conn.close()
            resp = jsonify({'message' : 'Email already exists'})
            resp.status_code = 400
            return resp
        else:
            pilot_id = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            session['pilot_id'] = pilot_id
            session['email'] = _email

            print(session)
            return jsonify({'message' : 'Register successful'}), 200
    
    else:
        resp = jsonify({'message' : 'Missing profile credentials'})
        resp.status_code = 400
        return resp


@app.route('/login', methods=['POST'])
def login():
    # receive login credentials
    _json = request.json
    _email = _json['email']
    _password = _json['password']
    print(_email)

    if _email and _password:
        # connect to database
        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp

        # check user exists
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT id,email,psswd FROM pilots WHERE email=%s"
        query_placer = (_email,)

        cursor.execute(query, query_placer)
        row = cursor.fetchone() # should only return one
        cursor.close()
        conn.close()
        
        # verify password
        if row:
            pilot_id = row['id']
            email = row['email']
            password = row['psswd']
            
            if check_password_hash(password, _password):
                session['email'] = email
                session['pilot_id'] = pilot_id
                print(session)
                return jsonify({'message' : 'Logged in'}), 200
            else:
                resp = jsonify({'message' : 'Incorrect password'})
                resp.status_code = 400
                return resp
        else:       # empty query results
            resp = jsonify({'message' : 'Incorrect credentials'})
            resp.status_code = 400
            return resp

    else:
        resp = jsonify({'message' : 'Missing credentials'})
        resp.status_code = 400
        return resp


@app.route('/logout', methods=['POST'])
def logout():
    # remove from session
    session.clear()
    return jsonify({'message' : 'Logged out'}), 200


@app.route('/pilot', methods=['GET'])
def get_current_pilot():
    print(session)
    if 'pilot_id' in session:
        return jsonify({'id': session['pilot_id'], 'email': session['email']})
    else:
        print('pilot not in session')
        return jsonify({'error': 'Not logged in'}), 401


@app.route('/drones', methods=['GET'])
def get_drones():
    print(session)
    if 'pilot_id' in session:

        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT id,short_name,serial_number FROM drones WHERE user_id=%s"
        query_placer = (session['pilot_id'],)

        cursor.execute(query, query_placer)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        drones = [{"id": d[0], "short_name": d[1], "serial_number": d[2]} for d in rows]
        return jsonify(drones), 200


@app.route('/drone_models', methods=['GET'])
def get_drone_models():
    conn = connect_db()
    if conn == False:
        resp = jsonify({'message' : 'No connection to db'})
        resp.status_code = 400
        return resp
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT id,manufacturer,model FROM drone_models \
            WHERE sdk_version >= 5"

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    models = result = [{"id": m[0], "manufacturer": m[1], "model": m[2]} for m in rows]
    return jsonify(models), 200


@app.route('/new_drone', methods=['POST'])
def add_new_drone():
    # receive credentials
    _json = request.json
    _user_id = _json['user_id']
    _drone_model_id = _json['drone_model_id']
    _serial_number = _json['serial_number']
    _short_name = _json['short_name']
    _payload = _json['payload']
    print(request.json)

    if _user_id and _drone_model_id and _serial_number:
        # connect to database
        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp

        # insert credentials without duplicated emails
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "INSERT INTO drones (user_id, drone_model_id, serial_number, short_name, payload) \
                VALUES (%s, %s, %s, %s, %s) \
                ON CONFLICT (serial_number) DO NOTHING \
                RETURNING id"
        query_placer = (_user_id,_drone_model_id,_serial_number,_short_name,_payload)

        cursor.execute(query, query_placer)
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            resp = jsonify({'message' : 'Serial number already exists'})
            resp.status_code = 400
            return resp
        else:
            cursor.close()
            conn.close()

            return jsonify({'message' : 'Drone registeration successful'}), 200
    
    else:
        resp = jsonify({'message' : 'Missing drone parameters'})
        resp.status_code = 400
        return resp


@app.route('/flights', methods=['GET'])
def get_flights():
    
    drone_id = request.args.get('drone_id')
    if 'pilot_id' in session and drone_id:

        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT id,type,flight_date,state,description FROM flights WHERE pilot_id=%s AND drone_id=%s"
        query_placer = (session['pilot_id'],drone_id,)

        cursor.execute(query, query_placer)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        drones = [{"id": f[0], "type": f[1], "date": f[2], "state": f[3], "description": f[4]} for f in rows]
        return jsonify(drones), 200


@app.route('/new_flight', methods=['POST'])
def add_new_flight():
    # receive credentials
    _json = request.json
    _drone_id = _json['drone_id']
    _pilot_id = _json['pilot_id']
    _state = _json['state']
    _type = _json['type']
    print(request.json)

    if _drone_id and _pilot_id and _state and _type:
        # connect to database
        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "INSERT INTO flights (drone_id, pilot_id, state, type) \
                VALUES (%s, %s, %s, %s)"
        query_placer = (_drone_id,_pilot_id,_state,_type)

        cursor.execute(query, query_placer)
        conn.commit()
    
        cursor.close()
        conn.close()

        return jsonify({'message' : 'Flight registeration successful'}), 200
    
    else:
        resp = jsonify({'message' : 'Missing flight parameters'})
        resp.status_code = 400
        return resp


@app.route('/update_flight', methods=['POST'])
def update_flight():
    # receive credentials
    _json = request.json
    _flight_id = _json['flight_id']
    _description = _json['description']
    print(request.json)

    if _flight_id:
        # connect to database
        conn = connect_db()
        if conn == False:
            resp = jsonify({'message' : 'No connection to db'})
            resp.status_code = 400
            return resp

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "UPDATE flights SET \
                description = %s, state = 'finished', flight_date = CURRENT_TIMESTAMP \
                WHERE id = %s"
        query_placer = (_description, _flight_id)

        cursor.execute(query, query_placer)
        conn.commit()
    
        cursor.close()
        conn.close()

        return jsonify({'message' : 'Flight update successful'}), 200
    
    else:
        resp = jsonify({'message' : 'Missing flight parameters'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()