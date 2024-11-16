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
    # Hàm đọc và hiển thị dữ liệu
    def read_and_display_data():
        # Làm sạch và chuẩn hóa dữ liệu
        Datacleaner.CleanUp()
        DataNormalizer.normalize()

        df = Read.read()  # Đảm bảo rằng hàm này đã tồn tại và trả về một DataFrame

        # Xóa bảng cũ nếu có
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Khung chứa Treeview và thanh cuộn
        tree_frame = tk.Frame(data_frame)
        tree_frame.pack(expand=True, fill="both")

        # Tạo Treeview
        global tree
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




    
    # ---------------------------------- Search -------------------------------------
    def add_search_interface():
    # Xóa giao diện cũ nếu đã hiển thị trước đó
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Khung tìm kiếm
        search_label = tk.Label(data_frame, text="Tìm kiếm quốc gia:")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        search_entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
        search_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Khung hiển thị danh sách gợi ý
        suggestion_listbox = tk.Listbox(data_frame, height=10, font=("Arial", 10))
        suggestion_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

        # Tạo scrollbar cho Listbox
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=suggestion_listbox.yview)
        suggestion_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=5)

        data_frame.grid_columnconfigure(1, weight=1)

        def filter_suggestions(event):
            # Lấy danh sách quốc gia từ dữ liệu
            df = Read.read()
            country_list = df["Country/Region"].dropna().tolist()

            # Lấy chuỗi nhập liệu
            query = search_entry.get().strip().lower()

            # Lọc gợi ý
            filtered_countries = [country for country in country_list if query in country.lower()]

            # Xóa danh sách cũ
            suggestion_listbox.delete(0, tk.END)

            # Cập nhật danh sách mới
            for country in filtered_countries:
                suggestion_listbox.insert(tk.END, country)

        # Liên kết sự kiện nhập liệu
        search_entry.bind("<KeyRelease>", filter_suggestions)

        def display_country_data(selected_country):
            # Lấy dữ liệu quốc gia từ `Read.read`
            df = Read.read()

            # Lọc dữ liệu theo quốc gia
            filtered_data = df[df["Country/Region"] == selected_country]

            # Xóa bảng cũ nếu có
            for widget in data_frame.winfo_children():
                widget.destroy()

            # Hiển thị dữ liệu quốc gia
            tree_frame = tk.Frame(data_frame)
            tree_frame.pack(expand=True, fill="both")

            # Tạo Treeview
            tree = ttk.Treeview(tree_frame, columns=list(filtered_data.columns), show="headings", style="Custom.Treeview")
            tree.grid(row=0, column=0, sticky="nsew")

            for col in filtered_data.columns:
                tree.heading(col, text=col, anchor="center")
                tree.column(col, anchor="center", minwidth=120, width=150, stretch=True)

            for _, row in filtered_data.iterrows():
                tree.insert("", "end", values=list(row))

            # Tạo thanh cuộn dọc và ngang
            v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)

        def select_suggestion(event=None):
            try:
                selected_country = suggestion_listbox.get(suggestion_listbox.curselection())
                display_country_data(selected_country)
            except tk.TclError:
                messagebox.showinfo("Thông báo", "Chưa chọn quốc gia nào!")

        def navigate_suggestions(event):
            current_selection = suggestion_listbox.curselection()
            suggestion_listbox.focus_set()  # Đảm bảo Listbox nhận focus

            if event.keysym == "Down":
                if not current_selection:
                    suggestion_listbox.selection_set(0)
                    suggestion_listbox.activate(0)
                else:
                    next_index = (current_selection[0] + 1) % suggestion_listbox.size()
                    suggestion_listbox.selection_clear(0, tk.END)
                    suggestion_listbox.selection_set(next_index)
                    suggestion_listbox.activate(next_index)
                return "break"  # Ngăn chặn hành vi mặc định

            elif event.keysym == "Up":
                if not current_selection:
                    suggestion_listbox.selection_set(suggestion_listbox.size() - 1)
                    suggestion_listbox.activate(suggestion_listbox.size() - 1)
                else:
                    prev_index = (current_selection[0] - 1) % suggestion_listbox.size()
                    suggestion_listbox.selection_clear(0, tk.END)
                    suggestion_listbox.selection_set(prev_index)
                    suggestion_listbox.activate(prev_index)
                return "break"  # Ngăn chặn hành vi mặc định


        # Liên kết sự kiện cho Entry
        search_entry.bind("<Return>", lambda event: suggestion_listbox.focus_set())  # Chuyển focus đến Listbox khi nhấn Enter
        search_entry.bind("<Down>", navigate_suggestions)  # Điều hướng xuống Listbox
        search_entry.bind("<Up>", navigate_suggestions)  # Điều hướng lên Listbox

        # Liên kết sự kiện cho Listbox
        suggestion_listbox.bind("<Return>", lambda event: select_suggestion())
        suggestion_listbox.bind("<Up>", navigate_suggestions)
        suggestion_listbox.bind("<Down>", navigate_suggestions)





    # ---------------------------------- Sort ----------------------------------------
    def sort():
        # Đọc dữ liệu từ file hoặc nguồn
        df = Read.read()

        # Cột để sắp xếp
        column_names = [
            "Country/Region", "Confirmed", "Deaths", "Recovered", "Active", "New cases", 
            "New deaths", "New recovered", "Deaths / 100 Cases", "Recovered / 100 Cases", 
            "Deaths / 100 Recovered", "Confirmed last week", "1 week change", 
            "1 week % increase", "WHO Region"
        ]
        
        # Hàm callback khi chọn cột để sắp xếp
        def on_column_select():
            column_name = column_combo.get()
            if column_name in column_names:
                # Sắp xếp dữ liệu theo cột được chọn
                sorted_df = df.sort_values(by=column_name, ascending=True)
                # Hiển thị dữ liệu đã sắp xếp
                display_sorted_data(sorted_df)
                sort_window.destroy()

        # Tạo cửa sổ con để chọn cột
        sort_window = tk.Toplevel(root)
        sort_window.title("Chọn cột để sắp xếp")

        # Label hướng dẫn
        label = tk.Label(sort_window, text="Chọn cột để sắp xếp:")
        label.pack(padx=10, pady=10)

        # ComboBox để chọn cột
        column_combo = ttk.Combobox(sort_window, values=column_names, width=30)
        column_combo.pack(padx=10, pady=10)

        # Nút xác nhận để sắp xếp
        sort_button = tk.Button(sort_window, text="Sắp xếp", command=on_column_select)
        sort_button.pack(padx=10, pady=10)

        # Hàm để hiển thị dữ liệu đã sắp xếp trong Treeview
        def display_sorted_data(sorted_df):
            for row in tree.get_children():
                tree.delete(row)  # Xóa tất cả các dòng cũ trong Treeview

            # Thêm dữ liệu đã sắp xếp vào Treeview
            for _, row in sorted_df.iterrows():
                tree.insert("", "end", values=list(row))



                
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
                    country = inputs['Country/Region'].get().strip().title()
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

                    df = Read.read()


                    if country in df['Country/Region'].values:
                        messagebox.showinfo(None,"Đã thêm thành công")
                    else:
                        messagebox.showerror('Lỗi', 'Giá trị nhập không hợp lệ. Không lưu được')


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
    # Các nút trong thanh điều hướng
    buttons = {
        "View": read_and_display_data,
        "Search": add_search_interface,
        "Sort": sort, 
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