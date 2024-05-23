from flask import Flask, render_template, redirect, url_for, request, jsonify, g
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database.db'
cur_user = None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr_reader')
def qr_reader():
    return render_template('qr_reader.html')

@app.route('/main_menu')
def main_menu():
    name = request.args.get('name')
    phone = request.args.get('phone')
    user_id = request.args.get('ID')
    return render_template('main_menu.html', name=name, phone=phone, user_id=user_id)

@app.route('/dispose_oil')
def dispose_oil():
    name = request.args.get('name')
    phone = request.args.get('phone')
    user_id = request.args.get('id')
    return render_template('dispose_oil.html', name=name, phone=phone, user_id=user_id)

@app.route('/history')
def history():
    name = request.args.get('name')
    phone = request.args.get('phone')
    user_id = request.args.get('id')
    return render_template('history.html', name=name, phone=phone, user_id=user_id)

@app.route('/view_records')
def view_records():
    # 처리 로직을 여기에 추가하세요.
    return "수거내역 확인하기 페이지"

@app.route('/process_qr', methods=['POST'])
def process_qr():
    global cur_user

    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    cur_user = data.get('ID')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO log (name, phone, user_id, timestamp) VALUES (?, ?, ?, ?)', (name, phone, cur_user, timestamp))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User data saved.'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)