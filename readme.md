# Meeees Discord Bot

I'm writing a simple discord bot using the [discord.py](https://github.com/Rapptz/discord.py) API written by [Rapptz](https://github.com/Rapptz).

### Current State

Right now all I have done is implemented a few basic commands and made the command system modular so it is easy to add new commands. I know there is a system similar to this already existing in the API, but this is more for me to just program something rather than for practical uses.

I also made a simple permissions system to restrict what users can run which commands, but it is not finished.

I originally wanted to make a bot that reacted to input from a voice channel, but the API does not currently support that feature. If in the future it does, I will probably add functionality to this bot relating to it.

### Planned Features
* A proper argument system for commands, a very basic approach of this can be seen in `!deleteme` and `!deletecmds` but I want to make it a more general approach
* Better/more permissions, as well as determining what should qualify a user for a specific level (e.g. discord has no moderator flag)
* Possibly some sort of functionality involving the bot making sounds in a voice channel