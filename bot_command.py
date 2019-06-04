import discord
import asyncio
import command_list as cmdlst
import sys
import importlib
import mtg_card_cmd

from enum import Enum

client = None

class cmd_lvl(Enum):
    everyone = 1
    #right now we use the mute_users permission to determine mod, but this may not be permanent
    mods = 2
    admins = 3
    bot_admins = 4
    
class bot_cmd:
    
    def __init__(self, cmd, run, lvl = cmd_lvl.everyone, desc = 'Default Description'):
        self.cmd = cmd.lower()
        self.run = run
        self.desc = desc
        self.lvl = lvl
        if type(self.lvl) == type(1) :
            self.lvl = cmd_lvl(self.lvl)


    def __str__(self):
        return '{} {}'.format(self.cmd, self.desc)

    async def execute(self, message, args, author, client):
        if not self.has_perms(author) :
            return
        #special check here to see if we need to reload the commands
        #this only reloads functionality, to add more commands the entire bot must be restarted for now
        if(self.cmd == '!reload') :
            global cmdlst
            cmdlst = importlib.reload(cmdlst)
            client.cmd_list = init_commands(client)
            print ('Reloaded commands')
            await message.channel.send('Reloaded command functionality')
            return
        await self.run(message, args, author, client)

    def has_perms(self, user) :
        if self.lvl == cmd_lvl.everyone :
            return True
        if self.lvl == cmd_lvl.mods :
            return type(user) is discord.member.Member and user.top_role.permissions.mute_members
        if self.lvl == cmd_lvl.admins :
            return type(user) is discord.member.Member and user.top_role.permissions.administrator
        if self.lvl == cmd_lvl.bot_admins :
            return str(user.id) in client.bot_admins
            

def find_command(command, client):
    test = command.lower()
    for cmd in client.cmd_list :
        if test == cmd.cmd :
            return cmd
    return None

def parse_command(message) :
    # TODO: support string arguments
    tmp = message.content.split(' ')
    return (tmp[0],tmp[1:])
        
def init_commands(client) :
    cmds = []

    cmds.append(bot_cmd("!reload", None, cmd_lvl.bot_admins, 'Reload the functionality of the commands'))
    cmds.append(bot_cmd("!help", cmdlst.help, 1, 'Show a user all the commands they can use'))
    cmds.append(bot_cmd("!ping", cmdlst.ping, 1, 'If I\'m alive I will say Pong!'))
    cmds.append(bot_cmd("!noise", cmdlst.noise, 1, 'Generate 20 random letters'))
    cmds.append(bot_cmd("!deleteme", cmdlst.deleteme, cmd_lvl.mods, 'Delete all messages from the bot, use -s to not get feedback'))
    cmds.append(bot_cmd("!deletecmds", cmdlst.deletecmds, 1, 'Delete all command messages written by the user'))
    cmds.append(bot_cmd("!deleteallcmds", cmdlst.deleteallcmds, cmd_lvl.mods, 'Delete all command messages written by anyone'))
    cmds.append(bot_cmd("!join", cmdlst.join, cmd_lvl.admins, 'Join the voice channel the user is in'))
    cmds.append(bot_cmd("!leave", cmdlst.leave, cmd_lvl.admins, 'Leave whatever voice channel the bot is in'))
    cmds.append(bot_cmd("!killme", cmdlst.endbot, cmd_lvl.bot_admins, 'Turn off the bot, will need to be manually restarted'))
    cmds.append(bot_cmd("!downloadchat", cmdlst.downloadhistory, cmd_lvl.bot_admins, 'Downloads chat history since the last download in the current channel'))
    cmds.append(bot_cmd("!rock", cmdlst.rockfact, 1, 'Say a random rock fact!'))
    cmds.append(bot_cmd("!flip", cmdlst.coinflip, 1, 'Flip a coin with cryptographically secure randomness!'))
    cmds.append(bot_cmd("!roulette", cmdlst.roulette, 1, 'Test your luck!'))
    cmds.append(bot_cmd("!markov", cmdlst.markov, 1, 'Generate a random sentence based on the current markov data (set by admins)'))
    cmds.append(bot_cmd("!markovusers", cmdlst.markovusers, 1, 'Get sent a list of markov users'))
    client.markov_chains = None
    client.named_markov_chains = None
    cmds.append(bot_cmd("!cardboard", mtg_card_cmd.mtgcard, 1, 'Search for a piece of cardboard by name'))

    return cmds

