import discord
import asyncio
import os, datetime, time, base64
from bot_command import *
from bot_markov import named_bot_markov_chain, bot_markov_chain

async def markov(message, args, author, client) :
    #print (args)
    if len(args) == 0 :
        if (not hasattr(client, 'markov_chains')) or client.markov_chains == None :
            tmp = await message.channel.send("Generating markov chains, please wait...")
            client.markov_chains = bot_markov_chain(False)
            client.markov_chains.load_markov('bot-data/136984919875387393/general')
            await tmp.delete()
        sentence = client.markov_chains.make_sentence()
        # we want sentences with at least 3 words
        tries = 0
        while (sentence.count(' ') < 3) :
            tries += 1
            if tries == 6 :
                break
            sentence = client.markov_chains.make_sentence()
        await message.channel.send(discord.utils.escape_mentions(sentence))
    else :
        if (not hasattr(client, 'named_markov_chains')) or client.named_markov_chains == None :
            tmp = await message.channel.send("Generating named markov chains, please wait...")
            client.named_markov_chains = named_bot_markov_chain(False)
            client.named_markov_chains.load_markov('bot-data/136984919875387393/general')
            await tmp.delete()
        try :
            sentence = args[0] + ': ' + client.named_markov_chains.generate_for(args[0])
        except :
            await message.channel.send("Username not found in markov chains!")
            return
        tries = 0
        while (sentence.count(' ') < 3) :
            tries += 1
            if tries == 6 :
                break
            sentence = args[0] + ': ' + client.named_markov_chains.generate_for(args[0])
        await message.channel.send(discord.utils.escape_mentions(sentence))



async def markovusers(message, args, author, client) :
    if not hasattr(client, 'named_markov_chains') or client.named_markov_chains == None :
        await message.channel.send("Named markov chains have not been generated, use !markov [name]")
        return
    if author.dm_channel == None :
        await author.create_dm()
    await author.dm_channel.send('```\n' + '\n'.join(client.named_markov_chains.chains.keys()) + '\n```')

markov_cmds = [
    bot_cmd("markov", markov, 1, 'Generate a random sentence based on the current markov data (set by admins)'),
    bot_cmd("markovusers", markovusers, 1, 'Get sent a list of markov users')
]