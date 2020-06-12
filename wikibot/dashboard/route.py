from flask import Blueprint, render_template, request
from sqlalchemy import desc,func
import json

from wikibot import db
from wikibot.database.models import Greet,GreetKeywords,Messages,Users,Responses,Questions,Keywords,Beta
from wikibot.database.static import stat
from wikibot.dashboard.util import length_checker,api_error_handler
from wikibot.bot.util import process_raw

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/',methods = ['GET'])
def main():
    return render_template('main.html')

@dashboard_bp.route('/dashboard', methods = ['GET'])
def dashboard():
    return render_template('dashboard.html')


@dashboard_bp.route('/api/dashboard/beta',methods = ['GET'])
def dashboard_api_beta():
    response = Beta.query.all()
    data = []
    for i in response:
        temp = {}
        temp['beta_id'] = i.beta_id
        temp['beta_keyword'] = i.beta_keyword
        temp['beta_response'] = i.beta_response
        data.append(temp)
    response = json.dumps(data)
    return response

# not checked this function once as not using it now
@dashboard_bp.route('/api/dashboard/beta/action', methods = ["POST"])
def dashboard_api_beta_action():
    request = request.data
    data = json.loads(request)
    action = data['action']

    if action == 'create' or action == 'update':
        keyword = data['beta_keyword']
        response = data['beta_response']
        if not keyword or not response or keyword >= stat['KEYWORD_MAX_SIZE'] or response >= stat['RESPONSE_MAX_SIZE']:
            resp = {'status' : False}
            resp = json.dumps(resp)
            return resp
        if action == 'create':
            beta_resp = Beta.query.filter_by(keyword = keyword).first()
            if (beta_resp!=None):
                resp = {'status' : False}
                resp = json.dumps(resp)
                return resp
            beta_elem = Beta(beta_keyword = keyword, beta_response = response)
            db.session.add(beta_elem)
            db.session.commit()
        else:
            beta_id = data['beta_id']
            beta_elem = Beta.query.get(beta_id)
            beta_elem.beta_keyword = keyword
            beta_elem.beta_response = response
    
    elif action == 'delete':
        beta_id = data['beta_id']
        beta_elem = Beta.query.get(beta_id)
        db.session.delete(beta_elem)
        db.session.commit()
    
    else:
        resp = {'status' : False }
        return resp
    resp = {'status' : True}
    resp = json.dumps(resp)
    return resp

@dashboard_bp.route('/api/dashboard/alpha/<string:name>',methods = ['GET'])
def dashboard_api_alpha(name):
    response_data = db.session.query(
                    Responses.response,Responses.response_id,
                    func.group_concat(Questions.question.op("ORDER BY")(Questions.question)).label('questions')
                    ).filter(
                        Questions.response_id == Responses.response_id,
                        Responses.category == name
                    ).group_by(
                        Questions.response_id
                    ).order_by(
                        desc(Responses.response_id)
                    )
    response = []
    for row in response_data:
        temp = {}
        temp['response_id'] = row.response_id
        temp['questions'] = row.questions
        temp['response'] = row.response
        response.append(temp)
    
    response = json.dumps(response)
    return response

@dashboard_bp.route('/api/alpha/update',methods = ['POST'])
def update():
    data = request.data
    data = json.loads(data)

    response_id = data['id']
    message = data['response'].strip()
    keywords = data['keys']

    if not response_id or not message or not keywords:
        error_message = 'Do not leave a field blank'
        response = api_error_handler(error_message)
        return response
    
    if not length_checker(message,keywords):
        error_message = 'Data size exceeds'
        response = api_error_handler(error_message)
        return response

    response_elem = Responses.query.get(response_id)

    questions = db.session.query(Questions.question).filter_by(response_id=response_id).all()

    temp =[]
    for question in questions:
        temp.append(question.question)

    questions = temp

    new_questions = []
    delete_questions = []
    new_keywords =[]
    delete_keywords = []
    tokens =[]

    new_questions = list(set(keywords)-set(questions))
    delete_questions = list(set(questions)-set(keywords))

    for keyword in keywords:
        token = process_raw(keyword)
        for elem in token:
            tokens.append(elem)

    keyword_list = response_elem.keyword_list.split(',')
    new_keywords = list(set(keyword_list)-set(tokens))
    delete_keywords = list(set(tokens)-set(keyword_list))

    for keyword in delete_keywords:
        Keywords.query.filter_by(keyword = keyword, response_id = response_id).delete()

    for question in delete_questions:
        Questions.query.filter_by(question = question, response_id = response_id).delete()

    for keyword in new_keywords:
        keyword_elem = Keywords(keyword = keyword, response_id = response_id)
        db.session.add(keyword_elem)

    for question in new_questions:
        ques_elem = Questions(question = question, response_id = response_id)
        db.session.add(ques_elem)

    keyword_list = ((str(keyword_list).replace("'","")).replace("]","")).replace("[","")
    
    Responses.query.filter_by(response_id = response_id).update({'response':message,'keyword_list':keyword_list})
    db.session.commit()
    
    response = {'status' : True}
    response = json.dumps(response)
    return response

