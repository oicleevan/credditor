import discord
import sys

# token requires input at runtime for security reasons
token = '' 
if(len(sys.argv) >= 2):
    token = sys.argv[1]
else:
    quit()

negative_triggers = [ "taiwan", "winnie the pooh", "winnie the poo", "winnie", "democracy", "mao is bad", "america", "capitalism" ]
def check_neg_trigger(msg):
    for x in negative_triggers:
        if x in msg: return True
    
    return False

positive_triggers = [ "mao", "xi jinping" ]
def check_pos_trigger(msg):
    for x in positive_triggers:
        if x in msg: return True
    
    return False

class MyClient(discord.Client):
    async def on_ready(self):
        print('# Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user: return

        print('Message from {0.author}: {0.content}'.format(message))

        if check_neg_trigger(message.content) == True:
            await message.reply('-1000000 social credit!! 😭')
            return

        if check_pos_trigger(message.content) == True:
            await message.reply('+100 social credit!! 👲🤏')
            return

    async def on_guild_join(self, guild):
        print('# Joined ' + guild.name + '.')

client = MyClient()
client.run(token)