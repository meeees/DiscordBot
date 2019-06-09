import discord
import asyncio
from bot_command import bot_cmd
from bot_refuse import refusalLevel, mood

refusal_cmds = [
    bot_cmd("refusallevel", refusalLevel, 1, "Update the bot's refusal level"),
    bot_cmd("mood", mood, 1, "Check on the bot's current mood")
]
