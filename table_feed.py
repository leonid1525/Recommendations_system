from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
import datetime

from sqlalchemy.orm import relationship

from database import Base
from table_user import User
from table_post import Post

class Feed(Base):
    __tablename__ = "feed_action"
    user_id=Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id=Column(Integer, ForeignKey("post.id"), primary_key=True)
    action=Column(String)
    time=Column(DateTime)
    user=relationship("User")
    post=relationship("Post")
    