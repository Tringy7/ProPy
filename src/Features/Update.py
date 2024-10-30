import tkinter as tk
from tkinter import messagebox, ttk
from Features import Read

def update_record(country_name):
    # Tạo cửa sổ nhập dữ liệu
    window = tk.Tk()
    window.title("Cập nhật dữ liệu quốc gia")
    window.geometry("400x600")

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

    # Tạo các ô nhập liệu cho từng trường thông tin
    for field in fields:
        tk.Label(window, text=f"{field}:", font=("Arial", 10)).pack(pady=5)
        
        if field == 'WHO Region':
            region_options = df['WHO Region'].unique()  
            combobox = ttk.Combobox(window, values=region_options)
            combobox.pack()
            entries[field] = combobox
        else:
            entry = tk.Entry(window)
            entry.pack()
            entries[field] = entry

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
    tk.Button(window, text="Cập nhật", command=save_changes, font=("Arial", 12)).pack(pady=20)
    window.mainloop()
