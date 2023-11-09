import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from flask_restful import Api, Resource
from flask_cors import CORS


DATABASE_URI = 'postgresql://electropulse_db_fx03_user:o2p44iVPrHI7z4Dt0ghvP3c83n4C8ASt@dpg-cl5lps472pts73eoad30-a.oregon-postgres.render.com/electropulse_db_fx03'
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
api=Api(app)