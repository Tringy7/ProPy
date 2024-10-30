import tkinter as tk
from tkinter import messagebox, ttk, Button, Frame 
from Features import Read
from Features import Create
from Features import Delete
from Features import Update
from Features import Chart
from Data_cleaning_normalization import Datacleaner
from Data_cleaning_normalization import DataNormalizer

def run_interface():
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Covid")
    root.geometry("700x500")
    root.iconbitmap("Data/src_img/OIP.ico")
    
    label = tk.Label(root, text="Dataset", font=("Arial", 14))
    label.pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    data_frame = tk.Frame(root)
    data_frame.pack(expand=True, fill="both", padx=10, pady=10)





    # ------------------------------------ View ---------------------------------------------
    def read_and_display_data():
            # Làm sạch và chuẩn hóa 
            Datacleaner.CleanUp()
            DataNormalizer.normalize()

            df = Read.read()
            
            # Xóa bảng cũ nếu có
            for widget in data_frame.winfo_children():
                widget.destroy()
            
            # Tạo Treeview
            tree = ttk.Treeview(data_frame, columns=list(df.columns), show="headings")
            
            # Thêm dữ liệu vào Treeview
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            # Đặt tên cho cột
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            
            # Tạo thanh cuộn
            v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
            h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            tree.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")
            
            # Điều chỉnh grid layout
            data_frame.grid_rowconfigure(0, weight=1)
            data_frame.grid_columnconfigure(0, weight=1)
            
    



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

        for idx, label_text in enumerate(labels):
            label = tk.Label(data_frame, text=label_text)
            label.grid(row=idx, column=0, padx=(10, 2), pady=5, sticky='w')

            if label_text == 'WHO Region':
                selected_region = tk.StringVar()
                selected_region.set(who_region_options[0])  
                dropdown = tk.OptionMenu(data_frame, selected_region, *who_region_options)
                dropdown.grid(row=idx, column=1, padx=(2, 10), pady=5, sticky='ew', columnspan=2)
                inputs[label_text] = selected_region
            else:
                entry = tk.Entry(data_frame, font=("Arial", 10, "normal"))
                entry.grid(row=idx, column=1, padx=(2, 10), pady=5, sticky='ew', columnspan=2)
                inputs[label_text] = entry
                entries.append(entry)

                entry.bind("<Return>", lambda event, idx=idx: entries[min(idx + 1, len(entries) - 1)].focus())

        data_frame.grid_columnconfigure(1, weight=1)

        # Hàm lưu dữ liệu mới vào CSV
        def save_new_record():
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

                messagebox.showinfo("Thành công", "Bản ghi đã được thêm vào CSV thành công!")
                read_and_display_data()

                # Xóa dữ liệu trong các ô nhập liệu sau khi lưu thành công
                for key, widget in inputs.items():
                    if isinstance(widget, tk.Entry):
                        widget.delete(0, tk.END)
                    elif isinstance(widget, tk.StringVar):
                        widget.set(who_region_options[0]) 

            except ValueError as ve:
                messagebox.showerror("Lỗi nhập liệu", f"Giá trị không hợp lệ: {ve}")
            except FileNotFoundError:
                messagebox.showerror("Lỗi", "Không tìm thấy file CSV.")

        # Nút Lưu bản ghi
        save_button = tk.Button(data_frame, text="Add", command=save_new_record)
        save_button.grid(row=len(labels), column=1, pady=20)





    # ------------------------------------ Delete ------------------------------------
    def add_delete_interface():
        # Xóa giao diện cũ nếu đã hiển thị trước đó
        for widget in data_frame.winfo_children():
            widget.destroy()

        inputs = {}

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
            temp_name_delete = country_to_delete

            # Gọi hàm delete trong module Delete
            df = Delete.delete(temp_name_delete) 
            read_and_display_data()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")





    # -------------------------------------- Update ----------------------------------
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
        root.destroy()





    # --------------------------------------Interface ---------------------------------
    # Tạo các nút với nhãn theo yêu cầu
    buttons = ["View", "Create", "Update", "Delete", "Quit", "Chart"]
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
        elif button_text == "Chart":
            button.config(command=add_chart_interface)
        elif button_text == "Quit":
            button.config(command=quit_app)

    read_and_display_data()
    
    root.mainloop()  