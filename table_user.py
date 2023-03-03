from sqlalchemy import Integer, Column, String, desc
from sqlalchemy.sql.functions import count

from database import Base, SessionLocal


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender=Column(Integer)
    age=Column(Integer)
    country=Column(String)
    city=Column(String)
    exp_group=Column(Integer)
    os=Column(String)
    source=Column(String)

if __name__ == "__main__":
    y=[]
    session=SessionLocal()
    res=session.query(User.country, User.os, count()).filter(User.exp_group==3).group_by(User.country, User.os).having(count()>100).order_by(desc(count()))
    for x in res:
        y.append(x)
    print(y)