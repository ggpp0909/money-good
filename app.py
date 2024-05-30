from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from excel import append_to_excel, calculate_total_monthly_amount
import sqlite3
from datetime import datetime
import openpyxl
import serial
import actuator

app = Flask(__name__)
DATABASE = 'database.db'
FILE_PATH = 'data.xlsx'
cur_user = None
arduino_port = actuator.find_arduino_port()

ser = serial.Serial(arduino_port, 9600)
if arduino_port is None:
    print("Could not find an Arduino connected to the computer.")
    # exit()

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
    user_id = request.args.get('id')
    return render_template('main_menu.html', name=name, phone=phone, user_id=user_id)


@app.route('/dispose_oil')
def dispose_oil():
    name = request.args.get('name')
    phone = request.args.get('phone')
    user_id = request.args.get('id')
    return render_template('dispose_oil.html', name=name, phone=phone, user_id=user_id)

# 1. 폐식용유 버리기 -> 투입구 문열어야해
@app.route('/open_lid')
def open_lid():
    try:
        # 아두이노로 O보내서 열고 투입구 열기
        # actuator.send_command(ser, 'O', 3)
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'fail'})
    finally:
        ser.close()

# 2. 투입구 닫기 -> 투입구 닫고 무게 재서 리턴해야해
@app.route('/close_lid')
def close_lid():
    try:
        # 아두이노로 C보내서 열고 투입구 닫고 무게재서 리턴
        # weight = actuator.send_command(ser, 'C', 3)
        return jsonify({'status': 'success', 'weight': 1234})
    except:
        return jsonify({'status': 'fail'})
    finally:
        ser.close()

# 3. 다시재기 -> 닫힌상태 그대로 무게재서 리턴
@app.route('/calc_weight_again')
def calc_weight_again():
    try:
        # 아두이노로 R보내서 무게재서 리턴
        # weight = actuator.send_command(ser, 'R', 3)
        return jsonify({'status': 'success', 'weight': 1234})
    except:
        return jsonify({'status': 'fail'})
    finally:
        ser.close()


# 4. 마지막 확인 -> 아래 오일통으로 떨구기 (밑에 모터 열었다 기다렸다 닫기)
@app.route('/store_oil')
def store_oil():
    try:
        # 아두이노로 M보내서 아랫 모터 열고닫기
        # actuator.send_command(ser, 'M', 3)
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'fail'})
    finally:
        ser.close()

@app.route('/save_to_excel')
def save_to_excel():
    name = request.args.get('name')
    phone = request.args.get('phone')
    user_id = request.args.get('id')
    oil_amount = request.args.get('amount')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    place = "Unknown"  # Place can be added dynamically if needed

    append_to_excel(name, phone, user_id, time, place, oil_amount, FILE_PATH)
    current_month = datetime.now().month
    total_amount = calculate_total_monthly_amount(user_id, current_month, FILE_PATH)
    return jsonify(totalAmount=total_amount)

@app.route('/fetch_history')
def fetch_history():
    user_id = request.args.get('id')
    month = int(request.args.get('month'))
    try:
        wb = openpyxl.load_workbook(FILE_PATH)
        sheet = wb.active
        history = []
        total_amount = 0
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            record_id, name, phone, oil_amount, place, record_time = row
            record_date = datetime.strptime(record_time, "%Y-%m-%d %H:%M:%S")
            if record_id == user_id and record_date.month == month:
                weekday_str = weekdays[record_date.weekday()]
                formatted_date = record_date.strftime(f"%Y.%m.%d({weekday_str})")
                history.append({
                    "date": formatted_date,
                    "amount": oil_amount
                })
                total_amount += float(oil_amount)

        return jsonify({"history": history, "total": total_amount})
    except FileNotFoundError:
        return jsonify({"history": [], "total": 0})

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
    cur_user = data.get('id')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO log (name, phone, user_id, timestamp) VALUES (?, ?, ?, ?)', (name, phone, cur_user, timestamp))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User data saved.'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)