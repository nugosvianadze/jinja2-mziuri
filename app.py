from flask import Flask, render_template

app = Flask(__name__)


def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value


print(app.jinja_env.filters)
app.jinja_env.filters['middle'] = middle

@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'nugzari', 'svianadze'
    num = 25
    d = {'name': 'nugzari', 'age': 20}
    return render_template('home.html', first_name=first_name,
                           last_name=last_name, num=num, d=d)

if __name__ == '__main__':
    app.run(debug=True, port=5100)