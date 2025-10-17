from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS # for cross-origin requests front and back ends
from datetime import timedelta, date
from db import connect_db

import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.config['SECRET_KEY'] = 'drones-dhyoa'   # for encrypting 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)    # session life span
CORS(app)       # for cross-origin front and back


@app.route('/ping')
def ping():
    return jsonify({'message' : 'pong'}),200


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
                ON CONFLICT (email) DO NOTHING"
        query_placer = (_email,_password,_full_name,_institution,_birthdate)

        cursor.execute(query, query_placer)
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            resp = jsonify({'message' : 'Email already exists'})
            resp.status_code = 400
            return resp
        else:
            cursor.close()
            conn.close()
            return jsonify({'message' : 'Register successful'})
    
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
        query = "SELECT email,psswd FROM pilots WHERE email=%s"
        query_placer = (_email,)

        cursor.execute(query, query_placer)
        row = cursor.fetchone() # should only return one
        cursor.close()
        conn.close()
        
        # verify password
        if row:
            email = row['email']
            password = row['psswd']
            
            if check_password_hash(password, _password):
                session['email'] = email
                cursor.close()
                return jsonify({'message' : 'Logged in'})
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


@app.route('/logout')
def logout():
    # remove from session
    if 'email' in session:
        session.pop('email', None)
    return jsonify({'message' : 'Logged out'})


if __name__ == '__main__':
    app.run()