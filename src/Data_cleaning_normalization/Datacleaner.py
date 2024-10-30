import pandas as pd
import numpy as np

def remove_duplicates(df):
    """Xóa các bản ghi trùng lặp dựa trên cột Country/Region, giữ lại bảng ghi cuối"""
    df.drop_duplicates(subset = "Country/Region",keep = 'last',inplace=True)
    return df
    
def process_missing_values(df, columns_number_of_cases):
    """
    Xử lí các cột bị thiếu giá trị
    Điền giá trị 0 cho các cột số ca bị thiếu
    Xóa hàng nếu các cột Country/Region và cột WHO Region bị thiếu 
    """

    #Thay các giá trị bị thiếu của các cột số ca bằng giá trị 0
    for column in columns_number_of_cases:
        df[column].fillna(0, inplace = True)

    #Xóa các hàng nếu cột Country/Region hoặc cột WHO Region bị thiếu giá trị
    df.dropna(subset = ["Country/Region", "WHO Region"], inplace = True)
    return df

def replace_negative_with_zero(df, columns):
    """Thay thế các giá trị âm trong các cột chỉ định bằng 0"""    
    for column in columns:
        df[column] = df[column].apply(lambda x:x if x >= 0 else 0 )
    return df

def remove_non_numeric(df, columns):
    """Loại bỏ các ký tự không phải số trong các cột số ca, giữ lại phần số nếu có"""
    
    def extract_number(value):
        # Chuyển giá trị sang chuỗi để dễ thao tác
        value = str(value)
        result = ""
        
        for char in value:
            # Kiểm tra nếu ký tự là số hoặc dấu thập phân, hoặc dấu âm ở đầu chuỗi
            if char.isdigit() or (char == '.' and '.' not in result) or (char == '-' and len(result) == 0):
                result += char
        
        # Nếu result có chứa số, chuyển thành float; nếu không, trả về NaN
        return float(result) if result else np.nan

    # Áp dụng hàm extract_number cho từng giá trị trong các cột chỉ định
    for column in columns:
        df[column] = df[column].apply(extract_number)
    
    return df


def remove_numbers_and_special_characters(df, columns):
    """Loại bỏ các kí tự số và kí tự đặc biệt trong các cột Country/Region và cột WHO Region"""
    def remove(value):
        value = str(value)  #Chuyển hết về str
        result = ""

        for char in value:  # Giữ lại các giá trị là chữ cái hoặc khoảng trắng hoặc kí tự ()
            if char.isalpha() or char.isspace() or char in "()":
                result+=char
        return result if result else np.nan #Trả về giá trị NaN nếu chuỗi result trống

    for column in columns:
        df[column] = df[column].apply(remove)

    return df

#Các cột số ca 
columns_number_of_cases = [
    'Confirmed', 'Deaths', 'Recovered', 'Active', 
    'New cases', 'New deaths', 'New recovered', 
    'Confirmed last week', '1 week change'
    ]


#Thực hiện các hàm làm sạch
def CleanUp():
    file_path = "Data/corona-virus-report/country_wise_latest.csv" 
    dataframe = pd.read_csv(file_path, header=0) #Lấy hàng đầu tiên làm tiêu đề
    remove_non_numeric(dataframe,columns_number_of_cases) #Loại bỏ các kí tự không phải số trong các cột số ca
    remove_numbers_and_special_characters(dataframe, ['Country/Region','WHO Region']) #Loại bỏ các kí tự không phải chữ cái
    replace_negative_with_zero(dataframe, columns_number_of_cases) #Thay các giá trị ở các cột số ca nếu là giá trị âm sẽ đổi thành 0 
    remove_duplicates(dataframe) #Xóa các hàng có giá trị trùng lặp dựa trên hàng Country\Region
    process_missing_values(dataframe, columns_number_of_cases) #Xử lí bị thiếu dữ liệu

    #Lưu bản làm sạch lại
    dataframe.to_csv(file_path, index=False)