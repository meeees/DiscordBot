import discord
import asyncio
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
