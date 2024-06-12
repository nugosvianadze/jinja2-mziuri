from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from random import randrange
from datetime import datetime, timedelta

import click
from werkzeug.utils import secure_filename
from functools import wraps

from enums import RoleEnum
from forms import LoginForm, RegistrationForm, UserUpdateForm, PostForm

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy import Integer, String, SmallInteger, BigInteger, select, ForeignKey, DateTime, MetaData
from flask_migrate import Migrate

app = Flask(__name__)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# initialize the app with the extension
db.init_app(app)
migrate.init_app(app, db)


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


# with app.app_context():
#     print('Creating Database And Tables')
#     db.create_all()
#     print('Created Database and tablesss')


def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value


app.jinja_env.filters['middle'] = middle

@app.before_request
def make_session_permanent():
    session.permanent = True


# creating commands

@app.cli.command('create_roles')
def create_roles():
    roles = [Role(title=role.value) for role in RoleEnum]
    db.session.add_all(roles)
    db.session.commit()
    click.echo('roles successfully created')


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('U must log in')
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return redirect(url_for('home'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
@app.route('/home')
@is_authenticated
def home():
    first_name, last_name = 'nugzari', 'svianadze'
    num = 25
    d = {'name': 'nugzari', 'age': 20}
    return render_template('home.html', first_name=first_name,
                           last_name=last_name, num=num, d=d)


@app.route('/login', methods=['GET', 'POST'])
@is_not_authenticated
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.check_credentials(email, password)
            if not user:
                flash('Invalid Credentials, Try Again!')
                return redirect(url_for('login'))
            session['user_id'] = user.id
            session['full_name'] = user.full_name
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route("/register", methods=["POST", "GET"])
@is_not_authenticated
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            profile_picture = form.profile_picture.data
            age = form.age.data
            address = form.address.data
            form_roles = form.roles.data

            filename = secure_filename(profile_picture.filename)
            profile_picture.save('static/uploads/' + filename)

            db_roles = Role.query.filter(Role.title.in_(form_roles)).all()

            if len(form_roles) != len(db_roles):
                non_exists = [role.title for role in db_roles]
                non_exists = [role for role in form_roles if role not in non_exists]
                roles = [Role(title=role) for role in non_exists]
                db.session.add_all(roles)
                db.session.commit()
                flash(f'new roles {non_exists} created!!!!')

            user = User.query.filter_by(first_name=first_name).all()
            if user:
                # flash('User With This Email Already Exists!')
                form.first_name.errors = ['User With This First Name Already Exists!']
                return render_template('register.html', form=form)

            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password, profile_picture=filename,
                        age=age, address=address)
            user.roles.extend(db_roles)
            db.session.add(user)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


app.secret_key = 'ijbiazbadub84v8rbsibiewfvidvsa'


@app.route('/users')
@is_authenticated
def users():

    form = UserUpdateForm()
    # 1
    users_data = User.query.all()
    # 2
    # stmt = select(User).where(User.age >= 18)
    # users_data = db.session.execute(stmt).scalars()
    # 3
    # users_data = db.session.query(User).where()
    return render_template('users.html', users=users_data, form=form)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserUpdateForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With this id-{user_id} Does Not Exists', 'error')
        return redirect(url_for('users'))
    # user = db.get_or_404(User, user_id)
    first_name = form.first_name.data
    last_name = form.last_name.data
    age = form.age.data
    address = form.address.data
    id_number = form.id_number.data
    print(form.id_number.validators)
    old_first_name = user.first_name
    user.first_name = first_name
    user.last_name = last_name
    user.age = age
    user.address = address
    user.id_card.id_number = id_number
    db.session.commit()
    flash(f'User {old_first_name} Successfully Updated!!', 'info')
    return redirect(url_for('users'))


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With this id-{user_id} Does Not Exists', 'warning')
        return redirect(url_for('users'))

    db.session.delete(user)
    db.session.commit()
    flash("User Successfully Deleted!!!!!", 'info')

    return redirect(url_for('users'))


@app.route('/user-posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))
    posts = user.posts
    return render_template('posts.html', posts=posts, user_id=user_id)


@app.route('/create_posts/<int:user_id>', methods=['GET', 'POST'])
def create_post(user_id):
    form = PostForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            post = Post(title=title, content=content, user=user)
            # user.posts.append(post)
            db.session.add(post)
            db.session.commit()
            flash('Post Successfuly Added')
            return redirect(url_for('user_posts', user_id=user_id))
        return render_template('create_post.html', form=form)

    return render_template('create_post.html', form=form, user_id=user_id)


@app.route('/add_id_card/<int:user_id>')
def add_id_card(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))
    if user.id_card:
        flash(f"User already has ID Card - {user.id_card.id_number}", 'error')
        return redirect(url_for('users'))
    id_card = IdCard(id_number=randrange(10000000000,99999999999),
                     created_at=datetime.now(), expire_at=datetime(2027, 10, 7),
                     user=user)
    db.session.add(id_card)
    db.session.commit()
    flash(f"ID Card for User {user.first_name} successfully Created!!!")
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('full_name', None)
    return redirect(url_for('login'))


@app.route('/my-page')
@is_authenticated
def my_page():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    return render_template('user_page.html', user=user)


if __name__ == '__main__':
    app.run(debug=True, port=5100)
