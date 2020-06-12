import time
import requests
import json
import random

payload = {
  "data": "my name's sanyam@jain is sam asea",
  "message": {
    "id": 191404088,
    "sender_id": 254216,
    "content": "+ task 231751",
    "recipient_id": 433815,
    "timestamp": 1584894647,
    "client": "website",
    "subject": "",
    "topic_links": [],
    "rendered_content": "<p>Hi</p>",
    "is_me_message": False,
    "reactions": [],
    "submessages": [],
    "sender_full_name": "sanyam",
    "sender_short_name": "sanyam.inbox",
    "sender_email": "sanyam.inbox@gmail.com",
    "sender_realm_str": "wikimedia",
    "display_recipient": [
      {
        "email": "sanyam.inbox@gmail.com",
        "full_name": "sanyam",
        "short_name": "sanyam.inbox",
        "id": 254216,
        "is_mirror_dummy": False
      },
      {
        "id": 274271,
        "email": "wikibot-bot@zulipchat.com",
        "full_name": "wikibot",
        "short_name": "wikibot-bot",
        "is_mirror_dummy": False
      }
    ],
    "type": "private",
    "avatar_url": "https://secure.gravatar.com/avatar/d8f78109444fc5ec90ca174923b580c9?d=identicon&version=1",
    "content_type": "text/x-markdown"
  },
  "bot_email": "wikibot-bot@zulipchat.com",
  "token": "v3BmJRGVB4Ec6pTOTi5gEqghSZKWQ275",
  "trigger": "private_message"
}

url = 'http://127.0.0.1:5000/api'
temp = 'This is the default message'
while True:
  message = input('you : ')
  if message == 'quit' or message == 'q':
    print('User exited with quit')
    break
  if message == '':
    message = temp

  temp = message

  payload['message']['id'] = random.randrange(100000000,999999999,1)
  payload['message']['content'] = message
  headers = {'content-type': 'application/json'}
  start = time.time()
  response = requests.post(url, data=json.dumps(payload), headers=headers)
  end = time.time()
  time_required = end-start
  print('wikibot : '+response.text+'\n(message fetched in '+str(time_required)+' seconds)')

