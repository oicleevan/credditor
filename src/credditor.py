import discord
import sys

# token requires input at runtime for security reasons
token = '' 
if(len(sys.argv) >= 2):
    token = sys.argv[1]
else:
    quit()

# will eventually figure out how to put all of this stuff into a separate file. yaml, txt, whatever it is ID ONT KNOW!
negative_triggers = [
    "taiwan",
    "winnie the pooh", "winnie the poo", "winnie",
    "democracy", "america", "capitalism",
    "mao is bad"
]

positive_triggers = [
    "mao",
    "xi jinping",
    "china numba one", "china number one", "china numba 1", "china number 1",
    "pubg", "player unknown",
    "lao gan ma", "bing chilling",
    "john cena"
]

def check_neg_trigger(msg):
    for x in negative_triggers:
        if x in msg: return True

def check_pos_trigger(msg):
    for x in positive_triggers:
        if x in msg: return True

client = discord.Client()

@client.event
async def on_ready():
    print('# Logged on as {0.user}!'.format(client))

@client.event
async def on_message(self, message):
    if message.author == client.user: return
    if str(message.author) == "travis#2799": return # L nerd

    print('Message from {0.author}: {0.content}'.format(message))

    if check_neg_trigger(message.content.lower()) == True:
        await message.reply('-1000000 social credit!! 😭')
        return

    if check_pos_trigger(message.content.lower()) == True:
        await message.reply('+100 social credit!! 👲🤏')
        return

@client.event
async def on_guild_join(self, guild):
    print('# Joined ' + guild.name + '.')

client.run(token)