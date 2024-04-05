from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'nugo', 'svianadze'
    return render_template('home.html', first_name=first_name,
                           last_name=last_name)

if __name__ == '__main__':
    app.run(debug=True)