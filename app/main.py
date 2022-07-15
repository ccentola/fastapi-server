from unicodedata import category
from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import transactions, user, auth, categories
from fastapi.middleware.cors import CORSMiddleware


# removed to allow alembic to manage db
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(transactions.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(categories.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
