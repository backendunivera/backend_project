from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class posts(Base):
    """
    Сущность "Пост"
    """
    __tablename__ = 'posts'
    postid = Column(Integer, primary_key=True, autoincrement=True)
    post_title = Column(String, nullable=False)
    description = Column(String, nullable=False)