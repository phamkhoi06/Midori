import nextcord, json, os
from nextcord.ext import commands

DEFAULT_PREFIX = 'm' # this constant will be used in commands.py

def writejson(prefixes):
 	with open('prefixes.json', 'w') as f:
 		json.dump(prefixes, f, indent=4)

def get_prefix(placeholder, message):
	if not os.path.exists('prefixes.json'):
		writejson(dict())
	with open('prefixes.json', 'r') as f: # open and read the prefixes.json, assuming it's in the same file
		prefixes = json.load(f) # load the json as prefixes
	pf = prefixes.get(str(message.guild.id)) # recieve the prefix for the guild id given
	if pf:
		return pf
	else:
		prefixes[str(message.guild.id)] = DEFAULT_PREFIX
		writejson(prefixes) # write default prefix in the prefixes.json if not exist
		return DEFAULT_PREFIX


intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix= get_prefix, intents=intents) # initialize bot

exts = ['command', 'music', 'nsfw']
for ext in exts:
	bot.load_extension(ext) # load every extension in list above

# get bot's token stored in .env file
with open('.env', 'r') as f:
	token = f.readlines()[1]


bot.run(token)
