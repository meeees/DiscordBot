import discord
from discord.utils import get
import asyncio
from bot_command import *

color_hex = {}

def load_colors():
	global color_hex
	if (len(color_hex) != 0):
		return
	dir_path = "bot-data/colors.txt"
	if os.path.exists(dir_path):
		with open(dir_path, 'r') as f:
			dat = f.read()
			color_hex = dict((a[0].lower(),a[1].lower()) for a in [x.split('\t') for x in dat.split('\n')])

async def color_role(message, args, author, client):
	color_name = ' '.join(args)
	load_colors()
	if (color_name.lower() in color_hex.keys()):
		col = color_hex[color_name.lower()]
		col_val = int(col[1:], 16)
		role_name = 'color_'+color_name.lower()
		check_for_duplicate = get(message.guild.roles, name=role_name)
		to_remove = [x for x in message.author.roles if x.name.startswith('color_')]
		if check_for_duplicate is None: # if the role doesn't exist
			role = await message.guild.create_role(name=role_name, colour=discord.Colour(col_val))
		else:
			role = check_for_duplicate
		await message.author.remove_roles(*to_remove)
		await message.author.add_roles(role)
	else:
		await message.channel.send('Color doesn\' exist in list!')

role_cmds = [
	bot_cmd("color", color_role, 1, 'Change your current color'),
]
