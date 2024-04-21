from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from forms import LoginForm

app = Flask(__name__)

conn = sqlite3.connect('mziuri.db')
cursor = conn.cursor()

cursor.execute("""
create table if not exists users 
(id integer primary key,
first_name text,
last_name text,
email text,
age integer,
birth_date text,
password text)
""")
conn.commit()

users = cursor.execute("""
select * from users
""")
print(users.fetchone())
# cursor.close()
# conn.close()


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

app.secret_key = 'ijbiazbadub84v8rbsibiewfvidvsa'

if __name__ == '__main__':
    app.run(debug=True, port=5100)
