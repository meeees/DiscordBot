import discord
import asyncio
import bot_command as botcmd
import bot_settings as settings
import app_update.app_update as updater
import _thread as thread

from discord.utils import get

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

client = discord.Client()
client.cmd_list = botcmd.init_commands(client)
botcmd.client = client

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    client.admin_channel = client.guilds[0].get_channel(int(client.admin_channel_id))
    await client.admin_channel.send('Hello World')
    client.loop.create_task(save_loop())

@client.event
async def on_message_delete(message) :
    if client.log_deleted :
        if message.channel.guild != None and not message.author.bot :
            text = "Deleted Message: " + message.author.mention + " in: " + message.channel.mention + "\n" + message.content
            await message.channel.guild.get_channel(int(client.admin_channel_id)).send(text)

@client.event
async def on_message_edit(before, after) :
    if client.log_edited :
        if before.channel.guild != None and not before.author.bot and before.content != after.content :
            text = "Edited Message: " + before.author.mention + " in: " + before.channel.mention + "\n" + before.content + "\n->\n" + after.content
            await before.channel.guild.get_channel(int(client.admin_channel_id)).send(text)

@client.event
async def on_reaction_add(reaction, user) :
    name = resolve_emoji(reaction.emoji)
    # no self points :thinking:
    if reaction.message.author != user :
        if name in client.settings.get_val('updoot_reacts') :
            award_point(reaction.message.author.id)

@client.event
async def on_reaction_remove(reaction, user) :
    name = resolve_emoji(reaction.emoji)
    if reaction.message.author != user :
        if name in client.settings.get_val('updoot_reacts') :
            remove_point(reaction.message.author.id)



@client.event
async def on_message(message):
    #we don't want to act on other bots
    if message.author.bot:
        return
    msgArgs = botcmd.parse_command(message)
    msgCmd = botcmd.find_command(msgArgs[0], client)
    if msgCmd:
        await msgCmd.execute(message, msgArgs[1], message.author, client)

async def save_loop():
    while True:
        await asyncio.sleep(client.settings.get_val('save_interval'))
        client.settings.save_data()
        print ('Data saved')

def award_point(author_id) :
    points = client.settings.get_data_val('user_points')
    if points == None :
        points = {}
        client.settings.set_data_val('user_points', points)

    if author_id in points:
        points[author_id] += 1
    else :
        points[author_id] = 1

def remove_point(author_id) :
    points = client.settings.get_data_val('user_points')
    if points == None :
        points = {}
        client.settings.set_data_val('user_points', points)

    if author_id in points:
        points[author_id] -= 1
        # no negative points
        if points[author_id] < 0 :
            points[author_id] = 0
    else :
        # no negative points
        points[author_id] = 0

def resolve_emoji(e) :
    if isinstance(e, discord.Emoji) :
        return e.name
    else :
        return e

def init() :

    client.settings = settings.bot_settings('bot-data/settings.json')
    token = client.settings.get_val('token')
    client.bot_admins = client.settings.get_val('admins')
    client.admin_channel_id = client.settings.get_val('admin_channel')
    client.log_deleted = client.settings.get_val('log_deleted')
    client.log_edited = client.settings.get_val('log_edited')

    client.settings.load_data()

    if client.settings.get_val('use_updater') :
        thread.start_new_thread(updater.python_start, (lambda: botcmd.bot_cmd.reload(client.admin_channel), client.loop, ))
        print ('Bot updater started')
    
    client.run(token)

if __name__ == '__main__' :
    init()