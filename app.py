import os
from flask import Flask, render_template, current_app, g, jsonify, request
import sqlite3 as sql
from datetime import datetime as dt

app = Flask('WheresHansel')

dblocation = os.environ('PERSISTENT_STORAGE')

def get_pwd_path():
    dirpath = dblocation
    DBPATH = dirpath + '/locations.db'
    return DBPATH

def init_db(db):
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())
    print('schema updated successfully')

def get_db():
    if 'db' not in g:
        DATABASE = get_pwd_path()
        if not os.path.exists(DATABASE):
            g.db = sql.connect(DATABASE)
            init_db(g.db)
        else:
            g.db = sql.connect(DATABASE)
        print('version' + sql.version)
    return g.db

def close_connection():
    if 'db' in g:
        g.db.close()
    else:
        print('not connected')

@app.route("/", methods = ['GET'])
def home():
    return jsonify({'id': 'myApi'})

@app.route("/v1/addnew", methods = ['POST'])
def add_new_location():
    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
    except TypeError:
        return jsonify({'status': 'contain thyself'})
    except ValueError:
        return jsonify({'status': '-_- ...plz'})
        
    if -90 < latitude < 90.0 and -90.0 < longitude < 90.0:
        time = dt.now()
        sqlstring = "INSERT INTO locations (latitude, longitude, time) VALUES(?,?,?)"
        db = get_db()
        cur = db.cursor()
        cur.execute(sqlstring,(latitude, longitude, str(time)))
        db.commit()
        return jsonify({'status': cur.lastrowid})
    else:
        return jsonify({'status': 'coordinates type error'})
    

@app.route("/v1/getlatest", methods = ['GET'])
def get_latest_location():
    cur = get_db().cursor()
    result = cur.execute('SELECT * FROM locations ORDER BY id DESC LIMIT 1;').fetchone()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
