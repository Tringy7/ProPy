import pandas as pd
from tkinter import messagebox
import Read


def delete(temp_name_delete):
    try:
        df = Read.read()  # Đọc file CSV

        country_to_delete = temp_name_delete

        if country_to_delete in df['Country/Region'].values:
            # Xóa bản ghi tương ứng
            df = df[df['Country/Region'] != country_to_delete]
            df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)  # Ghi đè vào file CSV

            messagebox.showinfo("Thành công", f"Bản ghi của quốc gia '{country_to_delete}' đã được xóa thành công!")
        else:
            messagebox.showerror("Lỗi", f"Quốc gia '{country_to_delete}' không tồn tại trong DataFrame.")

        return df  # Trả về DataFrame đã được cập nhật

    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")
        return None  # Trả về None nếu không tìm thấy file
