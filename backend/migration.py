
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, select, insert, func

from database import engine as mysql_engine, Base
import models  # Registers User and Application tables

load_dotenv()

OLD_DATABASE_URL = os.getenv("OLD_DATABASE_URL")

if not OLD_DATABASE_URL:
    raise RuntimeError("OLD_DATABASE_URL is missing in backend/.env")

postgres_engine = create_engine(OLD_DATABASE_URL, pool_pre_ping=True)

# Create the destination tables in MySQL if they do not exist.
Base.metadata.create_all(bind=mysql_engine)

source_metadata = MetaData()
source_metadata.reflect(
    bind=postgres_engine,
    only=["users", "applications"],
)

target_metadata = Base.metadata

# Stop rather than accidentally duplicate or mix records.
with mysql_engine.connect() as connection:
    for table_name in ("users", "applications"):
        target_table = target_metadata.tables[table_name]
        count = connection.execute(
            select(func.count()).select_from(target_table)
        ).scalar_one()

        if count != 0:
            raise RuntimeError(
                f"MySQL table '{table_name}' is not empty. "
                "Migration stopped to avoid duplicate records."
            )

# Copy parent table first, then child table.
with postgres_engine.connect() as source, mysql_engine.begin() as target:
    for table_name in ("users", "applications"):
        source_table = source_metadata.tables[table_name]
        target_table = target_metadata.tables[table_name]

        rows = source.execute(select(source_table)).mappings().all()

        if rows:
            target.execute(
                insert(target_table),
                [dict(row) for row in rows],
            )

        print(f"{table_name}: copied {len(rows)} records")

print("Migration completed. Verify record counts before switching production.")
