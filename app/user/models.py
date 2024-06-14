from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

user_m2m_roles = db.Table(
    'user_roles',
    db.Column("user_id", db.ForeignKey('users.id'), primary_key=True),
    db.Column("role_id", db.ForeignKey('roles.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(default='test@gmail.com')
    password: Mapped[str] = mapped_column(nullable=True)
    profile_picture: Mapped[str]
    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]
    id_card = db.relationship('IdCard', back_populates='user', uselist=False, cascade='all, delete')
    roles = db.relationship('Role', secondary=user_m2m_roles,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='user', cascade='all, delete')

    @classmethod
    def check_credentials(cls, email, password):
        user = cls.query.filter_by(email=email, password=password).first()
        return user

    @property
    def full_name(self):
        return self.first_name + self.last_name
