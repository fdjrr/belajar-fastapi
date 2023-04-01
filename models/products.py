from sqlalchemy import Column, Float, Integer, MetaData, String, Table, Text

metadata = MetaData()
ProductsModel = Table('products', metadata,
                      Column('id', Integer, primary_key=True, index=True),
                      Column('name', String(255), nullable=False),
                      Column('description', Text, nullable=False),
                      Column('price', Float(10, 2)))
