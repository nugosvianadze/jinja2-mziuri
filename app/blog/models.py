from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    images = db.relationship('PostImage', backref='post', cascade='all, delete')


class PostImage(db.Model):
    __tablename__ = 'post_images'
    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))


class IdCard(db.Model):
    __tablename__ = 'id_cards'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_number: Mapped[int]
    created_at = mapped_column(DateTime)
    expire_at = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='id_card')


class Role(db.Model):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
