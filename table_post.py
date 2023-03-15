from sqlalchemy import Integer, Column, String, desc
from sqlalchemy.orm import session, query
from database import Base, SessionLocal

# Класс описывающий таблицу в базе данных, с помощью него, можно обращаться через sqlalchemy к таблице Post
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)

# Проверка работоспособности класса
if __name__ == "__main__":
    result=[]
    session=SessionLocal()
    res=session.query(Post.id).filter(Post.topic=="business").order_by(Post.id.desc()).limit(10).all()
    for x in res:
        result.append(x[0])
    print(result)