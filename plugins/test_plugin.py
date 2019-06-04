import discord
import asyncio
import os, datetime, time, base64
from bot_command import *


async def ding(message, args, author, client) :
    await message.channel.send('Dong!')

# All the shit here will be put into the command list
__ = bot_cmd("ding", ding, 1, 'If I\'m alive I will say Dong!')

# This too
#other_cmd_list = [bot_cmd("!ding1", ding, 1, 'If I\'m alive I will say Dong!'),
#    bot_cmd("!ding2", ding, 1, 'If I\'m alive I will say Dong!'),
#    bot_cmd("!ding3", ding, 1, 'If I\'m alive I will say Dong!')]

# Any bot_cmd objects present in a module global object or globals list will be added to the command list
