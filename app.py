from datetime import datetime
from fastapi import FastAPI, HTTPException
from sqlalchemy import desc
from load_features import load_features
from load_model import load_models
from schema import UserGet, PostGet, FeedGet, Response
from typing import List
from table_feed import Feed
from table_post import Post
from table_user import User
from database import SessionLocal, engine
import pandas as pd
import uvicorn
import hashlib

# Загрузка данных о постах и пользователях
merge_user, merge_post, spisok_posts = load_features()

# Загрузка моделей, участвующих в А/Б-тесте
control_model = load_models("catboost (3)")
test_model = load_models("catboost (9)")

# Создание экземпляра веб-приложения
app=FastAPI()

# Дополнительные методы, с помощью которых можно производить А/Б-тестирование разных по параметрам моделей CatBoostClassifier
# При этом обе модели ждут одинаковый набор данных
# Данная функция, при помощи библиотеки hashlib, делит пользователей на 2 группы, используется в функции recomend
def get_exp_group(user_id: int) -> str:
    temp_exp_group=int(int(hashlib.md5((str(user_id) + 'my_salt').encode()).hexdigest(), 16) % 100)
    if temp_exp_group<=50:
        exp_group="control"
    elif temp_exp_group>50:
        exp_group="test"
    return exp_group

# Данная функция принимает модель и набор данных, после чего производит предсказания, используется в функции recomend
def get_recomend_group(df, model, session, limit):
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

# Функции запросов
# Функция запроса, возвращает информацию о запрошенном пользователе
@app.get("/user/{id}", response_model=UserGet)
def select(id):
    session=SessionLocal()
    result=session.query(User).filter(id==User.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

# Функция запроса, возвращает информацию о запрошенном посте
@app.get("/post/{id}", response_model=PostGet)
def select(id):
    session=SessionLocal()
    result=session.query(Post).filter(id==Post.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

# Функция запроса, возвращает информацию о действиях пользователя, таких как просмотр поста и лайки
@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.user_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

# функция запроса, возвращает информацию о действиях с конкретной публикацией, например, кто ее просмотрел и кому она понравилась
@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.post_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

# Функция-запрос, возвращает 5 постов, которые скорее всего лайкнет пользователь
@app.get("/post/recommendations/", response_model=Response)
def recomend(id: int, time: str, limit: int = 5, spisok_posts=spisok_posts):
    # Проверка того что пользователь существует в базе данных
    if id in merge_user["user_id"].values:
        # Превращаем строку во время
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        # Открываем соединение с базой данных
        session = SessionLocal()
        # Получаем столбик идентификаторов постов, которые пользователь уже просмотрел
        df_2 = session.query(Feed.post_id).filter(Feed.user_id == id, Feed.action == "view").all()
        # Столбик превращаем в список
        df_2 = pd.Series(df_2).tolist()
        # Вычитаем из общего списка постов, список постов, которые пользователь смотрел  
        spisok_posts = list(set(spisok_posts) - set(df_2))
        # Создаем таблицу, чтобы по ней создавать рекомендации, тут же из времени извлекаем необходимые признаки
        df = pd.DataFrame({'user_id': id,
                           'post_id': spisok_posts,
                           'week': time.isocalendar().week,
                           'day_of_week': time.isoweekday(),
                           'hour': time.time().hour,
                           'month': time.date().month})

        # Присоединяем к таблице информацию о постах
        df = df.merge(
            merge_post,
            how='left',
            left_on='post_id',
            right_on='post_id'
        )

        # Присоединяем к таблице информацию о пользователях
        df = df.merge(
            merge_user,
            how='left',
            left_on='user_id',
            right_on='user_id')
        
        # Определяем пользователя в группу, тестовую или контрольную, после чего проверяем в какую из них попал пользователь, делаем предсказания
        exp_group = get_exp_group(user_id=id)
        if exp_group == "control":
            result = get_recomend_group(df=df, model=control_model, session=session, limit=limit)
        elif exp_group == "test":
            result = get_recomend_group(df=df, model=test_model, session=session, limit=limit)
        else:
            raise ValueError('unknown group')
        # Возвращаем предсказания и принадлежность к группе
        return {"exp_group": exp_group,
                "recommendations": result}
    # Если пользователя не было в базе данных, то возвращаем ошибку
    else:
        raise HTTPException(404)

# Запуск сервера приложения
if __name__=="__main__":
    uvicorn.run(app, host='localhost', port=8899)