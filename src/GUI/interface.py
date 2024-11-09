import tkinter as tk
from tkinter import messagebox, ttk, Button, Frame 
from Features import Read, Create, Delete, Chart, Update
from Data_cleaning_normalization import Datacleaner, DataNormalizer

def run_interface():
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Covid Dashboard")
    root.geometry("1200x700")
    root.config(bg="#E8F5E9")
    root.iconbitmap("Data/src_img/OIP.ico")
    
    # Khung cho thanh điều hướng
    nav_frame = tk.Frame(root, bg="#2E7D32", width=200)
    nav_frame.pack(side="left", fill="y")

    # Khung cho dữ liệu
    data_frame = tk.Frame(root, bg="white")
    data_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    label = tk.Label(nav_frame, text="Covid Dashboard", font=("Arial", 16, "bold"), bg="#2E7D32", fg="white")
    label.pack(pady=20)





    # ------------------------------------ View ------------------------------------
    def read_and_display_data():
        # # Làm sạch và chuẩn hóa
        Datacleaner.CleanUp()
        DataNormalizer.normalize()

        df = Read.read()  # Đảm bảo rằng hàm này đã tồn tại và trả về một DataFrame

        # Xóa bảng cũ nếu có
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Khung cho Treeview và thanh cuộn
        tree_frame = tk.Frame(data_frame)
        tree_frame.pack(expand=True, fill="both")

        # Tạo Treeview
        tree = ttk.Treeview(tree_frame, columns=list(df.columns), show="headings", style="Custom.Treeview")
        tree.grid(row=0, column=0, sticky="nsew")

        # Đặt tên và kích thước cho cột
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", minwidth=120, width=150, stretch=True)

        # Thêm dữ liệu vào Treeview
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        # Tạo thanh cuộn dọc và ngang
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Đặt thanh cuộn dọc và ngang
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Cấu hình khung chứa để thay đổi kích thước đúng cách
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    



    # ------------------------------------ Create ------------------------------------
    def add_create_interface():
        # Xóa giao diện cũ nếu đã hiển thị trước đó
        for widget in data_frame.winfo_children():
            widget.destroy()

        inputs = {}
        labels = ['Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered', 'Confirmed last week', 'WHO Region']
        entries = []

        df = Read.read()
        who_region_options = df['WHO Region'].dropna().unique().tolist()

        def on_enter_key(event, idx):
            if idx < len(entries) - 1:
                entries[idx + 1].focus_set()
            else:
                save_new_record()

        def on_up_down_key(event, idx):
            if event.keysym == "Up" and idx > 0:
                entries[idx - 1].focus_set()
            elif event.keysym == "Down" and idx < len(entries) - 1:
                entries[idx + 1].focus_set()

        # Gộp chú thích và đưa lên đầu trang
        note_font = ("Arial", 8, "italic")  # Font nhạt và in nghiêng
        combined_note = "Confirmed lớn hơn Deaths, Recovered, Active và New cases lớn hơn New deaths, New recovered"
        
        # Đặt chú thích lên đầu trang (row=0, columnspan=3)
        note_label = tk.Label(data_frame, text=combined_note, font=note_font, fg="gray", wraplength=600)
        note_label.grid(row=0, column=0, columnspan=3, pady=(5, 2), sticky='w')

        # Các mục nhập dữ liệu bắt đầu từ hàng 1 để tránh bị che khuất bởi chú thích
        for idx, label_text in enumerate(labels):
            label = tk.Label(data_frame, text=label_text)
            label.grid(row=idx + 1, column=0, padx=(10, 2), pady=5, sticky='w')

            if label_text == 'WHO Region':
                selected_region = tk.StringVar(value="")
                combobox = ttk.Combobox(data_frame, textvariable=selected_region, values=who_region_options, state="readonly", font=("Arial", 10))
                combobox.grid(row=idx + 1, column=1, padx=(2, 10), pady=5, sticky='ew', columnspan=2)
                inputs[label_text] = selected_region
                entries.append(combobox)

                combobox.bind("<Return>", lambda event, idx=idx: on_enter_key(event, idx))
                combobox.bind("<Up>", lambda event, idx=idx: on_up_down_key(event, idx))
                combobox.bind("<Down>", lambda event, idx=idx: on_up_down_key(event, idx))
            else:
                entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
                entry.grid(row=idx + 1, column=1, padx=(2, 10), pady=5, sticky='ew', columnspan=2)
                inputs[label_text] = entry
                entries.append(entry)

                entry.bind("<Return>", lambda event, idx=idx: on_enter_key(event, idx))
                entry.bind("<Up>", lambda event, idx=idx: on_up_down_key(event, idx))
                entry.bind("<Down>", lambda event, idx=idx: on_up_down_key(event, idx))

        data_frame.grid_columnconfigure(1, weight=1)

        # Lưu bản ghi
        def save_new_record():
            # Xác nhận lưu bản ghi với hộp thoại
            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn ghi bản ghi này không?"):
                try:
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

                    Create.create(country, confirmed, deaths, recovered, active, new_cases, new_deaths, new_recovered, confirmed_last_week, who_region)

                    # messagebox.showinfo("Thành công", "Bản ghi đã được thêm vào CSV thành công!")
                    read_and_display_data()

                    for key, widget in inputs.items():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, tk.END)
                        elif isinstance(widget, tk.StringVar):
                            widget.set("")

                except ValueError as ve:
                    messagebox.showerror("Lỗi nhập liệu", f"Giá trị không hợp lệ: {ve}")
                except FileNotFoundError:
                    messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")

        # Đẩy nút Add xuống 1 hàng
        save_button = tk.Button(data_frame, text="Add", command=save_new_record, font=("Arial", 10, "bold"))
        save_button.grid(row=len(labels) + 1, column=1, pady=20)  # Thêm hàng xuống dưới cùng của form nhập liệu
        save_button.bind("<Return>", lambda event: save_new_record())






    # ------------------------------------ Delete ------------------------------------
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

        # Ràng buộc sự kiện Enter để thực hiện việc xóa khi nhấn Enter
        country_entry.bind("<Return>", lambda event: confirm_delete(country_entry.get()))

        # Nút Xóa bản ghi
        delete_button = tk.Button(data_frame, text="Delete", command=lambda: confirm_delete(country_entry.get()))
        delete_button.grid(row=1, column=1, pady=20)

    def confirm_delete(country_to_delete):
        # Hộp thoại xác nhận
        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa quốc gia '{country_to_delete}'?")
        if confirm:
            try:
                # Gọi hàm delete trong module Delete
                df = Delete.delete(country_to_delete)
                read_and_display_data()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")





    # -------------------------------------- Update ----------------------------------
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

        # Ràng buộc sự kiện Enter để thực hiện việc cập nhật khi nhấn Enter
        country_entry.bind("<Return>", lambda event: update_country(country_entry.get()))

        # Nút Cập nhật bản ghi
        update_button = tk.Button(data_frame, text="Update", command=lambda: update_country(country_entry.get()))
        update_button.grid(row=1, column=1, pady=20)

    def update_country(country_to_update):
        try:
            # Biến tạm để truyền vào hàm update
            temp_name_update = country_to_update

            # Gọi hàm update trong module Update
            df = Update.update_record(temp_name_update)

            if df is not None:  # Nếu df không phải None
                # Cập nhật giao diện hiển thị dữ liệu
                read_and_display_data()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")





    # --------------------------------------- Chart -----------------------------------
    def add_chart_interface():
        for widget in data_frame.winfo_children():
            widget.destroy()

        label = tk.Label(data_frame, text="Select chart type to view:")
        label.grid(row=0, column=0, padx=(10, 2), pady=1, sticky='w') 

        # Tạo nút
        button_frame = Frame(data_frame) 
        button_frame.grid(row=0, column=1, pady=10)


        # Tạo các nút chức năng
        piechart_button = Button(button_frame, text='Pie Chart', command=lambda: Chart.country_selection(), relief=tk.RAISED)
        piechart_button.pack(side='left', padx=10)

        confirmed_button = Button(button_frame, text='Total Confirmed', command=lambda: Chart.show_plot("Confirmed"), relief=tk.RAISED)
        confirmed_button.pack(side='left', padx=10)

        deaths_button = Button(button_frame, text='Total Deaths', command=lambda: Chart.show_plot("Deaths"), relief=tk.RAISED)
        deaths_button.pack(side='left', padx=5)

        recovered_button = Button(button_frame, text='Total Recovered', command=lambda: Chart.show_plot("Recovered"), relief=tk.RAISED)
        recovered_button.pack(side='left', padx=5)

    



    # --------------------------------------- Quit ------------------------------------
    def quit_app():
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát không?"):
            root.destroy()





    # --------------------------------------Interface ---------------------------------
    # Tạo các nút với nhãn theo yêu cầu
    # Thêm các nút trong thanh điều hướng
    buttons = {
        "View": read_and_display_data,
        "Create": add_create_interface,
        "Update": add_update_interface,
        "Delete": add_delete_interface,
        "Chart": add_chart_interface,
        "Quit": quit_app
    }

    for text, command in buttons.items():
        button = tk.Button(
            nav_frame,
            text=text,
            command=command,
            font=("Arial", 12),
            bg="#43A047",
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=10
        )
        button.pack(fill="x", padx=10, pady=5)

    # Tùy chỉnh giao diện Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"), foreground="#2E7D32")
    style.configure("Custom.Treeview", rowheight=30, fieldbackground="#E8F5E9")
    style.map("Custom.Treeview", background=[("selected", "#A5D6A7")], foreground=[("selected", "black")])

    # Chạy hiển thị dữ liệu ban đầu
    read_and_display_data()
    root.mainloop()