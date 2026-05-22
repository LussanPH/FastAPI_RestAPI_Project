from sqlalchemy.orm import sessionmaker
from models import db, Usuario

def fetch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

