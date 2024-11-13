from tkinter import messagebox
from Features import Read

def delete(temp_name_delete):
    try:
        df = Read.read() 

        country_to_delete = temp_name_delete.strip().title()

        if country_to_delete in df['Country/Region'].values:
            # Xóa bản ghi tương ứng
            df = df[df['Country/Region'] != country_to_delete]
            df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False) 

            messagebox.showinfo("Thành công", f"Bản ghi của quốc gia '{country_to_delete}' đã được xóa thành công!")
        else:
            messagebox.showerror("Lỗi", f"Quốc gia '{country_to_delete}' không tồn tại trong DataFrame.")

        return df 

    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")
        return None
