from pony.orm import *
from datetime import datetime

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(str)
    nickname = Optional(str)
    name = Required(str)
    meets = Set('Meet')

class Meet(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    date = Required(datetime)
    user = Optional(User)



try:
    db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
except Exception as Ex:
    print(Ex)