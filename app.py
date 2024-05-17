from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from forms import LoginForm, RegistrationForm, UserUpdateForm

app = Flask(__name__)


def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value


def create_conn():
    conn = sqlite3.connect('mziuri.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_cursor(conn):
    return conn.cursor()


def close_conn(conn):
    return conn.close()


app.jinja_env.filters['middle'] = middle


@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'nugzari', 'svianadze'
    num = 25
    d = {'name': 'nugzari', 'age': 20}
    return render_template('home.html', first_name=first_name,
                           last_name=last_name, num=num, d=d)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('forma validuria')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            age = form.age.data
            email = form.email.data
            birthday = form.birthday.data
            password = form.password.data

            conn = create_conn()
            cursor = create_cursor(conn)
            cursor.execute("""
            select * from users where email = ?
            """, (email,))
            user_exists = cursor.fetchone()
            close_conn(conn)
            print(user_exists)
            if user_exists is not None:
                # flash('User With This Email Already Exists!')
                form.email.errors = ['User With This Email Already Exists!']
                return render_template('register.html', form=form)

            conn = create_conn()
            cursor = create_cursor(conn)
            cursor.execute("""
            insert into users (first_name, last_name, email, age, birth_date, password) values
            (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, age, birthday, password))
            conn.commit()
            close_conn(conn)
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

app.secret_key = 'ijbiazbadub84v8rbsibiewfvidvsa'


@app.route('/users')
def users():
    form = UserUpdateForm()
    conn = create_conn()
    cursor = create_cursor(conn)
    cursor.execute("select * from users")
    users = cursor.fetchall()
    close_conn(conn)
    return render_template('users.html', users=users, form=form)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserUpdateForm()
    conn = create_conn()
    cursor = create_cursor(conn)
    first_name = form.first_name.data
    last_name = form.last_name.data
    age = form.age.data
    user = cursor.execute("""
    select * from users where id = ?
    """, (user_id, ))
    if not user.fetchone():
        flash('User With This Id Does Not Exist!')
        return redirect(url_for('users'))
    cursor.execute("""
    update users set first_name = ?, last_name = ?, age = ? where id = ?
    """, (first_name, last_name, age, user_id))
    flash("User Updated Successfully!!!!")
    conn.commit()
    close_conn(conn)
    return redirect(url_for('users'))


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = create_conn()
    cursor = create_cursor(conn)
    user = cursor.execute("""
        select * from users where id = ?
        """, (user_id,))
    if not user.fetchone():
        flash('User With This Id Does Not Exist!')
        return redirect(url_for('users'))
    cursor.execute("""
    delete from users where id = ?
    """, (user_id,))
    flash("User Successfully Deleted!!!!!")
    conn.commit()
    close_conn(conn)
    return redirect(url_for('users'))
if __name__ == '__main__':
    app.run(debug=True, port=5100)
