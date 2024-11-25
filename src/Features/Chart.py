import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame, Label, Toplevel, messagebox ,Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Features import Read

def calculate_cases_by_region(case_type):
    data = Read.read()
    
    # Tính toán
    if case_type == "Confirmed":
        region_cases = data.groupby('WHO Region')['Confirmed'].sum().reset_index()
    elif case_type == "Deaths":
        region_cases = data.groupby('WHO Region')['Deaths'].sum().reset_index()
    elif case_type == "Recovered":
        region_cases = data.groupby('WHO Region')['Recovered'].sum().reset_index()
    
    result = dict(zip(region_cases['WHO Region'], region_cases[case_type]))
    
    return result

def plot_cases_by_region(case_type):
    cases_by_region = calculate_cases_by_region(case_type)
    
    regions = list(cases_by_region.keys())
    cases = list(cases_by_region.values())

    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.bar(regions, cases)
    ax.set_xlabel('WHO Region', fontsize=12)
    ax.set_ylabel(f'Total {case_type.lower()}', fontsize=12)
    ax.set_title(f'Total {case_type.lower()} by WHO Region', fontsize=14)
    ax.set_xticklabels(regions, rotation=45, ha='right', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig

def plot_country_pie_chart(country):
    data = Read.read()
    
    # Lấy dữ liệu 'Country/Region'
    country_data = data[data['Country/Region'] == country].iloc[0]
    
    deaths = country_data['Deaths']
    recovered = country_data['Recovered']
    active_cases = country_data['Active']

    labels = ['Deaths', 'Recovered', 'Active Cases']
    sizes = [deaths, recovered, active_cases]
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90
    )
    ax.axis('equal') 

    ax.legend(wedges, labels, title="Categories", loc="upper right", bbox_to_anchor=(1.2, 1))

    plt.title(f"COVID-19 Cases in {country}", fontsize=14)

    return fig

def show_plot(case_type):
    fig = plot_cases_by_region(case_type)

    # Tạo giao diện
    plot_window = Tk()
    plot_window.title(f"Chart of {case_type} by WHO Region")
    plot_window.geometry("800x600") 

    label = Label(plot_window, text=f"Chart of total {case_type.lower()} by WHO Region", font=("Arial", 14))
    label.pack(pady=10)

    frame = Frame(plot_window)
    frame.pack(fill='both', expand=True)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_country_pie_chart(country):
    fig = plot_country_pie_chart(country)

    pie_window = Toplevel()
    pie_window.title(f"COVID-19 Pie Chart for {country}")
    pie_window.geometry("600x600") 

    label = Label(pie_window, text=f"COVID-19 Cases Distribution in {country}", font=("Arial", 14))
    label.pack(pady=10)

    frame = Frame(pie_window)
    frame.pack(fill='both', expand=True)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    exit_button = Button(pie_window, text='Exit', command=pie_window.destroy, font=("Arial", 12))
    exit_button.pack(pady=20)

def country_selection():
    selection_window = Toplevel()
    selection_window.title("Enter Country for Pie Chart")
    selection_window.geometry("400x200")

    label = Label(selection_window, text="Enter the name of the country to view the pie chart:")
    label.pack(pady=10)

    country_entry = Entry(selection_window, width=30)
    country_entry.pack(pady=5)

    def show_chart():
        country_name = country_entry.get().strip()  
        
        # Tạo danh sách dữ liệu 'Country/Region'
        data = Read.read()
        countries = data['Country/Region'].unique().tolist()  

        try:
            if country_name not in countries:
                raise ValueError(f"Country '{country_name}' not found. Please enter a valid country name.")
            show_country_pie_chart(country_name)  
            selection_window.destroy() 
        except ValueError as e:
            messagebox.showerror("Error", str(e))  

    country_button = Button(selection_window, text='Show Pie Chart', command=show_chart)
    country_button.pack(pady=10)

    # Thoát
    exit_button = Button(selection_window, text='Exit', command=selection_window.destroy)
    exit_button.pack(pady=5)