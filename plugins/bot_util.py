import discord
import asyncio
import os, datetime, time, base64
from random import randint, SystemRandom
from bot_command import *

async def ping(message, args, author, client) :
    await message.channel.send('Pong!')

async def noise(message, args, author, client) :
    await message.channel.send(''.join(chr(randint(65, 65 + 25)) for x in range(0, 20)))

async def deleteme(message, args, author, client) :
    counter = 0
    tmp = await message.channel.send('Finding messages...')
    # bulk delete only works on messages in the last 2 weeks, so we just grab messages from the last 24 hours
    day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.author.id == client.user.id and m.id != tmp.id).flatten()
    await message.channel.delete_messages(to_del)
    if len(args) > 0 and args[0] == '-s' :
        await tmp.delete()
        await message.delete()
    else :
        await tmp.edit(content = 'Deleted {} messages from me.'.format(len(to_del)))
            
async def deletecmds(message, args, author, client) :
    if message.channel.guild == None :
        await message.channel.send('I cannot delete your messages in a private channel')
        return
    counter = 0
    tmp = await message.channel.send('Finding messages...')
    # bulk delete only works on messages in the last 2 weeks, so we just grab messages from the last 24 hours
    day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    prefix = client.settings.get_val('cmd_prefix')
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.content.startswith(prefix) and m.author.id == message.author.id).flatten()
    await message.channel.delete_messages(to_del)
    if len(args) > 0 and args[0] == '-s' :
        await tmp.delete()
    else :
        await tmp.edit(content = 'Deleted {} command messages from you.'.format(len(to_del)))

async def deleteallcmds(message, args, author, client) :
    if message.channel.guild == None :
        await message.channel.send('I cannot delete your messages in a private channel')
        return
    counter = 0
    # bulk delete only works on messages in the last 2 weeks, so we just grab messages from the last 24 hours
    day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    tmp = await message.channel.send('Finding messages...')
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.content.startswith('!')).flatten()
    await message.channel.delete_messages(to_del)
    if len(args) > 0 and args[0] == '-s' :
        await tmp.delete()
    else :
        await tmp.edit(content = 'Deleted {} command messages.'.format(len(to_del)))

async def _help(message, args, author, client) :
    helpList = []
    await message.channel.send('Okay {}, sending you help. Check your PMs!'.format(author.name))
    for cmd in client.cmd_list :
        if cmd.has_perms(author) :
            helpList.append(str(cmd))
    if author.dm_channel == None :
        await author.create_dm()
    await author.dm_channel.send('Here are all the commands you can use (in wherever you typed !help):\n```\n' + ('\n'.join(helpList)) + '\n```')

async def endbot(message, args, author, client) :
    await message.channel.send('Goodbye!')
    print ("Ending due to command from {}".format(author.name))
    client.settings.save_data()
    await client.logout()

async def complain(message, args, author, client) :
    await message.channel.send('Your complaint has been noted.')
    if client.complaint_channel != None :
        await client.complaint_channel.send(message.content[10:])

async def save_data(message, args, author, client) :
    client.settings.save_data()
    await message.channel.send('Bot data has been saved.')

util_cmds = [
	bot_cmd("help", _help, 1, 'Show a user all the commands they can use'),
    bot_cmd("ping", ping, 1, 'If I\'m alive I will say Pong!'),
    bot_cmd("noise", noise, 1, 'Generate 20 random letters'),
    bot_cmd("deleteme", deleteme, cmd_lvl.mods, 'Delete all messages from the bot, use -s to not get feedback'),
    bot_cmd("deletecmds", deletecmds, 1, 'Delete all command messages written by the user'),
    bot_cmd("deleteallcmds", deleteallcmds, cmd_lvl.mods, 'Delete all command messages written by anyone'),
    bot_cmd("killme", endbot, cmd_lvl.bot_admins, 'Turn off the bot, will need to be manually restarted. It is recommended to use this to end the bot so that data will get saved.'),
    bot_cmd("complain", complain, 1, "File a complaint about the server"),
    bot_cmd("savedata", save_data, cmd_lvl.bot_admins, 'Save everything in the bot data')
]