from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

  # Explicación:
#Se utiliza SQLAlchemy para conectarse a una base de datos (en este ejemplo, SQLite).
#El archivo contiene la configuración de la base de datos y una función para obtener una sesión de base de datos para interactuar con los modelos.
