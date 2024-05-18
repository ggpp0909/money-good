import QR
import json
import excel

def main():
    # 1. QR code read
    data = QR.read_qr_code()
    data = json.loads(data)
    
    if not data.get("ID"):
        print("비회원 입니다")
        return 1
     
    ID = data["ID"]

    # 2. 아두이노에게 명령 전송
    

if __name__ == "__main__":
    main()
