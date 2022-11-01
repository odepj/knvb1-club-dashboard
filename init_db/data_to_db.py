import pandas as pd

from database import session_factory
from database.models import Account, Han

session = session_factory()


def persist(data: list):
    try:
        session.add_all(data)
        session.commit()
    except:
        print(f"table for {type(data[0])} contains duplicate entries")


# Loading csv file
han_data = pd.read_csv('csv/adjusted_date_knvb_data.csv', index_col=0, delimiter=',')
accounts = pd.read_csv('csv/standard_accounts.csv')

han_entities = Han.instantiate_from_dataframe(han_data)
account_entities = Account.instantiate_from_dataframe(accounts)

# Persisting data to DB
persist(han_entities)  # This will append and create duplicates so check DB first or after
persist(account_entities)
print(f"Data written to database")
