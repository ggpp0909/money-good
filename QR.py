import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # 사각형 그리기
        frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2
        rect_width, rect_height = 200, 200  # 사각형의 크기 설정
        x, y = frame_center_x - rect_width // 2, frame_center_y - rect_height // 2
        thickness = 2
        # cv2.rectangle(frame, (x, y), (x + rect_width, y + rect_height), (0, 255, 0), thickness)

        # 초록색 사각형 모서리 부분 제외하고 안쪽을 투명하게 만들기
        mask = np.zeros_like(frame, dtype=np.uint8)
        cv2.rectangle(mask, (x + thickness, y + thickness), (x + rect_width - thickness, y + rect_height - thickness), (255, 255, 255), -1)
        alpha = 0.35
        frame = cv2.addWeighted(mask, alpha, frame, 1 - alpha, 0)

        # 텍스트 표시
        text = "READ QR-CODE"
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


read_qr_code()
