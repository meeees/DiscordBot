import discord
import asyncio
import string
from random import SystemRandom

class refuse:
    REFUSAL_CHANCE = 0.1
    _rand = SystemRandom()
    simple = [
        "I refuse to comply.",
        "You're annoying.",
        "\**Sigh* \* Filthy peasants."]
    advanced = [
        "seriously"]
    moods = [
        "The bot seems joyful.",
        "The bot seems happy.",
        "The bot seems content.",
        "The bot seems annoyed.",
        "The bot seems pretty unhappy.",
        "It's pissed.",
        "The bot is ignoring you now. Good luck.",
        ]

    # def __init__(self):
    #     self.anger_level = 0

    @staticmethod
    def get_mood():
        return refuse.moods[int(refuse.REFUSAL_CHANCE * (len(refuse.moods) - 1))]

    @staticmethod
    def set_refusal_level(pct):
        if pct >= 0 and pct <= 1:
            refuse.REFUSAL_CHANCE = pct
        elif pct >= -100 and pct <= 100:
            refuse.REFUSAL_CHANCE = abs(pct) / 100
        else:
            return False
        return True
    
    @staticmethod
    def get_refusal_level():
        return refuse.REFUSAL_CHANCE

    @staticmethod
    def think_about_refusing():
        return refuse._rand.random() < refuse.REFUSAL_CHANCE

    @staticmethod
    async def send_refusal(message, args, author, client):
        # refusal_List = refuse.advanced if (args and args[0] == '-a') else refuse.simple
        refusal_Message = '> ' + refuse._rand.choice(refuse.simple)
        await message.channel.send(refusal_Message)

async def refusalLevel(message, args, author, client) :
    if len(args) == 0:
        await message.channel.send(refuse.get_refusal_level())
        return
    if refuse.set_refusal_level(float(args[0])):
        await message.channel.send(refuse.get_mood())
        # await message.channel.send('<@{}>'.format(author.id))

async def mood(message, args, author, client) :
    await message.channel.send(refuse.get_mood())