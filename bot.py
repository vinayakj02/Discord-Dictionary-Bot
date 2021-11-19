import discord
from discord import embeds
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import requests
import random
import openai
import os
import sys

giphy_api_key = 'xxxxxxxxxxxxxxxxxxxxxxx' #giphy api key

#dictionary class to parse the json output from API
gpt3 = bool(sys.argv[1]=="True")

def question(q):
    if not gpt3:
        return "Can't answer Q&A s now , try the other functions ! \ntype !help for other commands"
    try:
        openai.api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        response = openai.Completion.create(
        engine="davinci",
        prompt=f"Q: {q}\nA:",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["###"]
        )

        resp = str(response["choices"])
        resp = resp.split("\"text\":")[-1].split("\"")[1]
        if "\\" in resp:
            return resp.split("\\")[0]
        return resp
    except:
        return "Failed"

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

class dictionary:
    def __init__(self,word):
        try:
            self.jsonText = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()

            self.wordList = self.jsonText[0]['meanings']
            self.wordNum = random.randint(0,len(self.wordList)-1)
        except:
            self.jsonText = None
            print('Not Found')

    def getPhonetic(self):
        try :
            return self.jsonText[0]['phonetic']
        except:
            return 'Word Not Found'

    def getOrigin(self):
        try:
            return self.jsonText[0]['origin']
        except:
            return 'Could not find origin \U0001F914'

    def getDefinition(self):
        try:
            return self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['definition']
        except:
            return 'Word Not Found \U0001F914'


    def getPartofSpeech(self):
        try:
            return self.jsonText[0]['meanings'][self.wordNum]['partOfSpeech']
        except:
            return 'Word Not Found \U0001F914'

    def getSynonyms(self):
        try :
            synoyms = self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['synonyms']
            return f'{synoyms[0]} or {synoyms[1]}'
        except:
            return 'Could not find any synonyms \U0001F914'

    def getExample(self):
        try :
            return self.jsonText[0]['meanings'][self.wordNum]['definitions'][0]['example']
        except:
            return 'Could not find any examples \U0001F914'


client = commands.Bot(command_prefix='!')
client.remove_command('help')

@client.command()
async def statusGPT3(message):
    if gpt3:
        embed = discord.Embed(title="Online")
    else:
        embed = discord.Embed(title="Offline")
    await message.channel.send(embed = embed)


@client.command()
async def ques(message,*args):
    try:
        s = ""
        for e in args:
            s += e + " "
        print(s)
        ans = question(s)
        embed = discord.Embed(title = s,
        description = ans)
        await message.channel.send(embed = embed)
    except:
        print('Failed ques()')
        await message.channel.send("Try again")

@client.command()
async def gif(message,*,arg='Type'):
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key, arg,limit = 5, rating = 'g')
        listOfGifs = list(api_response.data)
        gif = random.choice(listOfGifs)

        await message.send(gif.embed_url)
    except ApiException as e:
        print('Error in gif ')


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
        value='Gives the pronounciation',
        inline=False
    )
    embed.add_field(
        name='!syn <word>',
        value='Synonyms of the word',
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
        name = '!ques',
        value = 'Ask general questions !',
        inline=False
    )

    embed.set_image(url=f'https://media.giphy.com/media/l2Je66zG6mAAZxgqI/giphy.gif')
    # embed.set_image(url = 'https://preview.redd.it/fyuad9psesx21.jpg?width=960&crop=smart&auto=webp&s=d677cbbeaa6df9b6f04503f81e3f4f84ee9e3771')

    await message.channel.send(embed=embed)


@client.command()
async def info(message):
    await message.channel.send(message.guild)
    await message.channel.send(message.author)
    await message.channel.send(message.message.id)

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

@client.command()
async def ran(message):
    arg = getRandomWord()
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
    # await message.send(embed=embed)

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

    # await message.channel.send(embed=embed)

@client.command()
async def define(message,arg='nothing'):
    """
    !define word
    """
    word = dictionary(arg)
    embed = discord.Embed(
        title = f'{arg}',
        description = word.getDefinition()
    )

    await message.channel.send(embed=embed)

@client.command()
async def pos(message,arg='nothing'):
    word = dictionary(arg)
    embed = discord.Embed(
        title = f'{arg}',
        description = word.getPartofSpeech()
    )

    await message.channel.send(embed=embed)

@client.command()
async def example(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getExample()
    )

    await message.channel.send(embed=embed)

@client.command()
async def phonetic(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getPhonetic()
    )

    await message.channel.send(embed=embed)

@client.command()
async def syn(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getSynonyms()
    )

    await message.channel.send(embed=embed)

@client.command()
async def org(message,arg='nothing'):
    word = dictionary(arg)

    embed = discord.Embed(
        title = f'{arg}',
        description = word.getOrigin()
    )

    await message.channel.send(embed=embed)

@client.command()
async def pro(message,arg):

    await message.channel.send(arg,tts=True)


@client.event
async def on_ready():
    print('Bot is Running.')

# @client.event
# async def on_member_join(member):
#     print(f'{member} joined the server')


# @client.event
# async def on_member_remove(member):
#     print('{member} left the server')

client.run('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
