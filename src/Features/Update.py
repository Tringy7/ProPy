import pandas as pd
from tkinter import Tk, Label, Entry, Button, messagebox

def update_record(country_name):
    # Tạo cửa sổ nhập dữ liệu
    window = Tk()
    window.title("Cập nhật dữ liệu quốc gia")
    window.geometry("400x600")

    # Đọc dữ liệu từ file CSV
    try:
        df = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")
        window.destroy()
        return

    # Kiểm tra xem quốc gia có tồn tại trong dữ liệu hay không
    if country_name not in df['Country/Region'].values:
        messagebox.showerror("Lỗi", f"Quốc gia '{country_name}' không tồn tại trong dữ liệu.")
        window.destroy()
        return

    # Lấy chỉ số của quốc gia cần cập nhật
    index = df[df['Country/Region'] == country_name].index[0]

    # Các trường thông tin cần cập nhật
    fields = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Cases', 
              'New Deaths', 'New Recovered', 'Confirmed last week', 'WHO Region']
    entries = {}

    # Tạo các ô nhập liệu cho từng trường thông tin
    for field in fields:
        Label(window, text=f"{field}:", font=("Arial", 10)).pack(pady=5)
        entry = Entry(window)
        entry.pack()
        entries[field] = entry

    # Hàm xử lý khi nhấn nút "Cập nhật"
    def save_changes():
        # Cập nhật các giá trị mới từ các ô nhập liệu
        for field in fields:
            new_value = entries[field].get()
            if new_value:
                if field in ['Confirmed', 'Deaths', 'Recovered', 'Active', 'Cases', 
                             'New Deaths', 'New Recovered', 'Confirmed last week']:
                    df.at[index, field] = int(new_value)
                else:
                    df.at[index, field] = new_value

        # Tính toán lại các giá trị dựa trên các công thức
        confirmed = df.at[index, 'Confirmed']
        deaths = df.at[index, 'Deaths']
        recovered = df.at[index, 'Recovered']
        confirmed_last_week = df.at[index, 'Confirmed last week']

        # Các công thức tính toán lại giá trị
        if confirmed and confirmed > 0:
            df.at[index, 'Deaths / 100 Cases'] = round((deaths / confirmed) * 100, 2) if deaths else 0
            df.at[index, 'Recovered / 100 Cases'] = round((recovered / confirmed) * 100, 2) if recovered else 0
        if recovered and recovered > 0:
            df.at[index, 'Deaths / 100 Recovered'] = round((deaths / recovered) * 100, 2) if deaths else 0
        if confirmed_last_week and confirmed_last_week > 0:
            df.at[index, '1 week change'] = round(confirmed - confirmed_last_week, 2)
            df.at[index, '1 week % increase'] = round(((confirmed - confirmed_last_week) / confirmed_last_week) * 100, 2)

        # Lưu DataFrame đã cập nhật vào file CSV
        df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)
        messagebox.showinfo("Thành công", f"Dữ liệu của quốc gia '{country_name}' đã được cập nhật thành công!")
        window.destroy()

    # Nút cập nhật
    Button(window, text="Cập nhật", command=save_changes, font=("Arial", 12)).pack(pady=20)
    window.mainloop()
