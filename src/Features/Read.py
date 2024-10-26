import pandas as pd

def read():
    csv_path = "Data/corona-virus-report/country_wise_latest.csv"
    df = pd.read_csv(csv_path)
    return df