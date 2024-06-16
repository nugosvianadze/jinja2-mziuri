import os

from flask import Blueprint, request, flash, url_for, redirect, session, render_template
from werkzeug.utils import secure_filename

from app.blog.models import Role
from app.decorators import is_not_authenticated, is_authenticated
from app.extensions import db
from app.user.forms import LoginForm, RegistrationForm, UserUpdateForm
from app.user.models import User
from app.utils import TEMPLATE_FOLDER, STATIC_FOLDER


user_bp = Blueprint('user', __name__, template_folder=TEMPLATE_FOLDER,
                    url_prefix='/user', static_folder=STATIC_FOLDER)

"""localhost:5000/user/login"""


@user_bp.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('user.login'))
            session['user_id'] = user.id
            session['full_name'] = user.full_name
            return redirect(url_for('blog.home'))
        print(form.errors)
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@user_bp.route("/register", methods=["POST", "GET"])
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
            return redirect(url_for('blog.home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@user_bp.route('/users')
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


@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserUpdateForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With this id-{user_id} Does Not Exists', 'error')
        return redirect(url_for('user.users'))
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
    return redirect(url_for('user.users'))


@user_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With this id-{user_id} Does Not Exists', 'warning')
        return redirect(url_for('user.users'))

    db.session.delete(user)
    db.session.commit()
    flash("User Successfully Deleted!!!!!", 'info')

    return redirect(url_for('user.users'))


@user_bp.route('/user-posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))
    posts = user.posts
    return render_template('posts.html', posts=posts, user_id=user_id)


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('full_name', None)
    return redirect(url_for('user.login'))


@user_bp.route('/my-page')
@is_authenticated
def my_page():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    return render_template('user_page.html', user=user)
