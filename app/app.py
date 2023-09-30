from flask_migrate import Migrate
from routes import create_app
from models.dbconfig import db

# App initialization
app = create_app()

# Configure the FLASK migrations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize Flask-Migrate
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(port=5555)