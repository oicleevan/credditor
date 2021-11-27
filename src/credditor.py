import discord
from discord.ext import commands
import sys, re
import mysql.connector
from os.path import exists
from configparser import ConfigParser

# Database configuration 
db = mysql.connector.connect(
  host="192.168.0.20",
  user="root",
  password="",
  database="china"
)
db_cursor = db.cursor(buffered=True)

# Config file setup
config = ConfigParser()
def config_setup(file):
    config["APP OPTIONS"] = {
        "prefix": "-"
    }

    with open(file, 'w') as conf:
        config.write(conf)

if exists("config.ini") == False:
    print('> Config file \'config.ini\' does not exist, creating...')
    config_setup('config.ini')
    print('> Config file \'config.ini\' created.')
else:
    print('> Config file found.')

def read_config(file):
    config.read(file)
    return config["APP OPTIONS"]
app_options = read_config('config.ini')

prefix = ''
if config.has_option("APP OPTIONS", "prefix"):
    prefix = str(app_options["prefix"])
else:
    prefix = '!'
# end config

# token requires input at runtime for security reasons
token = '' 
if(len(sys.argv) >= 2):
    token = sys.argv[1]
else:
    print('Please include a bot token!')
    quit()
# end token

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('ccp!help'))
    print('\n# Logged on as {0.user}!\n'.format(client))

@client.event
async def on_message(message):
    db_cursor.execute(f"SELECT * FROM social_credit WHERE id = {message.author.id};")
    if len(db_cursor.fetchall()) == 0: db_cursor.execute(f"INSERT INTO `china`.`social_credit` (`id`, `credits`) VALUES ('{message.author.id}', '1000');")

    db_cursor.execute(f"SELECT credits FROM social_credit WHERE `id` = '{message.author.id}';")
    try:
        credits = int(db_cursor.fetchall()[0][0])
    except IndexError:
        pass

    if message.author == client.user: return
    
    if str(message.guild) != 'None':
        print(f'Message from {message.author} in {message.guild}.{message.channel}: {message.content}')
    else:
        print(f'Message from {message.author} in {message.channel}: {message.content}')

    await client.process_commands(message)

@client.command(name="socialadd")
@guild_only
@has_permissions(manage_members=True)
async def add_social(ctx):
     if len(message.content.split(" ")) == 3:
            try:
                id = re.findall("\d+", message.content.split(" ")[1])[0]\
                credits = int(message.content.split(" ")[2])

                credit_arg = credits
                
                db_cursor.execute(f"SELECT * FROM social_credit WHERE id = {id};")
                if len(db_cursor.fetchall()) == 0: db_cursor.execute(f"INSERT INTO `china`.`social_credit` (`id`, `credits`) VALUES ('{id}', '1000');")

                db_cursor.execute(f"SELECT credits FROM social_credit WHERE `id` = '{id}';")
                try:
                    credits = int(db_cursor.fetchall()[0][0]) + credits
                except IndexError:
                    pass
                db_cursor.execute(f"UPDATE social_credit SET credits = {credits} WHERE id = {id};")

                await ctx.reply(f"{credit_arg} social credit has been added to the user with ID ``{id}``.")

            except:
               await ctx.reply(f"**Usage:** {prefix}socialadd (@user) (points amount)")
        else:
            await ctx.reply(f"**Usage:** {prefix}socialadd (@user) (points amount)")

@add_social.error
async def add_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('You do not have permission to use this command!')

@client.command(name="socialrem")
@guild_only
@has_permissions(manage_members=True)
async def remove_social(ctx):
    if len(message.content.split(" ")) == 3:
            try:
                id = re.findall("\d+", message.content.split(" ")[1])[0]
                credits = int(message.content.split(" ")[2])

                credit_arg = credits
                
                db_cursor.execute(f"SELECT * FROM social_credit WHERE `id` = '{id}';")
                
                if len(db_cursor.fetchall()) == 0: db_cursor.execute(f"INSERT INTO `china`.`social_credit` (`id`, `credits`) VALUES ('{id}', '1000');")


                db_cursor.execute(f"SELECT credits FROM social_credit WHERE `id` = '{id}';")
                try:
                    credits = int(db_cursor.fetchall()[0][0]) - credits
                except IndexError:
                    pass
                db_cursor.execute(f"UPDATE social_credit SET credits = {credits} WHERE id = {id};")
                await ctx.reply(f"{credit_arg} social credit points have been taken from user with ID ``{id}``.")
                
            except:
                await ctx.reply(f"**Usage:** {prefix}socialrem (@user) (points amount)")")
        else:
            await ctx.reply(f"**Usage:** {prefix}socialrem (@user) (points amount)")

@remove_social.error
async def rm_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('You do not have permission to use this command!')

@client.command(name="help")
async def bot_help(ctx):
    await ctx.reply(f"\n**User commands:**
                    \n    **{prefix}help**: View this message.
                    \n    **{prefix}points**: View social credit.
                    \n    **{prefix}ping**: Pong!
                    \n\n**Admin commands:**:
                    \n    **{prefix}socialadd**: Add points to user.
                    \n    **{prefix}socialrem**: Remove points from user."
                    )

@client.command(name="points")
async def credit_amount():
    id = message.author.id

        db_cursor.execute(f"SELECT * FROM social_credit WHERE id = {message.author.id};")
        if len(db_cursor.fetchall()) == 0: 
            await message.reply("This user is not registered!")
            db_cursor.execute(f"INSERT INTO `china`.`social_credit` (`id`, `credits`) VALUES ('{message.author.id}', '1000');")
           
        else:
            db_cursor.execute(f"SELECT credits FROM social_credit WHERE `id` = '{id}';")
            try:
                credits = int(db_cursor.fetchall()[0][0])
            except IndexError:
                pass
        await message.reply(f"This user has {credits} social credit.")

@client.event
async def on_guild_join(guild):
    print(f'# Joined {guild.name}.')

@client.command()
async def ping(ctx):
    await ctx.reply(f'Pong! {round(client.latency * 1000)}ms')

client.run(token)
