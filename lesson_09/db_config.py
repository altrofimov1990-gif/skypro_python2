from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Вставь свои данные вместо myuser/mypassword/mydatabase
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()