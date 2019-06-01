import discord
import asyncio
import os, datetime, time, base64
from random import randint, SystemRandom
import facts
import datetime

async def ping(message, args, author, client) :
    await message.channel.send('Pong!')

async def noise(message, args, author, client) :
    await message.channel.send(''.join(chr(randint(65, 65 + 25)) for x in range(0, 20)))

async def deleteme(message, args, author, client) :
    counter = 0
    tmp = await message.channel.send('Finding messages...')
    # bulk delete only works on messages in the last 2 weeks, so we just grab messages from the last 24 hours
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.author.id == client.user.id and m.id != tmp.id).flatten()
    await message.channel.delete_messages(to_del)
    if message.content.endswith('-s') :
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
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.content.startswith('!') and m.author.id == message.author.id).flatten()
    await message.channel.delete_messages(to_del)
    if message.content.endswith('-s') :
        await tmp.delete()
    else :
        await tmp.edit(content = 'Deleted {} command messages from you.'.format(len(to_del)))

async def deleteallcmds(message, args, author, client) :
    if message.channel.guild == None :
        await message.channel.send('I cannot delete your messages in a private channel')
        return
    counter = 0
    # bulk delete only works on messages in the last 2 weeks, so we just grab messages from the last 24 hours
    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    tmp = await message.channel.send('Finding messages...')
    to_del = await message.channel.history(limit=100, after=day_ago).filter(lambda m: m.conent.startswith('!')).flatten()
    await message.channel.delete_messages(to_del)
    if message.content.endswith('-s') :
        await tmp.delete()
    else :
        await tmp.edit(content = 'Deleted {} command messages.'.format(len(to_del)))


async def join(message, args, author, client) :
    uChannel = message.author.voice.channel
    vClient = message.guild.voice_client

    if vClient != None :
        if  uChannel != vClient.channel :
            print ('Joining voice channel: ' + uChannel.name)
            await vClient.move_to(uChannel)
    else :
        print ('Joining voice channel: ' + uChannel.name)
        await uChannel.connect()
            
async def leave(message, args, author, client) :               
    vClient = message.guild.voice_client
    if vClient != None:
        await vClient.disconnect()

async def help(message, args, author, client) :
    helpList = []
    await message.channel.send('Okay {}, sending you help, check your PMs!'.format(author.name))
    for cmd in client.cmd_list :
        if cmd.has_perms(author) :
            helpList.append(str(cmd))
    if author.dm_channel == None :
        await author.create_dm()
    await author.dm_channel.send('Here are all the commands you can use (in wherever you typed !help):\n```\n' + ('\n'.join(helpList)) + '\n```')

async def endbot(message, args, author, client) :
    await message.channel.send('Goodbye!')
    print ("Ending due to command from {}".format(author.name))
    await client.logout()

async def testing(message, args, author, client) :
    log_data = client.logs_from(message.channel, 1)
    async for log in log_data :
        print(log)

async def rockfact(message, args, author, client) :
    await message.channel.send(facts.get_fact('rock'))

async def coinflip(message, args, author, client) :
    if SystemRandom().randint(0, 1) == 1 :
        await message.channel.send('Heads!')
    else :
        await message.channel.send('Tails!')

async def roulette(message, args, author, client) :
    
    if message.author.voice != None :
        uChannel = message.author.voice.channel
        if SystemRandom().randint(0, 5) == 5 :
            await message.author.move_to(None)
            await message.channel.send(':boom:')
        else :
            await message.channel.send('Click')
    else :
        await message.channel.send('You must be in a voice channel to play')


async def downloadhistory(message, args, author, client) :
    channel = message.channel.name
    serverid = message.server.id
    dir_path = "bot-data/" + serverid
    if not os.path.exists(dir_path) :
        os.makedirs(dir_path)
    out_path = dir_path + "/" + channel
    time_path = dir_path + "/" + channel + ".time"
    limit_time = None
    if os.path.exists(time_path) :
        with open(time_path, 'r') as lt :
            limit_time = datetime.datetime.utcfromtimestamp(int(float(lt.read())))

    start_time = time.time()
    log_data = message.channel.history(after=limit_time)
    hist_out = open(out_path, 'a')
    data_out = []
    async for log in log_data :
        #skip bot messages and commands
        if log.author.bot or log.content.startswith('!') :
            continue
        name = base64.b64encode(log.author.name.encode('utf-16'))
        content = base64.b64encode(log.content.encode('utf-16'))
        data_out.append(name.decode("ascii") + ' ' + content.decode("ascii") + '\n')
    data_out = data_out[::-1]
    for do in data_out :
        hist_out.write(do)
    hist_out.close()
    with open(time_path, 'w') as nlt :
        nlt.write(str(start_time))
    await message.channel.send('Finished downloading all new messages in channel')


