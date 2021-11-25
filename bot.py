import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import requests
import random
import openai

giphy_api_key = 'xxxxxxxxxxxxxxxxxxxxxxx' #giphy api key ( Not the actual key )

gpt3 = True #Set this to False if you don't want Q&A . 

# Calls the OpenAI API and gets a response for the given input text
def question(q):
    if not gpt3:
        return "Can't answer Q&A s now , try the other functions ! \ntype !help for other commands"
    try:
        openai.api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Not the actual key 

        response = openai.Completion.create(
    engine="davinci",
    prompt=f"Human: {q} \nAI:",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"]
    )

        return str(response["choices"][0]["text"])

    except:
        return "Failed"

# Calls the random-word-api and gets a random word 
def getRandomWord():
    try:
        listOfRandomWords =  list(requests.get('https://random-word-api.herokuapp.com/word?number=50&swear=0').json())
        for w in listOfRandomWords:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{w}').json()
            if 'title' in response:
                continue
            else:
                return w
    except:
        return 'spacetime'

#dictionary class to parse the json output from the free dictionary API
class dictionary:
    # Constructor containing the word to be searched
    def __init__(self,word):
        try:
            self.jsonText = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()

            self.wordList = self.jsonText[0]['meanings']
            self.wordNum = random.randint(0,len(self.wordList)-1)
        except:
            self.jsonText = None
            print('Not Found')

    # Returns the phonetic spelling of the word
    def getPhonetic(self):
        try :
            return self.jsonText[0]['phonetic']
        except:
            return 'Word Not Found'

    # Returns the word's origin
    def getOrigin(self):
        try:
            return self.jsonText[0]['origin']
        except:
            return 'Could not find origin \U0001F914'

    # Returns the word's definition 
    def getDefinition(self):
        try:
            return self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['definition']
        except:
            return 'Word Not Found \U0001F914'

    # Returns the word's part of Speech
    def getPartofSpeech(self):
        try:
            return self.jsonText[0]['meanings'][self.wordNum]['partOfSpeech']
        except:
            return 'Word Not Found \U0001F914'

    # Returns the word's Synonyms 
    def getSynonyms(self):
        try : 
            synoyms = self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['synonyms']
            return f'{" , ".join(synoyms)}'
        except:
            return 'Could not find any synonyms \U0001F914'
    # Returns the word's Antonyms
    def getAntonyms(self):
        try : 
            antonyms = self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['antonyms']
            return f'{" , ".join(antonyms)}'
        except:
            return 'Could not find any antonyms \U0001F914'

    # Returns Examples of the word
    def getExample(self):
        try :
            return self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['example']
        except:
            return 'Could not find any examples \U0001F914'


# setting the bot's prefix to ! 
client = commands.Bot(command_prefix='!')

# removing the default help command ( because I've made a custom one )
client.remove_command('help')

# Tells us if the Q&A is enabled or not
@client.command()
async def statusGPT3(message):
    if gpt3:
        embed = discord.Embed(title="Online")
    else:
        embed = discord.Embed(title="Offline")
    await message.channel.send(embed = embed)


# Calls the Question() function and returns the response
@client.command()
async def ques(message,*args):
    try:
        s = ""
        for e in args:
            s += e + " "
        ans = question(s)
        embed = discord.Embed(title = s,
        description = ans)
        await message.channel.send(embed = embed)
    except:
        print('Failed ques()')
        await message.channel.send("Try again")

# Returns a gif of the word passed in (default = Type) using the Giphy API
@client.command()
async def gif(message,*,arg='Type'):
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key, arg,limit = 5, rating = 'g')
        # getting a random gif from the response 
        listOfGifs = list(api_response.data)
        gif = random.choice(listOfGifs)

        await message.send(gif.embed_url)
    except ApiException as e:
        print('Error in gif ')


# Custom !help command
@client.command()
async def help(message):

    embed = discord.Embed(
        title = 'Bot Commands',
        description='Welcome to the help section. Here are all the commands for this dictionary ! '
    )
    # embed.set_thumbnail(url='https://preview.redd.it/fyuad9psesx21.jpg?width=960&crop=smart&auto=webp&s=d677cbbeaa6df9b6f04503f81e3f4f84ee9e3771')
    embed.add_field(
        name='!all <word>',
        value='Gives all the information about the word',
        inline=False
    )
    embed.add_field(
        name='!define <word>',
        value='Gives the definition of the word',
        inline=False
    )
    embed.add_field(
        name='!phonetic <word>',
        value='Phonetic',
        inline=False
    )
    embed.add_field(
        name='!org <word>',
        value='Origin of the word',
        inline=False
    )
    embed.add_field(
        name='!example <word>',
        value='An example of the word',
        inline=False
    )
    embed.add_field(
        name='!pos <word>',
        value='Part of Speech',
        inline=False
    )
    embed.add_field(
        name='!pro <word>',
        value='Gives the pronunciation',
        inline=False
    )
    embed.add_field(
        name='!syn <word>',
        value='Synonyms of the word',
        inline=False
    )
    embed.add_field(
        name='!ant <word>',
        value='Antonyms of the word',
        inline=False
    )
    embed.add_field(
        name='!gif <word>',
        value='Gif',
        inline=False
    )
    embed.add_field(
        name='!status <word>',
        value='Status of the bot ',
        inline=False
    )
    embed.add_field(
        name='!ran',
        value='Generates a random word',
        inline=False
    )
    embed.add_field(
        name = '!ques <question>',
        value = 'Ask general questions !',
        inline=False
    )
    embed.set_image(url=f'https://media.giphy.com/media/l2Je66zG6mAAZxgqI/giphy.gif')
    # embed.set_image(url = 'https://preview.redd.it/fyuad9psesx21.jpg?width=960&crop=smart&auto=webp&s=d677cbbeaa6df9b6f04503f81e3f4f84ee9e3771')

    await message.channel.send(embed=embed)


