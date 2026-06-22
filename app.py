import os

from flask import Flask, render_template, url_for, request, flash, current_app, jsonify
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import uuid
import re

app = Flask(__name__)

app.secret_key = 'secret'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1801'
app.config['MYSQL_DATABASE_DB'] = 'students'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'Student Main Portal'
    return render_template('home.html', pageTitle = title)

@app.route('/student/portal', methods=['GET', 'POST'])
def home():
    title = 'JSchool Student Portal'
    return render_template('student-form.html', pageTitle = title)

@app.route('/add_details', methods=['POST'])
def add_details():
    req = request.get_json()
    
    is_valid = True
    invalid_txt = ''

    def mark_invalid(msg):
        nonlocal is_valid, invalid_txt
        is_valid = False
        invalid_txt = msg

    if not req.get('firstName', '').strip():
        mark_invalid('First Name')

    elif not req.get('lastName', '').strip():
        mark_invalid('Last Name')

    elif not req.get('email', '').strip():
        mark_invalid('Email')

    else:
        email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        if not re.match(email_pattern, req['email']):
            mark_invalid('Email')

    if not req.get('dob', '').strip():
        mark_invalid('Date of Birth')

    if not req.get('gender', '').strip():
        mark_invalid('Gender')

    if not req.get('phoneNumber', '').strip():
        mark_invalid('Phone Number')

    if not req.get('address', '').strip():
        mark_invalid('Address')

    region = req.get('regionOfOrigin', '').strip()
    if not region or region.lower() == "select region":
        mark_invalid('Region')

    district = req.get('districtOfOrigin', '').strip()
    if not district or district.lower() == "select district":
        mark_invalid('District')

    if not req.get('nextOfKin', '').strip():
        mark_invalid('Next of Kin')

    agg = req.get('wassceAggregate', '').strip()
    if not agg or not agg.isdigit() or not (6 <= int(agg) <= 54):
        mark_invalid('Aggregate')

    if not is_valid:
        return jsonify({
            "status": "error",
            "message": f"{invalid_txt} is invalid"
        }), 400

    try:
        print("Saving data:", req)
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO student_details (
                first_name, middle_name, last_name, email, dob, gender,
                phone_number, address, region_of_origin, district_of_origin,
                next_of_kin, wassce_aggregate, status, photo_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            req.get('firstName'), req.get('middleName'), req.get('lastName'),
            req.get('email'), req.get('dob'), req.get('gender'), req.get('phoneNumber'),
            req.get('address'), req.get('regionOfOrigin'), req.get('districtOfOrigin'),
            req.get('nextOfKin'), req.get('wassceAggregate'), req.get('status'), req.get('photoId')
        ))
        conn.commit()
        cur.close()
        flash('Operation successful!', 'flash_success')

        return jsonify({
            "status": "success",
            "message": "Data saved successfully"
        }), 200

    except Exception as e:
        print (e)
        return jsonify({
            "status": "error",
            "message": "Server error while saving data"
        }), 500

@app.route('/add_image', methods=['POST'])
def add_profile_pic():
    image = request.files.get('file')
    if not image:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    try:
        photo_id = uuid.uuid4().hex
        filepath = os.path.join(current_app.root_path, 'static/images/' + photo_id +'.png')
        image.save(filepath)
        return jsonify({"status": "success", "message": "Image uploaded successfully", "photo_id": photo_id}), 200
    
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Failed to save image"}), 500

@app.route('/admin/dashboard')
def admin_panel():
    title = 'Admin Portal: Dashboard'

    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from student_details')
    rv = cur.fetchall()

    return render_template('index.html', pageTitle = title, students = rv)

@app.route('/student/<id>/view', methods=['GET'])
def student_profile(id):
    title = 'Student Profile'
    student_id = id

    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student_details WHERE id=%s', (student_id))
    rv = cur.fetchall()
    
    return render_template('students-index.html', pageTitle = title, student = rv)

@app.route('/student/edit', methods=['POST'])
def edit_student():
    req = request.get_json()
    student_id = req.get('id')
    status = req.get('status').lower()

    if status.lower() == 'admitted' or status.lower() == 'pending' or status.lower() == 'rejected':
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('UPDATE student_details SET status=%s WHERE id=%s', (status, student_id))
        conn.commit()
        cur.close()
        flash('Student Admission Status Updated Successfully!', 'flash_success')
        return json.dumps('success')
    
    else:
        flash('Failed to Update Student Admission Status!', 'flash_error')
        return json.dumps('error')

@app.route('/admin/<source>/<key>/search')
def search(source, key):
    title = 'Admin Portal: Dashboard'

    if key and source:
        conn = mysql.get_db()
        cur = conn.cursor()

        if source == 'name':
            cur.execute("SELECT * FROM student_details WHERE first_name LIKE %s OR last_name LIKE %s",
            (f"%{key}%", f"%{key}%"))
        elif source == 'status':
            cur.execute('SELECT * FROM student_details WHERE status=%s;', f"{key}")
        elif source == 'gender':
            cur.execute('SELECT * FROM student_details WHERE gender=%s;', f"{key}")
        elif source == 'agg':
            cur.execute('SELECT * FROM student_details WHERE wassce_aggregate=%s;', f"{key}")

        rv = cur.fetchall()
        print(rv)
        return render_template('index.html', pageTitle = title, students = rv)
    
    else:
        rv = [{}]
        return render_template('index.html', pageTitle = title, students = rv)

if __name__ == "__main__":
    app.run(debug=True)