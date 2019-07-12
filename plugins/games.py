import discord
import asyncio
import os, datetime, time, base64
from random import randint, SystemRandom
from bot_command import *

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

async def leaderboard(message, args, author, client) :
    # print full leaderboard
    points = sorted(client.user_points.items(), key = lambda kv:(kv[1], kv[0]))
    # 32 is magic number because why not?
    lines = [message.guild.get_member(points[n][0]).display_name.ljust(32) + str(points[n][1]).rjust(10) for n in range(0, len(points))]
    await message.channel.send('Points do not persist between restarts, Soon\U00002122')
    to_send = '```\n' + '\n'.join(lines) + '\n```'
    await message.channel.send(to_send)

async def points(message, args, author, client) :
        await message.channel.send(author.display_name + ', you have ' + str(client.user_points[author.id]) + ' point' + ('s!' if client.user_points[author.id] != 1 else '!' ))




game_cmds = [
	bot_cmd("flip", coinflip, 1, 'Flip a coin with cryptographically secure randomness!'),
    bot_cmd("roulette", roulette, 1, 'Test your luck!'),
    bot_cmd("leaderboard", leaderboard, 1, 'See who\'s winning'),
    bot_cmd("points", points, 1, 'Check your score'),
]
