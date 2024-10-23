import pandas as pd
import Read as r

def delete(df):
    print("Các cột hiện tại trong DataFrame:", df.columns.tolist())
    
    country_to_delete = input("Nhập tên quốc gia cần xóa: ")
    
    # Kiểm tra xem quốc gia có tồn tại trong DataFrame không
    if country_to_delete in df['Country/Region'].values:
        # Xóa bản ghi tương ứng
        df = df[df['Country/Region'] != country_to_delete]
        print(f"Bản ghi của quốc gia '{country_to_delete}' đã được xóa thành công!")
    else:
        print(f"Quốc gia '{country_to_delete}' không tồn tại trong DataFrame.")
    
    return df

# Khởi tạo một DataFrame từ file CSV
df = r.read()

# Gọi hàm delete
df = delete(df)  # Cần gán lại df sau khi xóa

# Lưu DataFrame đã cập nhật vào file CSV
df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)
print("Dữ liệu đã được lưu vào file CSV thành công!")
