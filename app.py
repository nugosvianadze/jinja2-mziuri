from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from forms import LoginForm, RegistrationForm

app = Flask(__name__)


# cursor.execute("""
# create table if not exists users
# (id integer primary key,
# first_name text,
# last_name text,
# email text,
# age integer,
# birth_date text,
# password text)
# """)


def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value


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

            conn = sqlite3.connect('mziuri.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("""
            select * from users where email = ?
            """, (email,))
            user_exists = cursor.fetchone()
            conn.close()
            print(user_exists)
            if user_exists is not None:
                # flash('User With This Email Already Exists!')
                form.email.errors = ['User With This Email Already Exists!']
                return render_template('register.html', form=form)

            conn = sqlite3.connect('mziuri.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("""
            insert into users (first_name, last_name, email, age, birth_date, password) values
            (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, age, birthday, password))
            conn.commit()
            conn.close()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

app.secret_key = 'ijbiazbadub84v8rbsibiewfvidvsa'


@app.route('/users')
def users():
    conn = sqlite3.connect('mziuri.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select * from users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, port=5100)
