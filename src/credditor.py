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


config = ConfigParser()

def config_setup(file):
    config["APP OPTIONS"] = {
        "prefix": "-social",
        "reply_ping": "false"
    }

    with open(file, 'w') as conf:
        config.write(conf)

if exists("conf/config.ini") == False:
    print('> Config file \'config.ini\' does not exist, creating...')
    config_setup('conf/config.ini')
    print('> Config file \'config.ini\' created.')
else:
    print('> Config file found.')

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
    msg = message.content.lower()
    if check_neg_trigger(msg) == True:
        print(f'# {str(message.author)} triggered negative social credit!')
        if app_options["reply_ping"] == "false":
            await message.reply('-100 social credit!! 😭', mention_author=False)
        else:
            await message.reply('-100 social credit!! 😭')
        try:
            credits = credits - 100
            db_cursor.execute(f"UPDATE social_credit SET credits = {credits} WHERE id = {message.author.id};")
        except UnboundLocalError:
            pass
    if check_pos_trigger(msg) == True:
        print(f'# f{str(message.author)} triggered positive social credit!')
        if app_options["reply_ping"] == "false":
            await message.reply('+100 social credit!! 👲🤏', mention_author=False)
        else:
            await message.reply('+100 social credit!! 👲🤏')
        try:
            credits = credits + 100
            db_cursor.execute(f"UPDATE social_credit SET credits = {credits} WHERE id = {message.author.id};")
        except UnboundLocalError:
            pass

    if "+social" in msg and message.author.id == 543513627794210825:
        
        if len(message.content.split(" ")) == 3:
            try:
                id = re.findall("\d+", message.content.split(" ")[1])[0]
                

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

                await message.channel.send(f":white_check_mark: Se le han añadido al usuario con ID ``{id}`` {credit_arg} puntos sociales")

            except:
               await message.reply(":exclamation: Uso: ``+social @nombre puntos``")
        else:
            await message.reply(":exclamation: Uso: ``+social @nombre puntos``")

    if "-social" in msg and message.author.id == 543513627794210825:
        
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
                await message.channel.send(f":white_check_mark: Se le han quitado al usuario con ID ``{id}`` {credit_arg} puntos sociales")
                
            except:
                await message.reply(":exclamation: Uso: ``+social @nombre puntos``")
        else:
            await message.reply(":exclamation: Uso: ``+social @nombre puntos``")

    if "ccp!help" in msg: 
        await message.channel.send("\n**Comandos del usuario**:\n``ccp!social``: Ver mis social points.\n\n**Comandos del admin**:\n``+social``: Añade puntos a un usuario. \n``-social``: Quita puntos a un usuario.")
    
    if "ccp!social" in msg: 

        id = message.author.id


        db_cursor.execute(f"SELECT * FROM social_credit WHERE id = {message.author.id};")
        if len(db_cursor.fetchall()) == 0: 
            await message.channel.send(":exclamation: El usuario no está registrado!")
            db_cursor.execute(f"INSERT INTO `china`.`social_credit` (`id`, `credits`) VALUES ('{message.author.id}', '1000');")
           
        else:
            db_cursor.execute(f"SELECT credits FROM social_credit WHERE `id` = '{id}';")
            try:
                credits = int(db_cursor.fetchall()[0][0])
            except IndexError:
                pass
        await message.channel.send(f"El usuario tiene {credits} créditos sociales.")


    
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    print(f'# Joined {guild.name}.')

@client.command()
async def ping(ctx):
    await ctx.reply(f'Pong! {round(client.latency * 1000)}ms')

client.run(token)
