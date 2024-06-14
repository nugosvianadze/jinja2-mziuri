from flask import session
from app import create_app

app = create_app()

# with app.app_context():
#     print('Creating Database And Tables')
#     db.create_all()
#     print('Created Database and tablesss')


@app.before_request
def make_session_permanent():
    session.permanent = True


if __name__ == '__main__':
    app.run(debug=True, port=5100)
