from sqlalchemy import create_engine
from mysql.connector import Error
import pandas as pd
import os

try:
    engine = create_engine(f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")
    cnx = engine.connect()

except Error as e:
    print("Error while connecting to MySQL", e)

#Loading csv file
han_data = pd.read_csv('HAN_csv_example.csv', index_col=0, delimiter=',')

#Writing data to MySQL
han_data.to_sql("han", con=engine, if_exists='replace', index=False)
print("Data written")

cnx.close()
print("Conneciton closed")
