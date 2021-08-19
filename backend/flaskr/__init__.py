import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from dotenv import load_dotenv
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# create and configure the app
app = Flask(__name__)
setup_db(app)
  


@app.route('/')
def index():
  return 'hiiiiiiiiii'


