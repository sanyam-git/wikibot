stat = {}
# saving variables here temporarily
stat['PHAB_API_TOKEN'] = 'api-qiuvdui2y7ckael4jvc3q6oejh3j'
stat['MESSAGE_MAX_SIZE'] = 1000

stat['RESPONSE_MAX_SIZE'] = 10000
stat['KEYWORD_LIST_MAX_SIZE'] = 10000
stat['QUESTION_MAX_SIZE'] = 1000
stat['KEYWORD_MAX_SIZE'] = 100
stat['CATEGORY_MAX_SIZE'] = 100

stat['DEFAULT_COMMAND_RESPONSE'] = 'This is not a valid command. Please type +help for more info.'
stat['DEFAULT_TASK_RESPONSE'] = 'There is no task with such ID. Please check again.'

stat['GROUP_RESPONSE'] = '(You can also PM me at @**wikibot** :) )'
stat['WELCOME_RESPONSE'] = 'Welcome {name}! (here we will add a brief but effective message on how to start the journey).'
stat['HELP_RESPONSE'] = 'Here we will provide brief info about how to use bot ?, basic commands \
                  and link to extended bot documentation'

# add any more commands here
STANDARD_COMMANDS = ['task','help']

LIST = [
"I don't know everything, maybe you should try Wikipedia. Its awesome !",
"If you don't get a satisfying reply, you can always ask in the group chat",
"I am learning new things everyday. Maybe you can suggest on my github",
"I didn't get it. Use +help for more info",
"Use +help to know more",
"Use +help to know more",
"Everyday we learn new things, Maybe you can suggest on my github",
"Use +help to know more",
"Use +help to know more",
"Use +help to know more",
"We can start again. For more info +help",
"I am improving day by day, Use +help for more"
]

# if you filter here remember to filter in greetkeywords.py and file which fed data to database

STOP_WORDS = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone',
'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amount', 'an', 'and', 'another', 'any',
'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'b', 'back', 'be', 'became',
'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside',
'besides', 'between', 'beyond', 'both', 'but', 'by', 'c', 'call', 'can', 'cannot', 'cant', 'could', "couldn't", 
'couldnt', 'd', 'describe', 'detail', "didn't", 'do','doesn','doing', "don't", 'done','don','down', 'due', 'during', 'e',
'each', 'eg', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone',
'everything', 'everywhere', 'except', 'f', 'few', 'fifteen', 'fill', 'find', 'first', 'five', 'for', 'former', 
'formerly', 'found', 'four', 'from', 'front', 'full', 'further', 'g','get', 'give', 'go', 'h', 'had', 
'has', 'hasnt', 'have','having','he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 
'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i','ie', 'if', 'in', 'indeed', 'interest', 
'into', 'is', 'it', 'its', 'itself', 'j', 'k', 'keep','know','l', 'last', 'latter', 'latterly', 'least', 'less', 'm',
'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mine', 'more', 'moreover', 'most', 'mostly', 'move',
'much', 'must', 'my', 'myself', 'n', 'neither', 'never', 'nevertheless', 'next', 'nine', 
'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'o', 'of', 'off', 'often', 
'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 
'out', 'over', 'own', 'p', 'part', 'per', 'perhaps', 'please', 'put', 'q', 'r', 'rather', 're', 's','same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', "shouldn't", 'show',
'side', 'since', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
'still', 'such', 'system', 't', 'take','tell','ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then',
'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'this', 'those',
'though', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'u', 'un', 
'under', 'until', 'up', 'upon', 'us', 'v', 'very', 'via', 'w', 'was', "wasn't", 'we','well', 'were', "weren't", 
'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas',
'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole',
'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'x', 'y', 'yet', 'you', 'your', 'yours',
'yourself', 'yourselves', 'z']
