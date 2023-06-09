from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

# первый способ создания модели "императивный"

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20))
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(50)),
    Column('username', String(50)),
    Column('password', String()),
    Column('name', String(20)),
    Column('surname', String(20)),
    Column('role_id', Integer, ForeignKey('roles.id')),
)

