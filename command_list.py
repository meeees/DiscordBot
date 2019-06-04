import discord
import asyncio
import os, datetime, time, base64
from random import randint, SystemRandom
import facts
from bot_markov import named_bot_markov_chain, bot_markov_chain

async def rockfact(message, args, author, client) :
    await message.channel.send(facts.get_fact('rock'))



