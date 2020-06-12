import json
import re
from random import choice

from wikibot import db
from wikibot.database.models import Greet,GreetKeywords,Messages,Users,Responses,Questions,Keywords,Beta
from wikibot.database.static import stat,LIST,STOP_WORDS,STANDARD_COMMANDS

def get_response(message):
    command_word = message.split()[0]
    message = message[len(command_word):].lstrip()

    # checking for STANDARD commands (ex. +help etc.)
    if command_word in STANDARD_COMMANDS:
        response = standard_command(command_word, message)
        return response

    # checking for alpha command
    alpha_res = db.session.query(Responses.response_id).filter_by(category=command_word).first()
    if alpha_res != None:
        response = alpha(command_word, message)
        return response

    #checking for beta command
    beta_res = db.session.query(Beta.beta_response).filter_by(beta_keyword=command_word).first()
    if beta_res != None:
        response = beta_res.beta_response
        return response
    
    # if no such command exist
    response = stat['DEFAULT_COMMAND_RESPONSE']
    return response


def standard_command(command_word,message):
    # can add as much commands as you want
    # just update the STANDARD command list in static.py
    if command_word == 'help':
        response = stat['HELP_RESPONSE']
    elif command_word == 'task':
        response = task_command(message)
    return response

# for alpha type commands +<command> <something>
def alpha(category, message):
    # checking for exact match with any keyword
    resp = db.session.query(Responses.response
        ).join(Questions, Responses.response_id == Questions.response_id
        ).filter(Responses.category==category, Questions.question==message
        ).first()

    if resp != None:
        response = resp.response
        return response

    tokens = process_raw(message)

    response_id_list = [0]
    key_list = []
    flag = 0
    temp = {}

    for token in tokens:

        keywords = db.session.query(
                Keywords.response_id.distinct().label('response_id'), Responses.keyword_list
                ).filter(
                    Keywords.keyword == token,
                    Responses.category == category,
                    Keywords.response_id not in response_id_list,
                    Responses.response_id == Keywords.response_id
                ).all()

        if keywords != None:
            flag = 1
            for keyword in keywords:
                response_id_list.append(keyword.response_id)
                temp['key'] = keyword.keyword_list
                temp['id'] = keyword.response_id
                key_list.append(temp)

    if flag:
        # now doing scoring - scoring function
        max_score = 0
        response = get_default()
        key = ''

        for item in key_list:
            keyword_list = item['key'].split(',')
            score = 0
            for token in tokens:
                for keyword in keyword_list:
                    if token == keyword:
                        score += 1
                        break
            # add/remove break statement here if you want to prevent DUPLICATE entries
            if score > max_score:
                max_score = score
                key = item['id']
        if max_score > 0:
            response = (Responses.query.get(key)).response
        else:
            response = get_default()
    else:
        response = get_default()

    if category == 'main' and response in LIST:
        response = greetings(message,tokens)

    return response

