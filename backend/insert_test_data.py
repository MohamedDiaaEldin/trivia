from posixpath import split
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from models import setup_db,  Question, Category

database_name= ''
host_name = ''
password = ''
path = f'postgresql://{host_name}:{password}@127.0.0.1:5432/{database_name}'

app = Flask(__name__)
db = setup_db(app, path)

def insert_categories():
    f = open("test_categories.txt", "r")
    for r in f:
        words = r.strip().split(',')
        c =  Category(type=words[1])
        db.session.add(c)
        db.session.commit()

def insert_questions():
    f = open("test_questions.txt", "r")
    for r in f:
        words = r.strip().split(',')
        q =  Question(id=int(words[0]), question=words[1], answer=words[2], category=words[3], difficulty=int(words[4]))
        db.session.add(q)
        db.session.commit()


insert_categories()

insert_questions()
