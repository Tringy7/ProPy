import pandas as pd
import Read as r

def create(df):
    print("Các cột hiện tại trong DataFrame:", df.columns.tolist())
    
    new_record = {}
    try:
        new_record['Country/Region'] = input("Nhập tên quốc gia: ")
        new_record['Confirmed'] = float(input("Nhập số ca xác nhận: "))
        new_record['Deaths'] = float(input("Nhập số ca tử vong: "))
        new_record['Recovered'] = float(input("Nhập số ca phục hồi: "))
        new_record['Active'] = float(input("Nhập số ca phục hồi tích cực: "))
        new_record['New cases'] = float(input("Nhập số trường hợp mới: "))
        new_record['New deaths'] = float(input("Nhập số ca tử vong mới: "))
        new_record['New recovered'] = float(input("Nhập số ca phục hồi mới: "))
        new_record['Confirmed last week'] = float(input("Nhập số ca xác nhận tuần trước: "))
        new_record['WHO Region'] = input("Nhập vùng WHO: ")
        
        # Tính toán cho các biến có công thức
        new_record['Deaths / 100 Cases'] = round((new_record['Deaths'] / new_record['Confirmed']) * 100, 2)
        new_record['Recovered / 100 Cases'] = round((new_record['Recovered'] / new_record['Confirmed']) * 100, 2)
        new_record['Deaths / 100 Recovered'] = round((new_record['Deaths'] / new_record['Recovered']) * 100, 2)
        new_record['1 week change'] = round(new_record['Confirmed'] - new_record['Confirmed last week'], 2)
        new_record['1 week % increase'] = round((new_record['1 week change'] / new_record['Confirmed last week']) * 100, 2)

        # Chuyển đổi new_record thành DataFrame
        new_record_df = pd.DataFrame([new_record])
        
        # Sử dụng pd.concat để thêm bản ghi mới vào DataFrame
        df = pd.concat([df, new_record_df], ignore_index=True)
        
        print("Dữ liệu đã được thêm vào DataFrame thành công!")
        
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
    
    return df

# Khởi tạo một DataFrame trống với các cột tương ứng
df = r.read()

# Ví dụ sử dụng
df = create(df)

# Lưu DataFrame đã cập nhật vào file CSV
df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)
print("Dữ liệu đã được lưu vào file CSV thành công!")
