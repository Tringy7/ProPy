import tkinter as tk
from tkinter import messagebox, ttk
from Features import Read

def update_record(country_name):
    # Tạo cửa sổ cập nhật dữ liệu với kích thước lớn và phong cách tương tự giao diện chính
    window = tk.Tk()
    window.title("Cập nhật dữ liệu quốc gia")
    window.geometry("600x700")
    window.config(bg="#E8F5E9")  # Màu nền giống với cửa sổ chính

    try:
        df = Read.read()
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")
        window.destroy()
        return

    # Kiểm tra xem quốc gia có tồn tại trong dữ liệu hay không
    if country_name not in df['Country/Region'].values:
        messagebox.showerror("Lỗi", f"Quốc gia '{country_name}' không tồn tại trong dữ liệu.")
        window.destroy()
        return

    index = df[df['Country/Region'] == country_name].index[0]

    # Thông tin cần cập nhật
    fields = ['Confirmed', 'Deaths', 'Recovered', 'Active', 
              'New cases', 'New deaths', 'New recovered', 
              'Confirmed last week', 'WHO Region']
    entries = {}

    # Tiêu đề
    tk.Label(window, text=f"Cập nhật dữ liệu cho '{country_name}'", font=("Arial", 16, "bold"), bg="#E8F5E9").pack(pady=10)

    # Tạo các ô nhập liệu cho từng trường thông tin
    for idx, field in enumerate(fields):
        tk.Label(window, text=f"{field}:", font=("Arial", 10), bg="#E8F5E9").pack(pady=5)

        if field == 'WHO Region':
            region_options = [region.replace("'", "") for region in df['WHO Region'].unique()]  # Loại bỏ dấu nháy trong WHO Region
            combobox = ttk.Combobox(window, values=region_options, font=("Arial", 10))
            combobox.pack(fill="x", padx=10)
            entries[field] = combobox

            # Ràng buộc phím Enter, Up, và Down để chuyển đến ô tiếp theo hoặc lưu thay đổi
            combobox.bind("<Return>", lambda event, idx=idx: focus_next(idx))
            combobox.bind("<Down>", lambda event, idx=idx: focus_next(idx))
            combobox.bind("<Up>", lambda event, idx=idx: focus_previous(idx))
        else:
            entry = tk.Entry(window, font=("Arial", 10))
            entry.pack(fill="x", padx=10)
            entries[field] = entry

            # Ràng buộc phím Enter, Up, và Down để chuyển đến ô tiếp theo hoặc lưu thay đổi
            entry.bind("<Return>", lambda event, idx=idx: focus_next(idx))
            entry.bind("<Down>", lambda event, idx=idx: focus_next(idx))
            entry.bind("<Up>", lambda event, idx=idx: focus_previous(idx))

    # Hàm chuyển đến ô nhập liệu tiếp theo
    def focus_next(idx):
        if idx + 1 < len(fields):
            next_widget = entries[fields[idx + 1]]
            next_widget.focus_set()
        else:
            save_changes()  # Thực hiện cập nhật khi nhấn Enter ở ô cuối cùng

    # Hàm chuyển đến ô nhập liệu trước đó
    def focus_previous(idx):
        if idx > 0:
            previous_widget = entries[fields[idx - 1]]
            previous_widget.focus_set()

    # Hàm xử lý khi nhấn nút "Cập nhật"
    def save_changes():
        for field in fields:
            new_value = entries[field].get()
            if new_value:
                if field in ['Confirmed', 'Deaths', 'Recovered', 'Active', 
                             'New cases', 'New deaths', 'New recovered', 
                             'Confirmed last week']:
                    df.at[index, field] = int(new_value)
                else:
                    df.at[index, field] = new_value

        # Cập nhật các chỉ số tính toán
        confirmed = df.at[index, 'Confirmed']
        deaths = df.at[index, 'Deaths']
        recovered = df.at[index, 'Recovered']
        confirmed_last_week = df.at[index, 'Confirmed last week']

        if confirmed and confirmed > 0:
            df.at[index, 'Deaths / 100 Cases'] = round((deaths / confirmed) * 100, 2) if deaths else 0
            df.at[index, 'Recovered / 100 Cases'] = round((recovered / confirmed) * 100, 2) if recovered else 0
        if recovered and recovered > 0:
            df.at[index, 'Deaths / 100 Recovered'] = round((deaths / recovered) * 100, 2) if deaths else 0
        if confirmed_last_week and confirmed_last_week > 0:
            df.at[index, '1 week change'] = round(confirmed - confirmed_last_week, 2)
            df.at[index, '1 week % increase'] = round(((confirmed - confirmed_last_week) / confirmed_last_week) * 100, 2)

        # Lưu
        df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)
        messagebox.showinfo("Thành công", f"Dữ liệu của quốc gia '{country_name}' đã được cập nhật thành công!")
        window.destroy()

    # Nút cập nhật
    update_button = tk.Button(window, text="Cập nhật", command=save_changes, font=("Arial", 12, "bold"), bg="#2E7D32", fg="white")
    update_button.pack(pady=20, padx=10, fill="x")
    
    # Cho phép nhấn Enter tại nút cập nhật để thực hiện cập nhật
    update_button.bind("<Return>", lambda event: save_changes())

    window.mainloop()
