import pandas as pd


def standardize_country_region(df):
    """Chuẩn hóa cột Country/Region để loại bỏ khoảng trắng thừa và viết hoa chữ cái đầu."""
    df['Country/Region'] = df['Country/Region'].str.strip().str.title()
    return df



def standardize_WHO_region(df, valid_WHO_Regions):
    """Chuẩn hóa cột Country/Region để loại bỏ khoảng trắng thừa và viết hoa chữ cái đầu
       Xem thử giá trị WHO có hợp lệ không, nếu không sẽ xóa hàng đó"""
    df['WHO Region'] = df['WHO Region'].str.strip().str.title()

    #Giữ lại các giá trị WHO Region hợp lệ
    df = df[df['WHO Region'].isin(valid_WHO_Regions)].reset_index(drop=True)
    return df


def round_columns(df, columns):
    """Làm tròn 2 chữ số sau dấu phẩy các giá trị trong các cột tỉ lệ"""
    df[columns] = df[columns].round(2)
    return df

#Các cột tỉ lệ
ratio_columns = ["Deaths / 100 Cases", "Recovered / 100 Cases", "Deaths / 100 Recovered", "1 week % increase"]


#Các WHO Region hợp lệ 
valid_WHO_Regions = ["Africa", "Americas", "Eastern Mediterranean", "Europe", "South-East Asia", "Western Pacific"]


def normalize():
    file_path = "Data/corona-virus-report/country_wise_latest.csv" 
    dataframe = pd.read_csv(file_path, header=0) #Lấy hàng đầu tiên làm tiêu đề
    dataframe = standardize_country_region(dataframe) #Chuẩn hóa cột Country/Region
    dataframe = standardize_WHO_region(dataframe, valid_WHO_Regions) #Chuẩn hóa cột WHO/Region
    dataframe = round_columns(dataframe, ratio_columns) # Làm tròn các cột tỉ lệ
    dataframe.to_csv(file_path, index=False) #Lưu lại sau khi chuẩn hóa 
