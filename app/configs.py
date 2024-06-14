from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SECRET_KEY = 'ijbiazbadub84v8rbsibiewfvidvsa'
