#from sqlalchemy import create_engine
#from sqlalchemy.orm import declarative_base,sessionmaker

#SQLALCHEMY_DATABASE_URL  = "sqlite:///C:/Users/david/test.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/david/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 