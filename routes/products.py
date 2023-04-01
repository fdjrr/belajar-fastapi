from fastapi import APIRouter, Response, status

from config.database import conn
from models.products import ProductsModel
from schemas.products import Products, ProductSchema

products = APIRouter()


@products.get('/products', response_model=Products, description="Show all products")
async def get_all_products(limit: int = 10, offset: int = 0):
  query = ProductsModel.select().offset(offset).limit(limit)
  products = conn.execute(query).fetchall()
  products = [product._asdict() for product in products]
  response = {
    "limit": limit,
    "offset": offset,
    "products": products
  }
  return response


@products.get('/products/{id}', description='Get Product by ID')
async def get_product_by_id(id: int, response: Response):
  query = ProductsModel.select().where(ProductsModel.c.id == id)
  product = conn.execute(query).fetchone()
  if product is None:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Product not found."}
  else:
    response.status_code = status.HTTP_200_OK
    return product._asdict()


@products.post('/products', description="Add a new product")
async def add_product(product: ProductSchema):
  query = ProductsModel.insert().values(
    name=product.name,
    description=product.description,
    price=product.price,
  )
  conn.execute(query)

  query = ProductsModel.select().order_by(ProductsModel.c.id.desc())
  product = conn.execute(query).fetchone()

  # commit the transaction
  conn.commit()

  return product._asdict()


@products.post('/products/{id}', description='Update a product')
async def update_product(id: int, product: ProductSchema):
  query = ProductsModel.update().where(ProductsModel.c.id == id).values(
    name=product.name,
    description=product.description,
    price=product.price,
  )
  conn.execute(query)

  query = ProductsModel.select().where(ProductsModel.c.id == id)
  product = conn.execute(query).fetchone()

  # commit the transaction
  conn.commit()

  return product._asdict()


@products.delete('/products/{id}', description='Delete a product')
async def delete_product(id: int, response: Response):
  query = ProductsModel.select().where(ProductsModel.c.id == id)
  product = conn.execute(query).fetchone()

  if product is None:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Product not found."}
  else:
    query = ProductsModel.delete().where(ProductsModel.c.id == id)
    conn.execute(query)

    # commit the transaction
    conn.commit()

    response.status_code = status.HTTP_200_OK
    return {"message": "Product deleted."}
