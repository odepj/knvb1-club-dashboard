"""
Initialization of database using ORM
"""
import urllib
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv

# load in the environment variables
load_dotenv()

AZURE_DB = os.getenv('AZURE_DB')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')

# If the AZURE_DB environment variable is not None
# then we know that we are dealing with an Azure Database
if AZURE_DB is not None:
    # Azure Server connection configuration
    params = urllib.parse.quote_plus(os.getenv('AZURE_DB'))
    connect_string = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine = create_engine(connect_string, echo=True)

# Same can be said for MySQL, if the MYSQL env variables are not None or an empty string
# then we know that we are dealing with a MySQL Database
elif None not in (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB):
    # MySQL Server connection configuration
    connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
    connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format(os.getenv('MYSQL_USER'), os.getenv(
       'MYSQL_PASSWORD'), os.getenv('MYSQL_HOST'), os.getenv('MYSQL_DB'))
    engine = create_engine(connect_string, connect_args=connect_args, echo=False)
else:
    print("No suitable database connection variables were found!")
    

# Echo=True enables loggingø
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def init_db():
    import database.models
    Base.metadata.create_all(engine)
    db_session.commit()


def session_factory():
    return db_session


init_db()