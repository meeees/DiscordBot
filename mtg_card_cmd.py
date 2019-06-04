import discord
import asyncio
import requests as re

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
	await message.channel.send(response.json()['image_uris']['large'])


if __name__ == '__main__' :
	name = 'aust+com'
	url = 'https://api.scryfall.com/cards/named?fuzzy=' + name
	response = re.get(url)
	print (response.json()['image_uris']['large'])