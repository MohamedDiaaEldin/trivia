import os
from sqlalchemy import Column, String, Integer, create_engine, engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), 'database.env')
load_dotenv(dotenv_path)
host_name = os.environ.get('HOST_NAME')
password = os.environ.get('PASSWORD')
db_name = os.environ.get('DB_NAME')


database_name = "trivia"
# database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
database_path = f'postgresql://{host_name}:{password}@127.0.0.1:5432/{db_name}'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  # def __init__(self, question, answer, category, difficulty):
  #   self.question = question
  #   self.answer = answer
  #   self.category = category
  #   self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }