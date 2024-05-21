from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr_reader')
def qr_reader():
    return render_template('qr_reader.html')

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