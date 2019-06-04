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

game_cmds = [
	bot_cmd("!flip", coinflip, 1, 'Flip a coin with cryptographically secure randomness!'),
    bot_cmd("!roulette", roulette, 1, 'Test your luck!'),
]
