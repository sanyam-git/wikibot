import json

from wikibot import db
from wikibot.database.models import Greet,GreetKeywords,Messages,Users,Responses,Questions,Keywords,Beta
from wikibot.database.static import stat

# checking max length
def length_checker(response,keywords):
    flag = False
    response_len = len(response)
    if response_len < stat['RESPONSE_MAX_SIZE']:
        flag = True
        for keyword in keywords:
            if len(keyword) >= stat['QUESTION_MAX_SIZE']:
                flag = False
                break
    return flag

def api_error_handler(error_message):
    response = {}
    response['status'] = False
    response['alert_message'] = error_message
    response = json.dumps(response)
    return response