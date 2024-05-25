import qrcode
import json

# 예제 JSON 데이터
data = {
    "name": "yeong nam",
    "phone": "+1234567890",
    "id" : "1234"
}

# JSON 데이터를 문자열로 변환
json_data = json.dumps(data)

# QR 코드 생성
qr = qrcode.QRCode(
    version=1,  # 1부터 40까지 선택, 숫자가 클수록 크고 복잡한 QR 코드
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # 오류 수정 수준
    box_size=10,  # 각 박스의 크기
    border=4,  # 경계 여백 크기
)

# JSON 데이터를 QR 코드에 추가
qr.add_data(json_data)
qr.make(fit=True)

# QR 코드 이미지를 생성하고 저장
img = qr.make_image(fill='black', back_color='white')
img.save('qrcode.png')

print("QR 코드가 'qrcode.png' 파일로 저장되었습니다.")