
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from backend/.env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Aiven MySQL connection details
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# CA certificate path
ca_value = os.getenv("MYSQL_SSL_CA", "aiven-ca.pem")
ca_path = Path(ca_value)

if not ca_path.is_absolute():
    ca_path = BASE_DIR / ca_path

required_values = {
    "DB_HOST": DB_HOST,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}

missing = [key for key, value in required_values.items() if not value]

if missing:
    raise RuntimeError(
        "Missing MySQL environment variables: " + ", ".join(missing)
    )

if not ca_path.is_file():
    raise RuntimeError(
        f"MySQL CA certificate not found: {ca_path}"
    )

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": str(ca_path),
        }
    },
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
