from sqlalchemy import Connection, text

from app.database import execute

SQL = """SELECT 1=1;"""


def get_database_status(connection: Connection) -> None:
    """Check the database status."""
    execute(connection, text(SQL))
