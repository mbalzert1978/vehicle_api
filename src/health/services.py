from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from src.database import execute

SQL = """SELECT 1=1;"""


async def get_database_status(connection: AsyncConnection) -> None:
    """Check the database status."""
    query = text(SQL)
    result = await execute(connection, query)
    result.one()
