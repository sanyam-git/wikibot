from wikibot import db
import datetime
from wikibot.database.static import stat

class Greet(db.Model):
    __tablename__ = 'greet'
    greet_id = db.Column(db.Integer, primary_key = True) 
    greet_question = db.Column(db.String(stat['MESSAGE_MAX_SIZE']))
    greet_answer = db.Column(db.String(stat['MESSAGE_MAX_SIZE']))
    greet_list = db.Column(db.Text(stat['KEYWORD_LIST_MAX_SIZE']))

class GreetKeywords(db.Model):
    __tablename__ = 'greetkeywords'
    greet_keyword_id = db.Column(db.Integer, primary_key = True)
    greet_id = db.Column(db.Integer)
    greet_keyword = db.Column(db.String(stat['KEYWORD_MAX_SIZE']))

class Messages(db.Model):
    __tablename__ = 'messages'
    time_recieved = db.Column(db.DateTime, default = datetime.datetime.now())
    message_id = db.Column(db.Integer, primary_key = True)
    message_body = db.Column(db.String(stat['MESSAGE_MAX_SIZE']))
    response_body = db.Column(db.Text(stat['RESPONSE_MAX_SIZE']))
    sender_id = db.Column(db.Integer)

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(200))
    user_email = db.Column(db.String(200))

class Responses(db.Model):
    __tablename__ = 'responses'
    response = db.Column(db.Text(stat['RESPONSE_MAX_SIZE']))
    response_id = db.Column(db.Integer, primary_key = True)
    keyword_list = db.Column(db.Text(stat['KEYWORD_LIST_MAX_SIZE']))
    category = db.Column(db.String(stat['CATEGORY_MAX_SIZE']))

class Questions(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(stat['QUESTION_MAX_SIZE']))
    response_id = db.Column(db.Integer)

class Keywords(db.Model):
    __tablename__ = 'keywords'
    keyword_id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(stat['KEYWORD_MAX_SIZE']))
    response_id = db.Column(db.Integer)

class Beta(db.Model):
    __tablename__ = 'beta'
    beta_id = db.Column(db.Integer, primary_key=True)
    beta_keyword = db.Column(db.String(stat['KEYWORD_MAX_SIZE']))
    beta_response = db.Column(db.String(stat['RESPONSE_MAX_SIZE']))