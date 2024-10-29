import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame, Label, Toplevel, messagebox ,Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_cases_by_region(case_type):
    # Read data from CSV file
    data = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")
    
    # Calculate total confirmed cases, deaths, or recoveries by region
    if case_type == "Confirmed":
        region_cases = data.groupby('WHO Region')['Confirmed'].sum().reset_index()
    elif case_type == "Deaths":
        region_cases = data.groupby('WHO Region')['Deaths'].sum().reset_index()
    elif case_type == "Recovered":
        region_cases = data.groupby('WHO Region')['Recovered'].sum().reset_index()
    
    # Convert results to dictionary
    result = dict(zip(region_cases['WHO Region'], region_cases[case_type]))
    
    return result

def plot_cases_by_region(case_type):
    cases_by_region = calculate_cases_by_region(case_type)
    
    # Plot bar chart
    regions = list(cases_by_region.keys())
    cases = list(cases_by_region.values())

    fig, ax = plt.subplots(figsize=(10, 6))  # Change figure size
    ax.bar(regions, cases)
    ax.set_xlabel('WHO Region', fontsize=12)
    ax.set_ylabel(f'Total {case_type.lower()}', fontsize=12)
    ax.set_title(f'Total {case_type.lower()} by WHO Region', fontsize=14)
    ax.set_xticklabels(regions, rotation=45, ha='right', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid for better visibility

    return fig

def plot_country_pie_chart(country):
    # Read data from CSV file
    data = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")
    
    # Get the specific country data
    country_data = data[data['Country/Region'] == country].iloc[0]
    
    # Prepare data for pie chart
    confirmed = country_data['Confirmed']
    deaths = country_data['Deaths']
    recovered = country_data['Recovered']
    active_cases = confirmed - deaths - recovered
    remaining = confirmed - (deaths + recovered + active_cases)

    labels = ['Deaths', 'Recovered', 'Active Cases', 'Remaining']
    sizes = [deaths, recovered, active_cases, remaining]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    plt.title(f"COVID-19 Cases in {country}", fontsize=14)

    return fig

def show_plot(case_type):
    fig = plot_cases_by_region(case_type)

    # Create a Tkinter window
    plot_window = Tk()
    plot_window.title(f"Chart of {case_type} by WHO Region")
    plot_window.geometry("800x600")  # Window size

    # Add instruction label
    label = Label(plot_window, text=f"Chart of total {case_type.lower()} by WHO Region", font=("Arial", 14))
    label.pack(pady=10)

    # Create a Frame to contain the chart
    frame = Frame(plot_window)
    frame.pack(fill='both', expand=True)

    # Create a canvas for matplotlib
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_country_pie_chart(country):
    fig = plot_country_pie_chart(country)

    # Create a Toplevel window for the pie chart
    pie_window = Toplevel()
    pie_window.title(f"COVID-19 Pie Chart for {country}")
    pie_window.geometry("600x600")  # Window size

    # Add instruction label
    label = Label(pie_window, text=f"COVID-19 Cases Distribution in {country}", font=("Arial", 14))
    label.pack(pady=10)

    # Create a Frame to contain the chart
    frame = Frame(pie_window)
    frame.pack(fill='both', expand=True)

    # Create a canvas for matplotlib
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # Add exit button
    exit_button = Button(pie_window, text='Exit', command=pie_window.destroy, font=("Arial", 12))
    exit_button.pack(pady=20)

def country_selection():
    # Create a new window to input the country name
    selection_window = Toplevel()
    selection_window.title("Enter Country for Pie Chart")
    selection_window.geometry("400x200")

    label = Label(selection_window, text="Enter the name of the country to view the pie chart:")
    label.pack(pady=10)

    # Entry field for user to input country name
    country_entry = Entry(selection_window, width=30)
    country_entry.pack(pady=5)

    # Button to show the pie chart for the entered country
    def show_chart():
        country_name = country_entry.get().strip()  # Get the country name and remove any leading/trailing spaces
        
        # Get list of countries from CSV file
        data = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")
        countries = data['Country/Region'].unique().tolist()  # Get the list of countries

        try:
            # Attempt to find the country in the list
            if country_name not in countries:
                raise ValueError(f"Country '{country_name}' not found. Please enter a valid country name.")
            show_country_pie_chart(country_name)  # Show the pie chart for the entered country
            selection_window.destroy()  # Close the selection window
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error message if country is not found

    country_button = Button(selection_window, text='Show Pie Chart', command=show_chart)
    country_button.pack(pady=10)

    # Add exit button
    exit_button = Button(selection_window, text='Exit', command=selection_window.destroy)
    exit_button.pack(pady=5)