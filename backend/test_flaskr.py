import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os.path import join, dirname

from flaskr import app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        dotenv_path = join(dirname(__file__), 'testdb.env')
        load_dotenv(dotenv_path)
        host_name = os.environ.get('HOST_NAME')
        password = os.environ.get('PASSWORD')
        db_name = os.environ.get('DB_NAME')

        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://{host_name}:{password}@127.0.0.1:5432/{db_name}'
        self.Question = Question
        self.Category = Category
        self.db = setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    def test_add(self):
        c = self.Category(type='no type')
        self.db.session.add(c)
        self.db.session.commit()
        self.assertTrue(True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()