from unicodedata import category
from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import transactions, user, auth, categories

# removed to allow alembic to manage db
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transactions.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(categories.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
