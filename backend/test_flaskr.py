import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os.path import join, dirname

from flaskr import app
from models import setup_db, Question, Category

'''
to be able to test the app with mentioned data below 
you should check insert_test_data.py file which will read the data from test_question.txt and test_categories.txt
and call insertion methods 
you should mention local database information  
'''

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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(True if data is None else False)
        self.assertEqual(data['categories']["1"], 'Science')
        self.assertEqual(data['categories']["2"], 'Art')
        self.assertEqual(data['categories']['3'], 'Geography')

    def delete_categories(self):
        try:
            categories = Category.query.all()
            deleted = [Category(id=c.id, type=c.type) for c in categories]
            for c in categories:
                self.db.session.delete(c)
            self.db.session.commit()
            return deleted
        except:
            print('error happend while deleting categories')

    def add_categories(self):
        try:
            for c in self.deleted_categories:
                self.db.session.add(c)
                self.db.session.commit()

        except:
            print('error while adding categories')

        pass



    def test_get_422_error(self, res=None, data=None):
        if res is None or data is None:
            return
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertEqual(data['error'], 422)

    def test_get_404_error(self, res=None, data=None):
        if res is None or data is None:
            return
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')
        self.assertEqual(data['error'], 404)

    def test_notfound_path(self):
        res = self.client().get('/notfound')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_questions_pages(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 11)

    def test_get_trouble_questions_pages(self):
        res = self.client().get('/questions?page=-1')
        data = json.loads(res.data)
        self.test_get_422_error(res=res, data=data)

    def test_get_question_by_category_id(self):
        category_id = 4
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['totalQuestions'],
                         len(self.Question.query.all()))
        self.assertEqual(data['currentCategory'],
                         Category.query.get(category_id).type)
        category_id = 6
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['totalQuestions'],
                         len(self.Question.query.all()))
        self.assertEqual(data['currentCategory'],
                         Category.query.get(category_id).type)

    def test_get_trouble_get_trouble_questions_pages(self):
        res = self.client().get('categories/0/questions')
        data = json.loads(res.data)
        self.test_get_422_error(res, data)
        res = self.client().get('categories/1000000/questions')
        data = json.loads(res.data)
        self.test_get_404_error(res, data)

    def test_delete_question_by_id(self):
        question = self.Question.query.get(8)
        quesion_copy = self.Question( id=question.id , question=question.question,
                                     answer=question.answer, category=question.category, difficulty=question.difficulty)
        res = self.client().delete('question/8')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Question.query.get(8), None)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], quesion_copy.id)
        quesion_copy.insert()

    def test_get_trouble_delete_question_by_id(self):
        res = self.client().delete('question/-1')
        data = json.loads(res.data)
        self.test_get_404_error(res=res, data=data)

    def test_post_quizzes(self):
        previous_questions = [1, 2, 4]
        request_body = {
            'previous_questions': [1, 2, 4],
            'quiz_category': {'id': '4'}
        }
        res = self.client().post('quizzes', data=json.dumps(request_body),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question']['id'] not in previous_questions)

    def test_get_touble_post_quizzes(self):
        res = self.client().post('quizzes', data=json.dumps({}),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.test_get_422_error(res=res, data=data)

    def test_post_question(self):
        question = 'what is your name'
        request_body = {
            'question':  'what is your name',
            'answer':  'mohamed',
            'difficulty': 1,
            'category': 5,
        }
        res = self.client().post('/questions', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.Question.query.filter(self.Question.question == question))
        q = self.Question.query.filter(self.Question.answer == 'mohamed')[0]
        self.db.session.delete(q)
        self.db.session.commit()
    
    def test_get_trouble_post_questioin(self):        
        res = self.client().post('/questions', data=json.dumps({}), content_type='application/json')
        data = json.loads(res.data)
        self.test_get_422_error(res=res, data=data)
   
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()