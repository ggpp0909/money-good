import cv2
from pyzbar.pyzbar import decode

def read_qr_code():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return
    
    try:
        while True:
            ret, frame = cap.read()

            # 텍스트 표시
            text = "READ QR-CODE"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            frame_width = frame.shape[1]
            text_x = frame_width // 2 - text_size[0] // 2
            text_y = 40  # 화면 상단 중앙에 텍스트 위치 설정
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("QR Code Reader", frame)

            decoded_objects = decode(frame)
            # print(decoded_objects)
            for obj in decoded_objects:
                # QR 코드 데이터 출력
                # print(f"QR 코드 데이터: {obj.data.decode('utf-8')}")
                cap.release()
                cv2.destroyAllWindows()
                return obj.data.decode('utf-8')

            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
