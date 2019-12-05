import discord
import asyncio
import command_list as cmdlst
import sys
import importlib
import os

from enum import Enum
from bot_refuse import refuse

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
        if(self.cmd == 'reload') :
            await bot_cmd.reload(message.channel)
            return
        #only admins may change refusalLevel of bot
        if self.cmd == 'refusallevel' and len(args) :
            if str(author.id) in client.bot_admins :
                await self.run(message, args, author, client)
            return
        #if a peasant-level command is executed, the bot might not comply.
        if self.lvl == cmd_lvl.everyone and refuse.think_about_refusing() :
            await refuse.send_refusal(message, args, author, client)
            return
        #else run given command
        await self.run(message, args, author, client)

    @staticmethod
    def check_perms(user, lvl) :
        if lvl == cmd_lvl.everyone :
            return True
        if lvl == cmd_lvl.mods :
            return type(user) is discord.member.Member and user.top_role.permissions.mute_members
        if lvl == cmd_lvl.admins :
            return type(user) is discord.member.Member and user.top_role.permissions.administrator
        if lvl == cmd_lvl.bot_admins :
            return str(user.id) in client.bot_admins

    def has_perms(self, user) :
        return bot_cmd.check_perms(user, self.lvl)

    @staticmethod
    async def reload(channel): 
        global cmdlst
        cmdlst = importlib.reload(cmdlst)
        client.cmd_list = init_commands(client)
        print ('Reloaded commands')
        await channel.send('Reloaded command functionality')


def find_command(command, client):
    prefix = client.settings.get_val('cmd_prefix')
    if (not command.startswith(prefix)):
        return None
    command = command[len(prefix):]
    test = command.lower()
    for cmd in client.cmd_list :
        if test == cmd.cmd :
            return cmd
    return None

def parse_command(message):
    tmp = message.content.split(' ')
    return (tmp[0], [x for x in tmp[1:] if x != ''])

_loaded_modules = {}
def load_plugins():
    global _loaded_modules
    #print (_loaded_modules)
    new_modules = {}
    importlib.invalidate_caches()
    sys.path.append(sys.path[0] + '/plugins')
    #print(sys.path)
    index = 0
    path = sys.path[0] + '/plugins'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    def recurse_obj(obj):
        lst = []
        if (isinstance(obj, bot_cmd)):
            return [obj]
        elif (isinstance(obj, list)):
            for x in obj:
                lst += recurse_obj(x)
        return lst

    for f in files:
        if f in _loaded_modules.keys() :
            module = importlib.reload(_loaded_modules[f][0])
        else :
            module = __import__(f[0:-3])
        commands = []
        
        for x in dir(module):
            obj = getattr(module, x)
            commands += recurse_obj(obj)

        new_modules['%s' % f] = (module, commands)

    _loaded_modules = new_modules
    return _loaded_modules

def init_commands(client):
    cmds = []

    cmds.append(bot_cmd("reload", None, cmd_lvl.bot_admins, 'Reload the functionality of the commands'))
    cmds.append(bot_cmd("rock", cmdlst.rockfact, 1, 'Say a random rock fact!'))
    
    client.markov_chains = None
    client.named_markov_chains = None

    modules = load_plugins()
    for m in modules.keys():
        _m, _cmds = modules[m]
        cmds += _cmds

    return cmds

