from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()
UsersModel = Table('users', metadata,
                   Column('id', Integer, primary_key=True, index=True),
                   Column('email', String(255), nullable=True),
                   Column('password', String(255), nullable=True),
                   Column('employee_id', Integer, nullable=True),
                   Column('role_id', Integer, nullable=True),
                   Column('user_status_id', Integer, nullable=True))
