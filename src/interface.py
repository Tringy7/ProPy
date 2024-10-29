import tkinter as tk
from tkinter import messagebox, ttk
from Features import Read
from Features import Create
from Features import Delete
from Features import Update

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Covid")
root.geometry("700x500")
root.iconbitmap("Data/src_img/OIP.ico")

# Tiêu đề
label = tk.Label(root, text="Dataset", font=("Arial", 14))
label.pack(pady=10)

# Frame cho các nút
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Frame cho hiển thị dữ liệu và thanh cuộn
data_frame = tk.Frame(root)
data_frame.pack(expand=True, fill="both", padx=10, pady=10)





# ------------------------------------ View ---------------------------------------------
# Hàm để đọc file CSV và hiển thị trong Treeview
def read_and_display_data():
            # Đọc dữ liệu từ CSV
        df = Read.read()
        
        # Xóa bảng cũ nếu có
        for widget in data_frame.winfo_children():
            widget.destroy()
        
        # Tạo Treeview
        tree = ttk.Treeview(data_frame, columns=list(df.columns), show="headings")
        
        # Đặt tên cho cột
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Thêm dữ liệu vào Treeview
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        
        # Tạo thanh cuộn dọc và ngang
        v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Đặt thanh cuộn vào giao diện
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Điều chỉnh grid layout của data_frame
        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
   




# ------------------------------------ Create ------------------------------------
# Hàm tạo giao diện và lưu bản ghi mới trên trang chính
def add_create_interface():
    # Xóa giao diện cũ nếu đã hiển thị trước đó
    for widget in data_frame.winfo_children():
        widget.destroy()

    # Các biến nhập liệu
    inputs = {}
    labels = ['Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered', 'Confirmed last week', 'WHO Region']
    entries = [] 

    for idx, label_text in enumerate(labels):
        label = tk.Label(data_frame, text=label_text)
        label.grid(row=idx, column=0, padx=(10, 2), pady=5, sticky='w') 

        entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
        entry.grid(row=idx, column=1, padx=(2, 10), pady=5, sticky='ew', columnspan=2)  
        inputs[label_text] = entry
        entries.append(entry)  

        # Gán sự kiện Enter cho mỗi ô nhập liệu
        entry.bind("<Return>", lambda event, idx=idx: entries[min(idx + 1, len(entries) - 1)].focus())

    # Thiết lập tính năng giãn cho cột
    data_frame.grid_columnconfigure(1, weight=1)

    # Hàm lưu dữ liệu mới vào CSV
    def save_new_record():
        try:
            # Biến tạm để lưu giá trị từ các ô nhập liệu
            country = inputs['Country/Region'].get()
            confirmed = float(inputs['Confirmed'].get())
            deaths = float(inputs['Deaths'].get())
            recovered = float(inputs['Recovered'].get())
            active = float(inputs['Active'].get())
            new_cases = float(inputs['New cases'].get())
            new_deaths = float(inputs['New deaths'].get())
            new_recovered = float(inputs['New recovered'].get())
            confirmed_last_week = float(inputs['Confirmed last week'].get())
            who_region = inputs['WHO Region'].get()

            # Gọi hàm Create với các biến tạm
            df = Create.create(country, confirmed, deaths, recovered, active, new_cases, new_deaths, new_recovered, confirmed_last_week, who_region)

            # Hiển thị thông báo thành công
            messagebox.showinfo("Thành công", "Bản ghi đã được thêm vào CSV thành công!")

            # Cập nhật giao diện hiển thị dữ liệu
            read_and_display_data()
            
            # Xóa dữ liệu trong các ô nhập liệu sau khi lưu thành công
            for entry in inputs.values():
                entry.delete(0, tk.END)

        except ValueError as ve:
            messagebox.showerror("Lỗi nhập liệu", f"Giá trị không hợp lệ: {ve}")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")

    # Nút Lưu bản ghi
    save_button = tk.Button(data_frame, text="Add", command=save_new_record)
    save_button.grid(row=len(labels), column=1, pady=20)




# ------------------------------------ Delete ------------------------------------
# Hàm tạo giao diện và xóa bản ghi
def add_delete_interface():
    # Xóa giao diện cũ nếu đã hiển thị trước đó
    for widget in data_frame.winfo_children():
        widget.destroy()

    inputs = {}

    # Nhãn và ô nhập liệu cho tên quốc gia cần xóa
    label = tk.Label(data_frame, text="Nhập tên quốc gia cần xóa:")
    label.grid(row=0, column=0, padx=(10, 2), pady=5, sticky='w') 

    country_entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
    country_entry.grid(row=0, column=1, padx=(2, 10), pady=5, sticky='ew')  
    inputs['Country/Region'] = country_entry

    # Nút Xóa bản ghi
    delete_button = tk.Button(data_frame, text="Delete", command=lambda: delete_country(country_entry.get()))
    delete_button.grid(row=1, column=1, pady=20)

def delete_country(country_to_delete):
    try:
        # Biến tạm để truyền vào hàm delete
        temp_name_delete = country_to_delete

        # Gọi hàm delete trong module Delete
        df = Delete.delete(temp_name_delete)  # Giả sử Delete.delete() trả về DataFrame mới

        # Cập nhật giao diện hiển thị dữ liệu
        read_and_display_data()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# -------------------------------------- Update ---------------------------------------------
# Hàm tạo giao diện và cập nhật bản ghi
def add_update_interface():
    # Xóa giao diện cũ nếu đã hiển thị trước đó
    for widget in data_frame.winfo_children():
        widget.destroy()

    inputs = {}

    # Nhãn và ô nhập liệu cho tên quốc gia cần cập nhật
    label = tk.Label(data_frame, text="Nhập tên quốc gia cần cập nhật:")
    label.grid(row=0, column=0, padx=(10, 2), pady=5, sticky='w') 

    country_entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
    country_entry.grid(row=0, column=1, padx=(2, 10), pady=5, sticky='ew')  
    inputs['Country/Region'] = country_entry

    # Nút Cập nhật bản ghi
    update_button = tk.Button(data_frame, text="Update", command=lambda: update_country(country_entry.get()))
    update_button.grid(row=1, column=1, pady=20)

def update_country(country_to_update):
    try:
        # Biến tạm để truyền vào hàm update
        temp_name_update = country_to_update

        # Gọi hàm update trong module Update
        df = Update.update_record(temp_name_update)  # Giả sử Update.update_record() trả về DataFrame mới

        if df is not None:  # Nếu df không phải None
            # Cập nhật giao diện hiển thị dữ liệu
            read_and_display_data()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")






# --------------------------------------- Quit ------------------------------------------------
# Đóng ứng dụng khi nhấn nút Quit
def quit_app():
    root.destroy()



# ----------------------------------------- Interface ----------------------------------------------
# Tạo các nút với nhãn theo yêu cầu
buttons = ["View", "Create", "Update", "Delete", "Quit", "Desc"]
for i, button_text in enumerate(buttons):
    button = tk.Button(button_frame, text=button_text, width=10)
    button.pack(side=tk.LEFT, padx=5)
    
    # Gán chức năng cho từng nút
    if button_text == "View":
        button.config(command=read_and_display_data)  
    elif button_text == "Create":
        button.config(command=add_create_interface) 
    elif button_text == "Delete":
        button.config(command=add_delete_interface)
    elif button_text == "Update":
        button.config(command=add_update_interface)
    elif button_text == "Quit":
        button.config(command=quit_app)

# Gọi hàm để đọc và hiển thị dữ liệu ngay khi ứng dụng khởi động
read_and_display_data()

# Chạy ứng dụng
root.mainloop()  