@dashboard_bp.route('/api/alpha/create', methods =['POST'])
def create():
    data = request.data
    data = json.loads(data)

    response = data['response'].strip()
    keywords = data['keywords']
    category = data['category']

    if not response or not keywords:
        error_message = 'Do not leave a field blank'
        response = api_error_handler(error_message)
        return response

    if not length_checker(response,keywords):
        error_message = 'Data size exceeds'
        response = api_error_handler(error_message)
        return response

    list_of_keyowrds = []

    response_elem = Responses(response = response, category = category)
    db.session.add(response_elem)
    db.session.commit()

    response_elem = Responses.query.filter_by(response = response).first()
    response_id = response_elem.response_id

    for keyword in keywords:
        tokens = process_raw(keyword)
        list_of_keyowrds+=tokens

        keyword_elem =Questions(question = keyword, response_id =response_id)
        db.session.add(keyword_elem)

    for keyword in list_of_keyowrds:
        keyword_elem = Keywords(keyword = keyword, response_id = response_id)
        db.session.add(keyword_elem)

    response_elem = Responses.query.filter_by(response_id = response_id).first()
    response_elem.keyword_list = ','.join(list_of_keyowrds)
    db.session.commit()

    response = {'status' : True, 'response_id': response_id}
    response = json.dumps(response)
    return response

@dashboard_bp.route('/api/alpha/delete', methods =['POST'])
def delete():
    data = request.data
    data = json.loads(data)

    response_id = data['id']

    Responses.query.filter_by(response_id=response_id).delete()
    Keywords.query.filter_by(response_id=response_id).delete()
    Questions.query.filter_by(response_id=response_id).delete()
    db.session.commit()
    
    response = {'status' : True}
    response = json.dumps(response)
    return response

@dashboard_bp.route('/api/dashboard/category/<string:name>', methods =['GET','POST'])
def category(name):
    if name == 'list':
        alpha_res = db.session.query(
                        Responses.category.distinct().label('category')
                        ).order_by(Responses.category).all()
        alpha_list = [{'category':'main'}]
        temp={}
        #temp['category'] = 'main'
        #alpha_list.append(temp)
        for i in alpha_res:
            #temp = {}
            if i.category != 'main':
                temp['category'] = i.category
                alpha_list.append(temp)

        response = json.dumps(alpha_list)

    elif name == 'action':
        data = request.data
        data = json.loads(data)

        action = data['action'].lower()
        category = data['category-name'].lower()
        
        response = db.session.query(Responses.response_id).filter_by(category=category).first()
        
        if (response == None and action == 'delete') or (response !=None and action == 'create') or category == 'main':
            response = {'data':False}
            response = json.dumps(response)
            return response

        if action=='delete':
            db.session.query(Keywords).filter(Keywords.response_id==Responses.response_id,Responses.category==category).delete(synchronize_session='fetch')
            db.session.query(Questions).filter(Questions.response_id==Responses.response_id,Responses.category==category).delete(synchronize_session='fetch')
            db.session.query(Responses).filter(Responses.category==category).delete(synchronize_session='fetch')
            db.session.commit()
        
        elif action=='create':
            category_elem = Responses(category = category)
            db.session.add(category_elem)
            db.session.commit()

        response = {'data':True}
        response = json.dumps(response)

    return response


"""error handling of dashboard"""

@dashboard_bp.app_errorhandler(500)
def servor_error(e):
    error_code = '500 : Server Error'
    return render_template('error.html',error_code = error_code)

@dashboard_bp.app_errorhandler(404)
def page_not_found(e):
    error_code = '404 : Page Not Found'
    return render_template('error.html',error_code = error_code)

@dashboard_bp.app_errorhandler(405)
def method_not_allowed(e):
    error_code = '405 : Method Not Allowed'
    return render_template('error.html',error_code = error_code)