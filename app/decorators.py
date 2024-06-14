from functools import wraps

from flask import session, flash, url_for, redirect


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('U must log in')
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)

    return wrapper


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return redirect(url_for('blog.home'))
        return func(*args, **kwargs)

    return wrapper
