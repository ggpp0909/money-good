from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oil_collector.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# # 데이터베이스 초기화
# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr_reader')
def qr_reader():
    return render_template('qr_reader.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/dispose_oil')
def dispose_oil():
    # 처리 로직을 여기에 추가하세요.
    return "폐식용유 버리기 페이지"

@app.route('/view_records')
def view_records():
    # 처리 로직을 여기에 추가하세요.
    return "수거내역 확인하기 페이지"

@app.route('/process_qr', methods=['POST'])
def process_qr():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # 예시: JSON 데이터 처리
    name = data.get("name")
    phone = data.get("phone")
    user_id = data.get("ID")

    # 여기서 필요한 작업을 수행하세요. 예: 데이터베이스에 저장, 기타 작업 등
    print(f"Name: {name}, Phone: {phone}, ID: {user_id}")

    # 응답
    return jsonify({"message": "Data processed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)