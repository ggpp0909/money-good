'''
Customer ID
Time 
Place (Device number)
Oil quantity
'''
import openpyxl

def append_to_excel(customer_ID, time, place, oil_quantity, file_path):
    # 엑셀 파일 열기 (없으면 새로 생성)
    try:
        wb = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    sheet = wb.active

    # 헤더 추가 (파일이 새로 생성되는 경우에만 추가)
    if sheet.max_row == 1:
        sheet.append(["Customer ID", "Time", "Place", "Oil Quantity"])

    # 정보 추가
    sheet.append([customer_ID, time, place, oil_quantity])

    # 엑셀 파일 저장
    wb.save(file_path)
    print(f"Record appended successfully to {file_path}!")

# 예시 정보
customer_ID = "testid"
time = "testtime"
place = "testplace"
oil_quantity = "testquantity"

# 저장할 경로와 파일명
file_path = "C:/Users/ggpp0/Documents/record.xlsx"

# 엑셀에 정보 추가
append_to_excel(customer_ID, time, place, oil_quantity, file_path)
