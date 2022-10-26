import pandas as pd

from database import session_factory
from database.models import Account, Han

session = session_factory()

# Loading csv file
han_data = pd.read_csv('csv/adjusted_date_knvb_data.csv', index_col=0, delimiter=',')
accounts = pd.read_csv('csv/standard_accounts.csv')

han_entities = Han.instantiate_from_dataframe(han_data)
account_entities = Account.instantiate_from_dataframe(accounts)

# Persisting data to DB
session.add_all(han_entities + account_entities)
session.commit()
print(f"Data written to database")
