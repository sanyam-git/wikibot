# Wikibot
A simple, fast and scalable solution for an interactive chatbot.

+ Bot live at  : `@wikibot` on [zulipchat](http://wikimedia.zulipchat.com "zulipchat") 

## Internal Working
#### How the bot thinks ?
The flow schema followed by the bot:
![main_chart](https://user-images.githubusercontent.com/43791665/79746730-173c9c00-8328-11ea-8ef4-44aa0ca0613e.jpg)

#### Scraping the information
The platform uses the following approach to extract useful information from text and provide the best fit response.

![language-algo ](https://user-images.githubusercontent.com/43791665/79746758-21f73100-8328-11ea-9476-f38ef654ae08.jpg)

**Example :**
What are some Python projects I could work on ? 
**extracted keywords** are `['python', 'projects', 'work']`

## Types of Messages
The following commands are processes by the bot :

#### Messages without prefix
+ Can updated from dashboard (**main** category)
	*example :*  `Give me a list of Wikimedia's gsoc projects.`
	
![main](https://user-images.githubusercontent.com/43791665/79764474-0baa9e80-8343-11ea-97b1-537c75fe07eb.png)

+ **Casual Talk** : The bot is pre-programmed to perform casual talk with the users on general topics, such as greetings, activities, likes/dislikes, etc.

#### Messages with prefix (+)
+ **Alpha** Command : Category names and messages can be created and managed through Alpha section on dashboard.
	+ *syntax  :* `+<category_name > <query>`
	+ *example :* `+lang python projects`

![alpha](https://user-images.githubusercontent.com/43791665/79746803-36d3c480-8328-11ea-80e6-8510a3933ca6.png)

+ **Beta** Command : Messages with `+<name>` only. Can be created and managed through beta section on dashboard.
	+ *syntax    :* `+<name >`
	+ *example :* `+timeline`

![beta](https://user-images.githubusercontent.com/43791665/79746822-405d2c80-8328-11ea-919d-200dacda3720.png)


+ **Standard** Command : Inbuilt command in code for predefined actions.
	+ *example :*  `+ help` for help, `+ task  <task_id>` for info about a phab task

![task](https://user-images.githubusercontent.com/43791665/79746875-55d25680-8328-11ea-9cde-a333f0b751fd.png)


### Other Features:
+ Statistics Page : A statistics page on the dashboard to analyse the user-bot interaction.
+ Project Suggestion : suggesting project details (such as project location gerrit/github/phabricator, mentors, workboard etc.) from skills.
+ Find status of tasks assigned/created to/by the user.

## Dashboard
A single page web app to create, update and manage the bot's knowledge base.
+ link : shared with mentors
+ [dashboard images](#file-wikibot-md)
+ [demo video](https://youtu.be/Sv2PZOC_9x8)

![dashboard-main](https://user-images.githubusercontent.com/43791665/79747046-a34ec380-8328-11ea-9aa3-0d3ab5fecb2d.png)
