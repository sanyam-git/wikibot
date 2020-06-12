from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wikibot.config.config import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config['SQLALCHEMY_DATABASE_URI']
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

from wikibot.dashboard.route import dashboard_bp
from wikibot.bot.route import bot_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(bot_bp)
