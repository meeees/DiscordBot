import discord
import asyncio
import os, datetime, time, base64
from random import randint, SystemRandom
from bot_command import *

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

voice_cmds = [
	bot_cmd("!join", join, cmd_lvl.admins, 'Join the voice channel the user is in'),
    bot_cmd("!leave", leave, cmd_lvl.admins, 'Leave whatever voice channel the bot is in'),
]
