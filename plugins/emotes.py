import discord
import asyncio

from bot_command import bot_cmd

class Emotes:
    EMOTE_ADD_SYNTAX = '`!emote <name> <url>`'
    EMOTE_REMOVE_SYNTAX = '`!eremove <name>`'
    EMOTE_VOTE_SYNTAX = '`!vote <name>`'
    EMOTE_REVOKE_VOTE_SYNTAX = '`!rvote <name>`'

    @staticmethod
    async def display_proposed_emotes(message, args, author, client):
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are currently no proposed emotes! Propose one with ' + Emotes.EMOTE_ADD_SYNTAX)
            return
        proposed_emotes = sorted(proposed_emotes.items(), key=lambda emote: len(emote[1]['votes']), reverse=True)
        lines = [str(len(proposed_emotes[n][1]['votes'])).rjust(9) + ': [' + proposed_emotes[n][0].ljust(16) + '](' + proposed_emotes[n][1]['url'] + ')' for n in range(0, len(proposed_emotes))]
        to_send = '\n'.join(lines)
        embed = discord.Embed()
        embed.add_field(name='Votes: Emote', value=to_send)
        await message.channel.send(embed=embed)

    @staticmethod
    async def add_proposed_emote(message, args, author, client):
        if len(args) == 0 or len(args) == 1:
            await message.channel.send('Please supply both an emote name, and an image url: ' + Emotes.EMOTE_ADD_SYNTAX)
            return
        name = args[0]; url = args[1]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None:
            proposed_emotes = {}
            client.settings.set_data_val('proposed_emotes', proposed_emotes)
        if name in proposed_emotes:
            await message.channel.send('Emote already exists! Remove an emote with ' + Emotes.EMOTE_REMOVE_SYNTAX)
            return
        proposed_emotes[name] = { 'url': url, 'author': author.id, 'votes': { author.id } }
        await message.channel.send('Added Emote: ' + name)

    @staticmethod
    async def remove_proposed_emote(message, args, author, client):
        if len(args) == 0:
            await message.channel.send('Please supply an emote to remove: ' + Emotes.EMOTE_ADD_SYNTAX)
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes to remove! Add one with ' + Emotes.EMOTE_REMOVE_SYNTAX)
            return
        try:
            proposed_emotes.pop(name)
            await message.channel.send('Removed Emote: ' + name)
        except KeyError:
            await message.channel.send('Emote `' + name + '` does not exist!  (...but you may add it) :thinking:')

    @staticmethod
    async def vote_for_proposed_emote(message, args, author, client):
        if len(args) == 0:
            await message.channel.send('Please specify the emote for which you would like to vote! ' + Emotes.EMOTE_VOTE_SYNTAX)
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes! Add one with ' + Emotes.EMOTE_REMOVE_SYNTAX)
            return
        try:
            votes = proposed_emotes[name]['votes']
            if author.id in votes:
                await message.channel.send('You have already voted for ' + name)
                return
            votes.add(author.id)
            await message.channel.send('Successfully voted for ' + name)
        except KeyError:
            await message.channel.send('Emote `' + name + '` does not exist!  (...but you may add it) :thinking:')

    @staticmethod
    async def remove_vote_for_proposed_emote(message, args, author, client):
        if len(args) == 0:
            await message.channel.send('Please specify the emote from which you would like to revoke vote! ' + Emotes.EMOTE_REVOKE_VOTE_SYNTAX)
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes! Add one with ' + Emotes.EMOTE_REMOVE_SYNTAX)
            return
        try: 
            votes = proposed_emotes[name]['votes']
            try:
                votes.remove(author.id)
                await message.channel.send('Vote revoked from ' + name)
            except KeyError:
                await message.channel.send('You have not yet voted for this emote')
        except KeyError:
            await message.channel.send('Emote `' + name + '` does not exist!  (...but you may add it) :thinking:')    

emote_cmds = [
    bot_cmd('emotes', Emotes.display_proposed_emotes, 1, 'Display the list of proposed emotes'),
    bot_cmd('emote', Emotes.add_proposed_emote, 1, 'Add an emote to the proposed emotes list!'),
    bot_cmd('eremove', Emotes.remove_proposed_emote, 1, 'Remove an emote from the proposed emotes list'),
    bot_cmd('vote', Emotes.vote_for_proposed_emote, 1, 'Vote for a proposed emote!'),
    bot_cmd('rvote', Emotes.remove_vote_for_proposed_emote, 1, 'Revoke your support for a proposed emote')
]