from flask import Config, Flask, redirect, url_for
from flask_login import LoginManager

from database.engine import db
from database.models import User

from routes.init_routes import init_routes


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    init_routes(app)

    return app


app = Flask(__name__)
app.config.from_object('config')


db.init_app(app=app)

login_manager = LoginManager()
login_manager.login_view = 'books.login'
login_manager.init_app(app)


@app.route('/')
def home():
    return redirect(url_for('books.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_routes(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)