from sqlalchemy import create_engine
from mysql.connector import Error
import pandas as pd
import os

try:
    connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
    connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format('tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')
    engine = create_engine(connect_string, connect_args=connect_args)


except Error as e:
    print("Error while connecting to MySQL", e)

#Loading csv file
han_data = pd.read_csv('HAN_csv_example.csv', index_col=0, delimiter=',')

#Writing data to MySQL
han_data.to_sql("han", con=engine, if_exists='replace', index=False)
print("Data written")

print("Conneciton closed")
