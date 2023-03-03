from datetime import datetime
from fastapi import FastAPI, HTTPException
from sqlalchemy import desc
from load_features import load_features
from load_model import load_models
from schema import UserGet, PostGet, FeedGet
from typing import List
from table_feed import Feed
from table_post import Post
from table_user import User
from database import SessionLocal, engine
import pandas as pd
import uvicorn

# Loading data by posts and users
merge_user, merge_post, spisok_posts = load_features()

# We ship the model
model = load_models()

# Create an instance of the web application
app=FastAPI()

# Request function, returns information about the requested user
@app.get("/user/{id}", response_model=UserGet)
def select(id):
    session=SessionLocal()
    result=session.query(User).filter(id==User.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

# Request function, returns information about the requested post
@app.get("/post/{id}", response_model=PostGet)
def select(id):
    session=SessionLocal()
    result=session.query(Post).filter(id==Post.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

# Query function, returns information about user actions, such as viewing a post and likes
@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.user_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

# Query function, returns information about actions with a particular post, such as who viewed and liked it
@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.post_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

# Query function, returns 5 posts that the user is most likely to like
@app.get("/post/recommendations/", response_model=List[PostGet])
def recomend(id: int, time: str, limit: int = 5, spisok_posts=spisok_posts):
    if id in merge_user["user_id"].values:
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        session = SessionLocal()
        df_2 = session.query(Feed.post_id).filter(Feed.user_id == id, Feed.action == "view").all()
        df_2 = pd.Series(df_2).tolist()
        spisok_posts = list(set(spisok_posts) - set(df_2))
        df = pd.DataFrame({'user_id': id,
                           'post_id': spisok_posts,
                           'week': time.isocalendar().week,
                           'day_of_week': time.isoweekday(),
                           'hour': time.time().hour,
                           'month': time.date().month})

        df = df.merge(
            merge_post,
            how='left',
            left_on='post_id',
            right_on='post_id'
        )

        df = df.merge(
            merge_user,
            how='left',
            left_on='user_id',
            right_on='user_id')
        df = df.drop(["user_id"], axis=1)

        pred = pd.DataFrame(model.predict_proba(df)[:, 1], columns=["predict"])
        df = pd.concat([df, pred], axis=1)
        df = df.sort_values(by=["predict"])

        spisok = df["post_id"].tail(limit).tolist()
        for x in range(len(spisok)):
            spisok[x] = int(spisok[x])
        result = session.query(Post).filter(Post.id.in_(spisok)).limit(limit).all()
        session.close()
        engine.dispose()

        return result
    else:
        raise HTTPException(404)

# Starting the web application server
if __name__=="__main__":
    uvicorn.run(app, host='localhost', port=8899)