from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "Hello World",
        "content": "Welcome to my awesome blog",
        "id": 1,
    },
    {
        "title": "Hello Galaxy",
        "content": "Snark quarf",
        "id": 2,
    },
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


# posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return {"data": post}

    return {"data": None}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    for post_index, post_dict in enumerate(my_posts):
        if post_dict["id"] == post_id:
            my_posts[post_index] = post.dict()
            return {"data": my_posts[post_index]}
    return {"data": None}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for post_index, post_dict in enumerate(my_posts):
        if post_dict["id"] == post_id:
            my_posts.pop(post_index)
            return {"data": my_posts}
    return {"data": None}
