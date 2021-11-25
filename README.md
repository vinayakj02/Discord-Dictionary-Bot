# Discord Dictionary Bot - doc 
Doc is a Discord bot with features of a dictionary(and more) that is easy to set up and use !

## Features
* Get the definition of the any word in the english dictionary. 
* Get other details about the word like phonetics and part of speech.
* Get examples in which the word is used.
* Get synonyms and antonyms.
* Get the closest gif of the word .  
* Get to know about the origin of the word. 
* Get the pronunciation to the word.
* Bot can also generate random words. 
* Ask the bot any question ! 

## How to use 
* Invite the bot to the server , using this [link](https://discord.com/api/oauth2/authorize?client_id=910594616502390825&permissions=8&scope=bot).
* Type `!help` after inviting the Bot for more detailed information about the commands. 
* **These are the commands** , 
    * ``!status <word>`` Status of the bot.
    * ``!all <word>``    Gives all the information about the word 
    * ``!define <word>`` Gives the definition of the word
    * ``!phonetic <word>``   Phonetic
    * ``!org <word>``    Origin of the word
    * ``!example <word>``An example of the word
    * ``!pos <word>`` Part of Speech
    * ``!pro <word>`` Gives the pronunciation
    * ``!syn <word>``Synonyms of the word
    * ``!ant <word>``Antonyms of the word
    * ``!gif <word>`` Gif of the word 
    * ``!ques <question>``Ask general questions !
    * ``!ran`` Gives all information about a random word 
    * ``!help`` Help command

## Libraries / API's Used 
* [Dictionary API](https://dictionaryapi.dev/)
* [Giphy's API](https://developers.giphy.com/)
* [OpenAi's API](https://openai.com/) - For Q&A 
* [discord.py](https://discordpy.readthedocs.io/en/stable/)
* [Random Word API](https://random-word-api.herokuapp.com)

## Requirements 
```
pip install discord.py giphy_client openai requests
```

## Demo 
#### Use of the all command
   ![all command](https://github.com/vinayakj02/Discord-Dictionary-Bot/blob/main/imgs/all-command.png)
#### Use of the ques command
![ques command](https://github.com/vinayakj02/Discord-Dictionary-Bot/blob/main/imgs/ques-command.png)
![ques command](https://github.com/vinayakj02/Discord-Dictionary-Bot/blob/main/imgs/ques-command2.png)
#### Use of the define command 
![define command](https://github.com/vinayakj02/Discord-Dictionary-Bot/blob/main/imgs/define-command.png)