# Returns the info the guild and author 
@client.command()
async def info(message):
    await message.channel.send(message.guild)
    await message.channel.send(message.author)

# Returns "Online" and a gif if the bot is online on '!status' command 
@client.command()
async def status(message):
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key,'online',limit = 5, rating = 'g')
        listOfGifs = list(api_response.data)
        gif = random.choice(listOfGifs)

        embed = discord.Embed(title ='Online')
        embed.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')

        await message.channel.send(embed = embed)
    except ApiException as e:
        print('Error in gif ')

# Returns all the information about a random word by calling the getRandomWord() function on '!ran <word>' command
@client.command()
async def ran(message):
    arg2 = getRandomWord()
    
    wordR = dictionary(arg2)

    embed = discord.Embed(title = arg2,
    description = wordR.getDefinition())

    embed.add_field(
        name='Phonetic',
        value=wordR.getPhonetic(),
        inline=False
    )
    embed.add_field(
        name='Origin',
        value=wordR.getOrigin(),
        inline=False
    )
    embed.add_field(
        name='Synonyms',
        value=wordR.getSynonyms(),
        inline=False
    )
    embed.add_field(
        name='Antonyms',
        value=wordR.getAntonyms(),
        inline=False
    )
    embed.add_field(
        name='Example',
        value=wordR.getExample(),
        inline=False
    )
    embed.add_field(
        name='Part of Speech',
        value=wordR.getPartofSpeech(),
        inline=False
    )
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key,arg2,limit = 5, rating = 'g')
        listOfGifs = list(api_response.data)
        gif = random.choice(listOfGifs)
        embed.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')

    except ApiException as e:
        print('Error in gif ')
    
    await message.channel.send(embed = embed)

# Returns all the definitions of the word (default = "nothing") on '!all <word>' command
@client.command()
async def all(message, arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description=f'{word.getDefinition()}'
    )
    embed.add_field(
        name='Phonetic',
        value=word.getPhonetic(),
        inline=False
    )
    embed.add_field(
        name='Origin',
        value=word.getOrigin(),
        inline=False
    )
    embed.add_field(
        name='Part Of Speech',
        value=word.getPartofSpeech(),
        inline=False
    )
    embed.add_field(
        name = 'Synonyms',
        value=word.getSynonyms(),
        inline= False
    )
    embed.add_field(
        name = 'Antonyms',
        value=word.getAntonyms(),
        inline= False
    )
    embed.add_field(
        name='Example',
        value=word.getExample(),
        inline=False
    )
    api_instance = giphy_client.DefaultApi()
    desc = word.getDefinition()
    if ',' in desc:
        try:
            api_response = api_instance.gifs_search_get(giphy_api_key,desc.split(',')[0],limit = 5, rating = 'g')
            listOfGifs = list(api_response.data)
            gif = random.choice(listOfGifs)

            embed.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')
            await message.send(embed = embed)
        except ApiException as e:
            print('Error in gif ')
    else:
        try:
            api_response = api_instance.gifs_search_get(giphy_api_key,arg,limit = 5, rating = 'g')
            listOfGifs = list(api_response.data)
            gif = random.choice(listOfGifs)

            embed.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')
            await message.send(embed = embed)
        except ApiException as e:
            print('Error in gif ')


# Returns the definition of the word (default = "nothing") on '!def <word>' command 
@client.command()
async def define(message,arg='nothing'):
    
    word = dictionary(arg)
    embed = discord.Embed(
        title = f'{arg}',
        description = word.getDefinition()
    )

    await message.channel.send(embed=embed)

# Returns the part of speech of the word (default = "nothing") on '!pos <word>' command . 
@client.command()
async def pos(message,arg='nothing'):
    word = dictionary(arg)
    embed = discord.Embed(
        title = f'{arg}',
        description = word.getPartofSpeech()
    )

    await message.channel.send(embed=embed)


# Gives an example of the word (default = "nothing") on '!example <word>' command
@client.command()
async def example(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getExample()
    )

    await message.channel.send(embed=embed)

# Gives the phonetic of the word (default = "nothing") on '!phonetic <word>' command
@client.command()
async def phonetic(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getPhonetic()
    )

    await message.channel.send(embed=embed)

# Gvies the synonyms of the word (default = "nothing") on '!synonyms <word>' command
@client.command()
async def syn(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getSynonyms()
    )

    await message.channel.send(embed=embed)

# Gives the antonyms of the word (default = "nothing") on '!ant <word>' command
@client.command()
async def ant(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getAntonyms()
    )

    await message.channel.send(embed=embed)    
# Gives the origin of the word (default = "nothing") on '!origin <word>' command
@client.command()
async def org(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getOrigin()
    )

    await message.channel.send(embed=embed)

# Gives the pronunciation the word on '!pro <word>' command
@client.command()
async def pro(message,arg):

    await message.channel.send(arg,tts=True)

# To check if bot is running in terminal 
@client.event
async def on_ready():
    print('Bot is Running.')

# To run the bot
client.run('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') # Not the actual token 
