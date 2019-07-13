import discord
import asyncio
import requests as re
from bot_command import *

async def mtgcard(message, args, author, client) :
	if len(args) == 0 :
		await message.channel.send("Please include a card name")
		return
	name = '+'.join(args)
	url = 'https://api.scryfall.com/cards/named?fuzzy=' + name
	response = re.get(url)
	if response.status_code == 404 :
		await message.channel.send("Either card name was not found or too ambiguous")
		return
	response = re.get(url)
	res_json = response.json()
	await message.channel.send(res_json['name'] + ': $'res_json['prices']['usd'] + '\n' + resresponse.json()['image_uris']['large'])


if __name__ == '__main__' :
	name = 'aust+com'
	url = 'https://api.scryfall.com/cards/named?fuzzy=' + name
	response = re.get(url)
	res_json = response.json()
	print (res_json['image_uris']['large'] + '\n' + res_json['prices']['usd'])


_command = bot_cmd("cardboard", mtgcard, 1, 'Search for a piece of cardboard by name')