def process_raw(raw_message):
    # removing punctuation with whitespace
    message = remove_punct(raw_message)
    # removing multiple white spaces
    message = (re.sub(' +', ' ',message)).strip()
    # tokenization
    tokens = message.split(' ')

    # removing STOP_WORDS
    token_delete = []
    length = len(STOP_WORDS)-1
    for token in tokens:
        index = binarysearch(STOP_WORDS,0,length,token)
        if index != -1:
            token_delete.append(token)
    for token in token_delete:
        tokens.remove(token)
    
    # lemmenizing 
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for i in tokens:
        temp = lemmatizer.lemmatize(i)
        lemmatized_words.append(temp)
    """
    return tokens

def save_to_db(content, response):
    # saving every message to database
    message = Messages(message_id = content['message']['id'], 
                    message_body = (content['message']['content'])[:stat['MESSAGE_MAX_SIZE']] ,
                    sender_id = content['message']['sender_id'], response_body = response)
    db.session.add(message)
    db.session.commit()

def task_command(message):
    # maniphest.info (PHAB API)
    # get info about any task on phabricator, using PHAB API
    response = ''
    try:
        # adding try except as the re statemnt or the post request can give error
        task_id = int(re.search(r'\d+', message).group())
        
        data = {}
        data['api.token'] = stat['PHAB_API_TOKEN']
        data['task_id'] = task_id
        response = requests.post('https://phabricator.wikimedia.org/api/maniphest.info', data=data)
        response = (response.json())['result']
        
        title = response['title']
        status = response['status']
        url = response['uri']
        owner_phid = response['ownerPHID']
        
        data = {}
        data['api.token'] = PHAB_API_TOKEN
        data['names[0]'] = owner_phid
        response = requests.post('https://phabricator.wikimedia.org/api/phid.lookup', data=data)
        response = (response.json())['result'][owner_phid]
        
        owner_name = response['name']
        owner_url = response['uri']
        
        response = '**Title** : ['+title+']('+url+')    ,\
                    **Status** : '+status+'   ,\
                    **Assigned To** : [' +owner_name+']('+owner_url+')'
    except:
        response = stat['DEFAULT_TASK_RESPONSE']
    return response

def greetings(message, tokens):
    # greeting message
    message = message.replace('.',' ')
    message = message.replace('?',' ')
    message = message.replace('!',' ')
    message = message.strip()
    message = Greet.query.get(message)
    if message == None:
        response = keyword_greeting(tokens)
    else:
        response = message.greet_answer
    return response

def keyword_greeting(tokens):
    response_id_list = [0]
    key_list = []
    flag = 0
    temp = {}

    for token in tokens:
        keywords = db.session.query(
                GreetKeywords.greet_id.distinct().label('greet_id'), Greet.greet_list
                ).filter(
                    GreetKeywords.greet_keyword == token,
                    GreetKeywords.greet_id not in response_id_list,
                    Greet.greet_id == GreetKeywords.greet_id
                ).all()

        if keywords != None:
            flag = 1
            for keyword in keywords:
                response_id_list.append(keyword.greet_id)
                temp['key'] = keyword.greet_list
                temp['id'] = keyword.greet_id
                key_list.append(temp)
    if flag:
        # now doing scoring
        max_score = 0
        response = get_default()
        key = []
        score_array =[]

        for item in key_list:
            keyword_list = item['key']
            keyword_list = keyword_list.split(',')
            score = 0
            for token in tokens:
                for keyword in keyword_list:
                    if token == keyword:
                        score += 1
                        break
            # add/remove break statement here if you want to prevent DUPLICATE entries
            key.append(item['id'])
            score_array.append(score)
            if score > max_score:
                max_score = score
        if max_score > 0:
            max_score_array = []
            elem=0
            for item in score_array:
                if item == max_score:
                    max_score_array.append(key[elem])
                elem+=1
            key = choice(max_score_array)
        else:
            key = 99999999999
        response = Greet.query.get(key)
        if max_score > 0 and response != None:
            response = response.greet_answer
        else:
            response = get_default()
    else:
        response = get_default()
    return response

def get_default():
    # random default response
    response = choice(LIST)
    return response

def beautify(content, response):
    
    # user WELCOME if user coming first time
    user_id = content['message']['sender_id']
    user = Users.query.get(user_id)
    if user == None:
        user_name = content['message']['sender_full_name']
        user_email = content['message']['sender_email']
        u = Users(user_id = user_id, user_name = user_name, user_email = user_email)
        db.session.add(u)
        db.session.commit()
        response = stat['WELCOME_RESPONSE'] + response

    # if user messages in group
    if content['message']['type'] != 'private':
        response = response + stat['GROUP_RESPONSE']

    # substituing {name} with name
    if '{name}' in response:
        name = content['message']['sender_full_name']
        response = response.replace('{name}',name)  

    response = response.strip()
    save_to_db(content, response)
    response = {'content':response}
    response = json.dumps(response)
    return response


def remove_punct(string): 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x,' ') 
    return string

def binarysearch(arr, l, r, x): 
    if r >= l: 
        mid = l + (r - l)//2
        if arr[mid] == x: 
            return mid 
        elif arr[mid] > x: 
            return binarysearch(arr, l, mid-1, x) 
        else: 
            return binarysearch(arr, mid+1, r, x) 
    else:
        return -1