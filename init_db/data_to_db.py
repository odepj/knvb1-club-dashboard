import pandas as pd

from database import engine, session_factory
from database.models import Account

session = session_factory()
accounts = [Account(id='1X8m4', username='sdz', password='sdz', email='sdz@sdz.nl', display_name='SDZ', is_admin=False),
            Account(id='EoYnc', username='tos', password='tos', email='tos@tos.nl', display_name='TOS Actief', is_admin=False)]

session.add_all(accounts)
session.commit()

# Loading csv file
han_data = pd.read_csv('csv/adjusted_date_knvb_data.csv', index_col=0, delimiter=',')
accounts = pd.read_csv('csv/standard_accounts.csv', index_col=0, delimiter=',')

# Writing data to MySQL
han_data.to_sql("han", con=engine, if_exists='replace', index=False)
accounts.to_sql("accounts", con=engine, if_exists='replace', index=False)
print("Data written to database")
