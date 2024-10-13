from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import settings


engine = create_engine(f'{settings.db_url}', connect_args={"check_same_thread": False})

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
    print('Database created.')