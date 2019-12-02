import discord
import asyncio
import re
from bot_command import bot_cmd, cmd_lvl

class Emotes:
    EMOTE_ADD_SYNTAX = '!emotes -a <name> <url or emote id>'
    EMOTE_REMOVE_SYNTAX = '!emotes -r <name>'
    EMOTE_VOTE_SYNTAX = '!emotes -v <name>'
    EMOTE_REVOKE_VOTE_SYNTAX = '!emotes -rv <name>'
    EMOTE_CURRENT_EMOTES_SYNTAX = '!emotes -c'
    URL_TEMPLATE = 'https://cdn.discordapp.com/emojis/{emote_id}.png'
    EMOTE_ID_REGEX = re.compile(r'^\s*([0-9]+)\s*$')

    @staticmethod
    async def display_current_emotes(message, args, author, client):
        emotes = map(lambda e: str(e), message.guild.emojis)
        to_send = ' '.join(emotes)
        await message.channel.send(to_send)

    @staticmethod
    async def display_proposed_emotes(message, args, author, client):
        if len(args) != 0:
            if any(arg.find('help') != -1 for arg in args):
                await Emotes.help(message, args, author, client)
            return
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are currently no proposed emotes! Propose one with `' + Emotes.EMOTE_ADD_SYNTAX + '`')
            return
        proposed_emotes = sorted(proposed_emotes.items(), key=lambda emote: len(emote[1]['votes']), reverse=True)
        lines = [str(len(proposed_emotes[n][1]['votes'])) + ': [' + proposed_emotes[n][0] + '](' + proposed_emotes[n][1]['url'] + ')' for n in range(0, len(proposed_emotes))]
        to_send = '\n'.join(lines)
        embed = discord.Embed()
        embed.add_field(name='Votes: Emote', value=to_send)
        await message.channel.send(embed=embed)

    @staticmethod
    async def add_proposed_emote(message, args, author, client):
        if len(args) == 0 or len(args) == 1:
            await message.channel.send('Please supply both an emote name, and an image url: `' + Emotes.EMOTE_ADD_SYNTAX + '`')
            return
        name = args[0]; url = args[1]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None:
            proposed_emotes = {}
            client.settings.set_data_val('proposed_emotes', proposed_emotes)
        if name in proposed_emotes:
            await message.channel.send('Emote already exists! Remove an emote with `' + Emotes.EMOTE_REMOVE_SYNTAX + '`')
            return
        if Emotes.EMOTE_ID_REGEX.match(url):
            url = Emotes.URL_TEMPLATE.format(emote_id = url)
        proposed_emotes[name] = { 'url': url, 'author': author.id, 'votes': { author.id } }
        await message.channel.send('Added Emote: ' + name)

    @staticmethod
    async def remove_proposed_emote(message, args, author, client):
        # Only allow mods to remove proposed emotes 
        if not bot_cmd.check_perms(author, cmd_lvl.mods):
            await message.channel.send('Sorry, only mods may remove proposed emotes (for now).')
            return
        if len(args) == 0:
            await message.channel.send('Please supply an emote to remove: `' + Emotes.EMOTE_ADD_SYNTAX + '`')
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes to remove! Add one with `' + Emotes.EMOTE_REMOVE_SYNTAX + '`')
            return
        try:
            proposed_emotes.pop(name)
            await message.channel.send('Removed Emote: ' + name)
        except KeyError:
            await message.channel.send('Emote `' + name + '` does not exist!  (...but you may add it) :thinking:')

    @staticmethod
    async def vote_for_proposed_emote(message, args, author, client):
        if len(args) == 0:
            await message.channel.send('Please specify the emote for which you would like to vote! `' + Emotes.EMOTE_VOTE_SYNTAX + '`')
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes! Add one with `' + Emotes.EMOTE_REMOVE_SYNTAX + '`')
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
            await message.channel.send('Please specify the emote from which you would like to revoke your vote! `' + Emotes.EMOTE_REVOKE_VOTE_SYNTAX + '`')
            return
        name = args[0]
        proposed_emotes = client.settings.get_data_val('proposed_emotes')
        if proposed_emotes == None or len(proposed_emotes.items()) == 0:
            await message.channel.send('There are no emotes! Add one with `' + Emotes.EMOTE_REMOVE_SYNTAX + '`')
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

    @staticmethod
    async def help(message, args, author, client):
        embed = discord.Embed(title="Emotes", colour=discord.Colour(0x1869f), description="Command options:\n\n")
        embed.add_field(name="-a", inline="false", value="Add an emote to the list of proposed emotes\n```" + Emotes.EMOTE_ADD_SYNTAX + "```")
        embed.add_field(name="-v", inline="false", value="Vote for a proposed emote\n```" + Emotes.EMOTE_REMOVE_SYNTAX + "```")
        embed.add_field(name="-r", inline="false", value="Remove an emote from the list of proposed emotes\n```" + Emotes.EMOTE_VOTE_SYNTAX + "```")
        embed.add_field(name="-rv", inline="false", value="Revoke your vote from one of the proposed emotes (note: 'v' and 'r' may be specified in any order, including but not limited to: `-vr`, `-rv`, `-v -r`, or `-r -v`)\n```" + Emotes.EMOTE_REVOKE_VOTE_SYNTAX + "```")
        embed.add_field(name="-c", inline="false", value="View the server's current emotes (this one's just for fun)```" + Emotes.EMOTE_CURRENT_EMOTES_SYNTAX + "```")
        await author.send(embed = embed)


#----- Definitions for emote commands, based on options length -----
def zero(options):
    return Emotes.display_proposed_emotes

def one(options):
    # todo: 'help' option
    return {
        'a': Emotes.add_proposed_emote,
        'c': Emotes.display_current_emotes,
        'r': Emotes.remove_proposed_emote,
        'v': Emotes.vote_for_proposed_emote,
        'help': Emotes.help
    }.get(options.pop())

def two(options):
    if { 'v', 'r' }.issubset(options):
        return Emotes.remove_vote_for_proposed_emote

#----- Switch case for commands, based on number of options -----#
EMOTES_COMMANDS_SWITCH = {
    0: zero,
    1: one,
    2: two,
}

def separate_options_and_args(args):
    argsIndex = 0
    options = set()
    for n in range(0, len(args)): 
        if args[n][0] != '-':
            break
        argsIndex += 1
        if args[n].find('help') != -1:
            options.add('help')
        else:
            for opt in args[n][1:]:
                options.add(opt)
    return (options, args[argsIndex:])

async def handle_emotes_command(message, args, author, client):
    options, args = separate_options_and_args(args)
    cmd = EMOTES_COMMANDS_SWITCH.get(len(options), lambda o: None)(options)
    if cmd != None:
        await cmd(message, args, author, client)

emote_cmds = [
    bot_cmd('emotes', handle_emotes_command, 1, 'Command to interact with server emotes, such as viewing proposed emotes and voting!'),
]