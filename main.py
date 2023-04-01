import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.products import products
from routes.user import user

app = FastAPI()


def cors_headers(app):
  app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
  )
  return app


# app.include_router(products)
app.include_router(user)


@app.get('/')
async def home():
  return {'status': True}


if __name__ == '__main__':
  uvicorn.run('main:app', host='0.0.0.0', port=8000)
