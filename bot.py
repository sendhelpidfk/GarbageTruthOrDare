from turtle import color
import discord
from discord import Color
from discord.ext import commands
import random
import os
from datetime import datetime

debugon = True
bot = commands.Bot(command_prefix='td')

#file definitions
if True:
    basefolder = os.getcwd() + "\\base\\"
    truthsfolder = os.getcwd() + "\\truths\\"
    darefolder = os.getcwd() + "\\dares\\"

    selfpath = os.getcwd() + "\\bot.py"
    botkeypath = basefolder + "botkey.txt"
    configpath = basefolder + "config.txt"
    helppath = basefolder + "help.txt"
    logpath = basefolder + "logs.txt"
    truthpath = truthsfolder + "truths.txt"
    darepath = darefolder + "dares.txt"
    suggestionpath = truthsfolder + "truthsuggestions.txt"

#Load bot key from file
keyfile = open(botkeypath, "r")
botkey = keyfile.read()
keyfile.close()

workdir = os.getcwd()

client = discord.Client()

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#
# Generic Functions
#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=

def debugsend(message):
    if debugon:
        print(message)
    return debugon
    
def logmessage(message):
    log = open(logpath,"a")
    log.write("[" + str(datetime.now(tz=None)) + "] #" + str(str(message.channel).encode("utf-8")) + " (" + str(str(message.guild).encode("utf-8")) + "): " + str(str(message.content).encode("utf-8")) + "\n")
    log.close
    return True

def loggeneric(message):
    log = open(logpath,"a")
    log.write("[" + str(datetime.now(tz=None)) + "] (internal log): " + str(str(message).encode("utf-8")) + "\n")
    log.close
    return True

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#
# truth or dare Functions
#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=

def fetchtruths(specials):
    loggeneric("Executing fetchtruths(" + str(specials) + ")")
    #no specials, do a normal read - for use with special case of truthening the bot itself
    truthsfile = open(truthpath, "r")
    truths1 = truthsfile.read()
    truths1 = truths1.split("\n")
    truthsfile.close()
    return truths1

def fetchdares(specials):
    loggeneric("Executing fetchdares(" + str(specials) + ")")
    #no specials, do a normal read - for use with special case of dareening the bot itself
    daresfile = open(darepath, "r")
    dares1 = daresfile.read()
    dares1 = dares1.split("\n")
    daresfile.close()
    return dares1

def generateembed(title, color, description):
    return discord.Embed(title = title, description = description, color = color)

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#
# Discord API Functions
#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=

@bot.command
async def help(ctx): #help command
    #refresh help message in memory
    helpmsgfile = open(helppath,"r")
    helpmessage = helpmsgfile.read()
    helpmsgfile.close()
    #send help message
    await ctx.send(helpmessage)
    await ctx.send("_Sent using new command system._")

@client.event
async def on_message(message):

    if message.content == 'tdtruth':
        truths = fetchtruths(True)
        truthcount = len(truths)
        specifictruth = random.randint(0,len(truths)-1)
        embed = generateembed('Truth %i/%i' % (specifictruth + 1, truthcount), 0x008888, truths[specifictruth])

        await message.channel.send(embed = embed)

    elif message.content == 'tddare':
        dares = fetchdares(True)
        darecount = len(dares)
        specificdare = random.randint(0,len(dares)-1)
        embed = generateembed('Dare %i/%i' % (specificdare + 1, darecount), 0xff0000, dares[specificdare])

        await message.channel.send(embed = embed)

@client.event
async def on_connect():
    print("[" + str(datetime.now(tz=None)) + "] Connection to Discord established, bot booting...")

@client.event
async def on_ready():
    print("[" + str(datetime.now(tz=None)) + '] Bot online as {0.user}'.format(client))
    game = discord.Game("tdhelp")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_disconnect():
    print("[" + str(datetime.now(tz=None)) + "] Connection lost, reconnecting when able...")     

client.run(str(botkey))