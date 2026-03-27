from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PRIMARY_DATABASE_URL = "postgresql+psycopg://app_user:app_password@localhost:5432/scaling_reads"
REPLICA_DATABASE_URL = "postgresql+psycopg://app_user:app_password@localhost:5433/scaling_reads"

engine_primary = create_engine(PRIMARY_DATABASE_URL)
engine_replica = create_engine(REPLICA_DATABASE_URL)

SessionPrimary = sessionmaker(bind=engine_primary)
SessionReplica = sessionmaker(bind=engine_replica)

Base = declarative_base()


def get_db_write():
    db = SessionPrimary()
    try:
        yield db
    finally:
        db.close()


def get_db_read():
    db = SessionReplica()
    try:
        yield db
    finally:
        db.close()
