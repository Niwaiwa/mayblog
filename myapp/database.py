from conf import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conn_url = URL(
    drivername='mysql+mysqldb',
    username=settings.username,
    password=settings.password,
    host=settings.host,
    port=settings.port,
    database=settings.database,
    query={'charset': 'utf8mb4'}
)

# engine = create_engine('mysql+mysqldb://root:password@127.0.0.1:3306/testdb', echo=True)
engine = create_engine(conn_url, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import myapp.model.users
    from myapp.model import users
    Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#     init_db()