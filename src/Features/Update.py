import pandas as pd
from tkinter import messagebox

def update_record(country_to_update):
    # Đọc dữ liệu từ file CSV
    try:
        df = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")  # Đọc file CSV

        print("Các cột hiện tại trong DataFrame:", df.columns.tolist())
        
        # Kiểm tra xem quốc gia có tồn tại trong DataFrame không
        if country_to_update in df['Country/Region'].values:
            # Lấy chỉ số của quốc gia cần cập nhật
            index = df[df['Country/Region'] == country_to_update].index[0]

            # Thay đổi các giá trị mới
            change_confirmed = input("Thay đổi số ca Confirmed (hoặc nhấn Enter để giữ nguyên): ")
            change_deaths = input("Thay đổi số ca Deaths (hoặc nhấn Enter để giữ nguyên): ")
            change_recovered = input("Thay đổi số ca Recovered (hoặc nhấn Enter để giữ nguyên): ")
            change_active = input("Thay đổi số ca Active (hoặc nhấn Enter để giữ nguyên): ")
            change_cases = input("Thay đổi số Cases (hoặc nhấn Enter để giữ nguyên): ")
            change_new_deaths = input("Thay đổi số ca New Deaths (hoặc nhấn Enter để giữ nguyên): ")
            change_new_recovered = input("Thay đổi số ca New Recovered (hoặc nhấn Enter để giữ nguyên): ")
            change_confirmed_lw = input("Thay đổi số ca Confirmed last week (hoặc nhấn Enter để giữ nguyên): ")
            change_WHO_region = input("Thay đổi WHO Region (hoặc nhấn Enter để giữ nguyên): ")

            # Cập nhật các giá trị mới, nếu có
            if change_confirmed: 
                df.at[index, 'Confirmed'] = int(change_confirmed)
            if change_deaths:
                df.at[index, 'Deaths'] = int(change_deaths)
            if change_recovered:
                df.at[index, 'Recovered'] = int(change_recovered)
            if change_confirmed_lw:
                df.at[index, 'Confirmed last week'] = int(change_confirmed_lw)
            if change_active:
                df.at[index, 'Active'] = int(change_active)
            if change_cases:
                df.at[index, 'Cases'] = int(change_cases)
            if change_new_deaths:
                df.at[index, 'New Deaths'] = int(change_new_deaths)
            if change_new_recovered:
                df.at[index, 'New Recovered'] = int(change_new_recovered)
            if change_WHO_region:
                df.at[index, 'WHO Region'] = change_WHO_region

            # Tính toán lại các giá trị dựa trên các công thức được yêu cầu
            confirmed = df.at[index, 'Confirmed']
            deaths = df.at[index, 'Deaths']
            recovered = df.at[index, 'Recovered']
            confirmed_last_week = df.at[index, 'Confirmed last week']

            # Chỉ tính toán nếu các giá trị đã tồn tại và hợp lệ
            if confirmed and confirmed > 0:
                df.at[index, 'Deaths / 100 Cases'] = round((deaths / confirmed) * 100, 2) if deaths else 0
                df.at[index, 'Recovered / 100 Cases'] = round((recovered / confirmed) * 100, 2) if recovered else 0
            if recovered and recovered > 0:
                df.at[index, 'Deaths / 100 Recovered'] = round((deaths / recovered) * 100, 2) if deaths else 0
            if confirmed_last_week and confirmed_last_week > 0:
                df.at[index, '1 week change'] = round(confirmed - confirmed_last_week, 2)
                df.at[index, '1 week % increase'] = round(((confirmed - confirmed_last_week) / confirmed_last_week) * 100, 2)

            # Lưu DataFrame đã cập nhật vào file CSV
            df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)  # Ghi đè vào file CSV
            messagebox.showinfo("Thành công", f"Dữ liệu của quốc gia '{country_to_update}' đã được cập nhật thành công!")
            return df  # Trả về DataFrame đã được cập nhật
        else:
            messagebox.showerror("Lỗi", f"Quốc gia '{country_to_update}' không tồn tại trong DataFrame.")
            return None  # Trả về None nếu không tìm thấy

    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")
        return None  # Trả về None nếu không tìm thấy file
