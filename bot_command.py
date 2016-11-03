import discord
import asyncio
import command_list as cmdlst
import sys

from enum import Enum


class cmd_lvl(Enum):
    everyone = 1
    #not sure what I will use to determine if someone is a mod or not
    mods = 2
    admins = 3
    
class bot_cmd:
    def __init__(self, cmd, run, lvl = cmd_lvl.everyone, desc = 'Default Description'):
        self.cmd = cmd
        self.run = run
        self.desc = desc
        self.lvl = lvl


    def __str__(self):
        return '{} {}'.format(self.cmd, self.desc)

    async def execute(self, message, args, author, client):
        if not self.has_perms(author) :
            return
        await self.run(message, args, author, client)

    def has_perms(self, user) :
        if self.lvl == cmd_lvl.everyone :
            return True
        if self.lvl == cmd_lvl.admins :
            return type(user) is discord.member.Member and user.top_role.permissions.administrator

def find_command(message, client):
    for cmd in client.cmd_list :
        if message.content.startswith(cmd.cmd) :
            return cmd
    return None
        
def init_commands() :
    cmds = []

    cmds.append(bot_cmd("!help", cmdlst.help))
    cmds.append(bot_cmd("!ping", cmdlst.ping))
    cmds.append(bot_cmd("!noise", cmdlst.noise))
    cmds.append(bot_cmd("!deleteme", cmdlst.deleteme))
    cmds.append(bot_cmd("!deletecmds", cmdlst.deletecmds))
    cmds.append(bot_cmd("!join", cmdlst.join, cmd_lvl.admins))
    cmds.append(bot_cmd("!leave", cmdlst.leave, cmd_lvl.admins))
    
    return cmds

