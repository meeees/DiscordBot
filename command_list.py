import discord
import asyncio
import os, datetime, time, base64
from random import randint

async def ping(message, args, author, client) :
    await client.send_message(message.channel, 'Pong!')

async def noise(message, args, author, client) :
    await client.send_message(message.channel, ''.join(chr(randint(65, 65 + 25)) for x in range(0, 20)))

async def deleteme(message, args, author, client) :
    counter = 0
    tmp = await client.send_message(message.channel, 'Finding messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.author.id == client.user.id and log.id != tmp.id:
            await client.delete_message(log)
            counter += 1
    if message.content.endswith('-s') :
        await client.delete_message(tmp)
    else :
        await client.edit_message(tmp, 'Deleted {} messages from me.'.format(counter))
            
async def deletecmds(message, args, author, client) :
    if message.channel.is_private :
        await client.send_message(message.channel, 'I cannot delete your messages in a private channel')
        return
    counter = 0
    tmp = await client.send_message(message.channel, 'Finding messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.content.startswith('!') and log.author.id == message.author.id:
            await client.delete_message(log)
            counter += 1
    if message.content.endswith('-s') :
        await client.delete_message(tmp)
    else :
        await client.edit_message(tmp, 'Deleted {} command messages from you.'.format(counter))

async def join(message, args, author, client) :
    uChannel = message.author.voice.voice_channel
    vClient = client.voice_client_in(message.server)

    if vClient != None :
        if  uChannel != vClient.channel :
            print ('Joining voice channel: ' + uChannel.name)
            await vClient.move_to(uChannel)
    else :
        print ('Joining voice channel: ' + uChannel.name)
        await client.join_voice_channel(uChannel)
            
async def leave(message, args, author, client) :               
    vClient = client.voice_client_in(message.server)
    if vClient != None:
        await vClient.disconnect()

async def help(message, args, author, client) :
    helpList = []
    await client.send_message(message.channel, 'Okay {}, sending you help, check your PMs!'.format(author.name))
    for cmd in client.cmd_list :
        if cmd.has_perms(author) :
            helpList.append(str(cmd))
    await client.send_message(author, 'Here are all the commands you can use (in wherever you typed !help):\n```\n' + ('\n'.join(helpList)) + '\n```')

async def endbot(message, args, author, client) :
    await client.send_message(message.channel, 'Goodbye!')
    print ("Ending due to command from {}".format(author.name))
    await client.logout()

async def testing(message, args, author, client) :
    log_data = client.logs_from(message.channel, 1)
    async for log in log_data :
        print(log)

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
    log_data = client.logs_from(message.channel, limit=1000000000, after=limit_time)
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
    await client.send_message(message.channel, 'Finished downloading all new messages in channel')


