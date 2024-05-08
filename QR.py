import cv2
from pyzbar.pyzbar import decode

def read_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # 화면 중앙에 사각형 그리기
        frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2
        rect_width, rect_height = 200, 200  # 사각형의 크기 설정
        x, y = frame_center_x - rect_width // 2, frame_center_y - rect_height // 2
        cv2.rectangle(frame, (x, y), (x + rect_width, y + rect_height), (0, 255, 0), 2)

        # 사각형 위에 텍스트 표시
        text = "READ QR-code"
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        text_x = frame_center_x - text_size[0] // 2
        text_y = y - 20  # 사각형 위에 텍스트 위치 설정
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # QR 코드 데이터 출력
            print(f"QR 코드 데이터: {obj.data.decode('utf-8')}")

        cv2.imshow("QR Code Reader", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_code()
