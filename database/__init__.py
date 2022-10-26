"""
Initialization of database using ORM
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format('tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')

# Echo=True enables logging
engine = create_engine(connect_string, connect_args=connect_args, echo=False)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def init_db():
    import database.models
    Base.metadata.create_all(engine)
    db_session.commit()


def session_factory():
    return db_session


init_db()
