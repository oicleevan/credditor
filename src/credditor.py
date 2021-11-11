import discord
from discord.ext import commands
import sys
from os.path import exists
from configparser import ConfigParser

config = ConfigParser()

def config_setup(file):
    config["APP OPTIONS"] = {
        "prefix": "-social",
        "reply_ping": "false"
    }

    with open(file, 'w') as conf:
        config.write(conf)

if exists("conf/config.ini") == False:
    print('> Config file does not exist, creating...')
    config_setup('conf/config.ini')
    print('> Config file created.')

def read_config(file):
    config.read(file)
    return config["APP OPTIONS"]
app_options = read_config('conf/config.ini')

prefix = ''
if config.has_option("APP OPTIONS", "prefix"):
    prefix = str(app_options["prefix"])
else:
    prefix = '!'

# token requires input at runtime for security reasons
token = '' 
if(len(sys.argv) >= 2):
    token = sys.argv[1]
else:
    print('Please include a bot token!')
    quit()
 
negative_triggers = []
def set_neg_trig(file):
    f = open(file, 'r+')
    f_line = f.readlines()
    
    for x in f_line:
        negative_triggers.append(x.strip())

if exists('conf/negative_trig.txt') == True:
    print('> Found negative_trig file.')
    set_neg_trig('conf/negative_trig.txt')
else:
    print('Please create a text file `conf/negative_trig.txt` and include negative social credit triggers.')
    quit()

positive_triggers = []
def set_neg_trig(file):
    f = open(file, 'r+')
    f_line = f.readlines()
    
    for x in f_line:
        positive_triggers.append(x.strip())

if exists('conf/positive_trig.txt') == True:
    print('> Found positive_trig file.')
    set_neg_trig('conf/positive_trig.txt')
else:
    print('Please create a text file `conf/positive_trig.txt` and include positive social credit triggers.')
    quit()

def check_neg_trigger(msg):
    for x in negative_triggers:
        if x in msg: return True

def check_pos_trigger(msg):
    for x in positive_triggers:
        if x in msg: return True

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print('\n# Logged on as {0.user}!\n'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: return
    if str(message.author) == "travis#2799": return # L nerd

    print('Message from {0.author}: {0.content}'.format(message))

    msg = message.content.lower()

    if check_neg_trigger(msg) == True:
        print(f'# {str(message.author)} triggered negative social credit!')
        if app_options["reply_ping"] == "false":
            await message.reply('-1000000 social credit!! 😭', mention_author=False)
        else:
            await message.reply('-1000000 social credit!! 😭')

    if check_pos_trigger(msg) == True:
        print(f'# f{str(message.author)} triggered positive social credit!')
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
    await ctx.reply(f'Pong! {round(client.latency * 1000)}ms')

client.run(token)
