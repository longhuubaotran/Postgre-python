from database import initilizeTables, engine, sessionDB
from sqlalchemy import select
from database.models import Person

initilizeTables()


# with sessionDB.begin() as session:
#     session.add(Person(name="Long"))
#     session.commit()

with sessionDB.begin() as session:
    statement = select(Person)
    result = session.execute(statement)
    for user_obj in result.scalars():
        print(f"{user_obj.id} {user_obj.name} {user_obj.create_at}")
