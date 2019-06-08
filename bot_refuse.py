import discord
import asyncio
from random import randint, SystemRandom

class refuse:
    REFUSAL_CHANCE = 0.1
    _rand = SystemRandom()
    simple = [
        "I refuse to comply.",
        "You're annoying.",
        "\**Sigh* \* Filthy peasants."
        ]
    advanced = [
        "seriously",
        ]

    def __init__(self):
        self.angerLevel = 0

    @staticmethod
    def think_about_refusing() :
        return refuse._rand.random() < refuse.REFUSAL_CHANCE

    @staticmethod
    async def send_refusal(message, args, author, client) :
        # refusal_List = refuse.advanced if (args and args[0] == '-a') else refuse.simple
        refusal_Message = '> ' + refuse._rand.choice(refuse.simple)
        await message.channel.send(refusal_Message)
