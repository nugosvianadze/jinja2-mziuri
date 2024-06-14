from datetime import datetime
from random import randrange

from flask import Blueprint, request, flash, url_for, redirect, session, render_template

from app.blog.forms import PostForm
from app.blog.models import Role, IdCard, Post
from app.decorators import is_authenticated
from app.extensions import db
from app.user.models import User
from app.utils import TEMPLATE_FOLDER

print(TEMPLATE_FOLDER)
blog_bp = Blueprint('blog', __name__, template_folder=TEMPLATE_FOLDER, url_prefix='/blog')


@blog_bp.route('/')
@is_authenticated
def home():
    first_name, last_name = 'nugzari', 'svianadze'
    num = 25
    d = {'name': 'nugzari', 'age': 20}
    return render_template('home.html', first_name=first_name,
                           last_name=last_name, num=num, d=d)


@blog_bp.route('/create_posts/<int:user_id>', methods=['GET', 'POST'])
def create_post(user_id):
    form = PostForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))

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


@blog_bp.route('/add_id_card/<int:user_id>')
def add_id_card(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))
    if user.id_card:
        flash(f"User already has ID Card - {user.id_card.id_number}", 'error')
        return redirect(url_for('user.users'))
    id_card = IdCard(id_number=randrange(10000000000,99999999999),
                     created_at=datetime.now(), expire_at=datetime(2027, 10, 7),
                     user=user)
    db.session.add(id_card)
    db.session.commit()
    flash(f"ID Card for User {user.first_name} successfully Created!!!")
    return redirect(url_for('user.users'))
