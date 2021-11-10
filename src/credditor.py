import discord
from discord.ext import commands
import sys
from os.path import exists
from configparser import ConfigParser

config = ConfigParser()

def config_setup(file):
    config["APP OPTIONS"] = {
        "prefix": "-social",
        "reply_ping": "false ; please make true or false"
    }

    with open(file, 'w') as conf:
        config.write(conf)

if exists("config.ini") == False:
    print('> Config file does not exist, creating...')
    config_setup('config.ini')
    print('> Config file created.')

def read_config(file):
    config.read(file)
    return config["APP OPTIONS"]
app_options = read_config('config.ini')

prefix = ''
if config.has_option("APP OPTIONS", "prefix"):
    prefix = str(app_options["prefix"])
else:
    prefix = '-social'

# token requires input at runtime for security reasons
token = '' 
if(len(sys.argv) >= 2):
    token = sys.argv[1]
else:
    print('Please include a bot token!')
    quit()

# will eventually figure out how to put all of this stuff into a separate file. yaml, txt, whatever it is ID ONT KNOW!
negative_triggers = [
    "taiwan",
    "winnie the pooh", "winnie the poo", "winnie",
    "democracy", "america", "capitalism",
    "tankman",
    "tiananmen square", "tianenmen square",
    "1989"
]

positive_triggers = [
    "mao",
    "xi jinping",
    "china numba one", "china number one", "china numba 1", "china number 1",
    "pubg", "player unknown",
    "lao gan ma", "bing chilling",
    "john cena",
    "xue hua piao piao",
    "shashumga",
    "ching cheng hanji"
]

def check_neg_trigger(msg):
    for x in negative_triggers:
        if x in msg: return True

def check_pos_trigger(msg):
    for x in positive_triggers:
        if x in msg: return True

client = commands.Bot(command_prefix=prefix + ' ')

@client.event
async def on_ready():
    print('# Logged on as {0.user}!'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: return
    if str(message.author) == "travis#2799": return # L nerd

    print('Message from {0.author}: {0.content}'.format(message))

    msg = message.content.lower()

    if check_neg_trigger(msg) == True:
        print(f'\t {str(message.author)} triggered negative social credit!')
        if app_options["reply_ping"] == "false":
            await message.reply('-1000000 social credit!! 😭', mention_author=False)
        else:
            await message.reply('-1000000 social credit!! 😭')

    if check_pos_trigger(msg) == True:
        print('\t' + str(message.author) + ' triggered positive social credit!')
        if app_options["reply_ping"] == "false":
            await message.reply('+100 social credit!! 👲🤏', mention_author=False)
        else:
            await message.reply('+100 social credit!! 👲🤏')

    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    print('# Joined ' + guild.name + '.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(token)