import discord
import asyncio
import os, datetime, time, base64
from bot_command import *


async def testing(message, args, author, client) :
    log_data = client.logs_from(message.channel, 1)
    async for log in log_data :
        print(log)

async def downloadhistory(message, args, author, client) :
    channel = message.channel.name
    serverid = message.channel.guild.id
    dir_path = "bot-data/" + str(serverid)
    if not os.path.exists(dir_path) :
        os.makedirs(dir_path)
    out_path = dir_path + "/" + channel
    time_path = dir_path + "/" + channel + ".time"
    limit_time = None
    if os.path.exists(time_path) :
        with open(time_path, 'r') as lt :
            limit_time = datetime.datetime.utcfromtimestamp(int(float(lt.read())))

    start_time = time.time()
    log_data = message.channel.history(limit=999999999999999,after=limit_time)
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

log_cmds = [
    bot_cmd("!downloadchat", downloadhistory, cmd_lvl.bot_admins, 'Downloads chat history since the last download in the current channel'),
]