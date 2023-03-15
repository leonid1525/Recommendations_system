from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
import datetime

from sqlalchemy.orm import relationship

from database import Base
from table_user import User
from table_post import Post

# Класс описывающий таблицу в базе данных, с помощью него, можно обращаться через sqlalchemy к таблице Feed
class Feed(Base):
    __tablename__ = "feed_action"
    user_id=Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id=Column(Integer, ForeignKey("post.id"), primary_key=True)
    action=Column(String)
    time=Column(DateTime)
    user=relationship("User")
    post=relationship("Post")
    