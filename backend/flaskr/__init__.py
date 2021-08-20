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
  return 'hello'


def get_dic_gategories():
  categories = Category.query.all()
  response = {}
  for category in categories:
    response[category.id] = category.type
  return response

# api/v1.0/
@app.route('/categories')
def get_categories():
  try:
    categories = get_dic_gategories()
    if len(categories)==0 : raise Exception
    response = {}
    response['categories'] = categories
    return jsonify(response)
  except :
    return unprocessable_entity('database error might happend')    


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error' : 404 ,
        'message' :'Not Found'
    }), 404


@app.errorhandler(422)
def  unprocessable_entity(error):
    return jsonify({
        'error' : 422 ,
        'message' :'Unprocessable Entity'
    }), 422


# api/v1.0
def get_dic_questions(questions, paginate):
  paginate = len(questions) if paginate > len(questions) else paginate
  questions = questions[:paginate]
  json_questions = []
  for q in questions:
    json_questions.append({
    'id': q.id,
    'question': q.question,
     'answer': q.answer,
     'difficulty': q.difficulty,
      'category': q.category
    })
  return json_questions

    # questions?page=${integer}
@app.route('/questions')  # QUESTIONS_PER_PAGE = 10    Update

def get_questions():
  page = request.args.get('page', 1, type=int)
  if page is None or page < 0:    
    return unprocessable_entity('page numbers not valid')
  try:
    total_questions = Question.query.all()
    # questions = Question.query.filter( Question.category == '4').all()  # hsitory
    questions = list(filter(lambda c : c.category =='4' , total_questions))
    total_questions_len = len(total_questions)
    response = {}
    questions = get_dic_questions(questions=questions, paginate=page*QUESTIONS_PER_PAGE)
    response['questions'] = questions
    response['totalQuestions'] = total_questions_len
    response['categories'] = get_dic_gategories()
    response['currentCategory'] = 'History'
    return jsonify(response)
  except:
    return unprocessable_entity('error while query database')
  
@app.route('/categories/<int:category_id>/questions')
def get_questions_by_category_id(category_id):  
  category = Category.query.get(category_id)  
  total_questions = Question.query.all()
  questions = list(filter(lambda q : q.category == str(category_id), total_questions))

  total_questions_len = len(total_questions)
  if category_id < 1:
    return unprocessable_entity('not valid category id') 
  elif category is None or total_questions_len == 0:    
    return not_found('category not found or questions')
  try:
    questions = get_dic_questions(questions=questions, paginate=10)
    return jsonify({
      'questions' : questions ,
      'totalQuestions' : total_questions_len ,
      'currentCategory' : category.type
    })
  except:
    unprocessable_entity('error reading database or parse json')


@app.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):    
  q = Question.query.get(question_id)
  if question_id <= 0 or q is None:
    return not_found('question not found')
  try:
    q.delete()
    return jsonify({
      'success' : True,
      'id' : question_id
    })
  except:
    print('error while deleting question') 
    return jsonify({
      'success' : False ,
      'id' : q.id
    })

@app.route('/quizzes', methods=['POST'])
def get_quizzes():
  json_body  = request.get_json()
  if json_body is None or 'previous_questions' not in json_body or 'quiz_category' not in json_body:
    return unprocessable_entity('missing json data')  
  try:
    previous_questions = request.get_json().get('previous_questions')  
    quiz_category = request.get_json().get('quiz_category')
    questions  = Question.query.filter(Question.category == quiz_category['id']).all()
    questions = list(filter(lambda q : q.id not in previous_questions, questions))
    return jsonify({
      'question' : questions[0].format()
    })
  except:
    print('error while getting question')
    return jsonify({
      'success' : False ,       
    })


def handel_search(term):
  term = term.strip()
  total_questions = Question.query.all()
  total_questions_len = len(total_questions)
  matched  = Question.query.filter(Question.question.ilike(f'{term}')).all()
  
  return jsonify({
    'questions' : [q.format for q in matched],
    'totalQuestions' : total_questions_len ,
    'currentCategory' : matched[0].category if len(matched)>0 else '0'
  })
 
  

@app.route('/questions', methods=['POST'])
def create_question():
  json_body = request.get_json()
  if json_body is not None and 'searchTerm' in json_body:
    return handel_search(json_body['searchTerm'])
  elif json_body is None or 'question' not in json_body or 'answer' not in json_body or 'difficulty' not in json_body or 'category' not in json_body:
    return unprocessable_entity('missing json data')
  try:    
    question  = Question(question=json_body.get('question'), answer =json_body.get('answer') ,
                category=json_body.get('category'), difficulty=json_body.get('difficulty'))
    question.insert()    
    return jsonify({
      'success' : True
    })                          
  except:
    print('error while inserting question to database')
    return jsonify({
      'success' : False
    })
  
  


