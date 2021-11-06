import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user: return
        
        print('Message from {0.author}: {0.content}'.format(message))

        if "taiwan" in message.content:
            await message.channel.send('-100000000 social credit!!!!')
            return

        if message.content.startswith('-social add'):
            await message.channel.send('+100 social credit')
            return

client = MyClient()
client.run('OTA2MDI0NTY2MzQ4OTc2MTI4.YYSnIQ.Ro5t_ONPYT1uPEO46YcO6qrMQg4')