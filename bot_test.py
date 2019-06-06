import discord
import asyncio
import bot_command as botcmd
import bot_settings as settings

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

client = discord.Client()
client.cmd_list = botcmd.init_commands(client)
botcmd.client = client

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    #we don't want to act on other bots
    if message.author.bot:
        return
    msgArgs = botcmd.parse_command(message)
    msgCmd = botcmd.find_command(msgArgs[0], client)
    if msgCmd:
        await msgCmd.execute(message, msgArgs[1], message.author, client)

client.settings = settings.bot_settings('bot-data/settings.json')
token = client.settings.get_val('token')
client.bot_admins = client.settings.get_val('admins')
client.run(token)