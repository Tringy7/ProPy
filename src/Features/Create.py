import pandas as pd

def create(country, confirmed, deaths, recovered, active, new_cases, new_deaths, new_recovered, confirmed_last_week, who_region):
    new_data = {
        'Country/Region': country,
        'Confirmed': confirmed,
        'Deaths': deaths,
        'Recovered': recovered,
        'Active': active,
        'New cases': new_cases,
        'New deaths': new_deaths,
        'New recovered': new_recovered,
        'Confirmed last week': confirmed_last_week,
        'WHO Region': who_region,
    }
    
    # Tính toán cho các biến có công thức
    new_data['Deaths / 100 Cases'] = round((new_data['Deaths'] / new_data['Confirmed']) * 100, 2) if new_data['Confirmed'] > 0 else 0
    new_data['Recovered / 100 Cases'] = round((new_data['Recovered'] / new_data['Confirmed']) * 100, 2) if new_data['Confirmed'] > 0 else 0
    new_data['Deaths / 100 Recovered'] = round((new_data['Deaths'] / new_data['Recovered']) * 100, 2) if new_data['Recovered'] > 0 else 0
    new_data['1 week change'] = round(new_data['Confirmed'] - new_data['Confirmed last week'], 2)
    new_data['1 week % increase'] = round((new_data['1 week change'] / new_data['Confirmed last week']) * 100, 2) if new_data['Confirmed last week'] > 0 else 0

    # Đọc dữ liệu từ file CSV trước khi thêm bản ghi mới
    # df = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")
    df = pd.read_csv("Data/corona-virus-report/country_wise_latest.csv")

    # Chuyển đổi new_data thành DataFrame
    new_record_df = pd.DataFrame([new_data])
    
    # Sử dụng pd.concat để thêm bản ghi mới vào DataFrame
    df = pd.concat([df, new_record_df], ignore_index=True)
    
    # Lưu DataFrame vào file CSV
    df.to_csv("Data/corona-virus-report/country_wise_latest.csv", index=False)
    
    return df
