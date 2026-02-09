import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.base import Table, Booking, User

TABLE_CONFIG = [
    {"count": 7, "capacity": 2},
    {"count": 6, "capacity": 3},
    {"count": 3, "capacity": 6},
]


async def init_tables():
    """
    Initializes the database with predefined restaurant tables.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Check if tables are already initialized
            result = await session.execute(select(Table))
            tables = result.scalars().all()

            if tables:
                print("Tables already initialized.")
                return

            print("Initializing tables...")
            table_number = 1

            for config in TABLE_CONFIG:
                for _ in range(config["count"]):
                    new_table = Table(
                        name=f"Table {table_number}",
                        capacity=config["capacity"]
                    )
                    session.add(new_table)
                    table_number += 1

            await session.commit()
            print(f"Successfully created {table_number - 1} tables.")
        except Exception as e:
            print(f"Error during initialization: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(init_tables())
