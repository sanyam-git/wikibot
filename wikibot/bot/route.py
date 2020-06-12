from flask import Blueprint, request

from wikibot.bot.util import get_response, beautify, alpha
from wikibot.database.static import stat

bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/api', methods=['POST'])
def api():
    content = request.get_json()

    # formatting the message
    message = (content['message']['content'])[:stat['MESSAGE_MAX_SIZE']]
    message = (message.strip()).lower()
    
    # checking for + prefix (standard,alpha or beta command)
    if '+' in message:
        index = message.index('+')
        message = message[(index+1):].lstrip()
        response = get_response(message)
    else:
        # if no prefix check main category and then check greetings
        response = alpha('main', message)

    response = beautify(content, response)
    return response
    