from flask import Flask
from .database import initialize_db
from flask_migrate import Migrate

app = Flask(__name__)


""" app.config['MONGODB_SETTINGS'] = {
    "db": "lineage",
    "host": "localhost",
    "username": "lineage",
    "password": "lineage@tiger",
    "authentication_source": "admin"
} """


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:RDn5ODgpaH45IKJFOgUL@containers-us-west-32.railway.app:6060/railway"#"sqlite:////lineage.db"
db = initialize_db()
#migrate = Migrate(app, db)
