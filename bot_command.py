import discord
import asyncio
import command_list as cmdlst
import sys

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
        await self.run(message, args, author, client)

    def has_perms(self, user) :
        if self.lvl == cmd_lvl.everyone :
            return True
        if self.lvl == cmd_lvl.mods :
            return type(user) is discord.member.Member and user.top_role.permisions.mute_members
        if self.lvl == cmd_lvl.admins :
            return type(user) is discord.member.Member and user.top_role.permissions.administrator
        if self.lvl == cmd_lvl.bot_admins :
            return user.id in client.bot_admins
            

def find_command(message, client):
    test = message.content.lower()
    for cmd in client.cmd_list :
        if test.startswith(cmd.cmd) :
            return cmd
    return None
        
def init_commands() :
    cmds = []

    cmds.append(bot_cmd("!help", cmdlst.help, 1, 'Show a user all the commands they can use'))
    cmds.append(bot_cmd("!ping", cmdlst.ping, 1, 'If I\'m alive I will say Pong!'))
    cmds.append(bot_cmd("!noise", cmdlst.noise, 1, 'Generate 20 random letters'))
    cmds.append(bot_cmd("!deleteme", cmdlst.deleteme, cmd_lvl.mods, 'Delete all messages from the bot, use -s to not get feedback'))
    cmds.append(bot_cmd("!deletecmds", cmdlst.deletecmds, 1, 'Delete all command messages written by the user'))
    cmds.append(bot_cmd("!join", cmdlst.join, cmd_lvl.admins, 'Join the voice channel the user is in'))
    cmds.append(bot_cmd("!leave", cmdlst.leave, cmd_lvl.admins, 'Leave whatever voice channel the bot is in'))
    cmds.append(bot_cmd("!killme", cmdlst.endbot, cmd_lvl.bot_admins, 'Turn off the bot, will need to be manually restarted'))
                
    return cmds

