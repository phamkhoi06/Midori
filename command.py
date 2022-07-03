import nextcord, json
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from bot import writejson, DEFAULT_PREFIX

class Commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# on ready print a message
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'Bot is ready! Logged in as: {self.bot.user}')
		name = "|mhelp|"
		activity_type=nextcord.ActivityType.watching #Status type
		await self.bot.change_presence(activity=nextcord.Activity(type=activity_type, name=name))

	@commands.Cog.listener()
	async def on_guild_join(self, guild): #when the bot joins the guild
		with open('prefixes.json', 'r') as f: #read the prefixes.json file
			prefixes = json.load(f) #load the json file
		prefixes[str(guild.id)] = DEFAULT_PREFIX
		writejson(prefixes)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild): #when the bot is removed from the guild

		with open('prefixes.json', 'r') as f: #read the file
			prefixes = json.load(f)
		prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from
		writejson(prefixes) #deletes the guild.id as well as its prefix

	@commands.command(pass_context=True)
	@has_permissions(administrator=True)
	async def prefix(self, ctx, prefix):
		"""Set prefix for commands with [prefix]command to use the bot"""
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = prefix
		writejson(prefixes)
		await ctx.send(f'Prefix changed to: {prefix}') #confirms the prefix it's been changed to

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			pass
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please pass in all requirements arguments.')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send("You dont have permission to excute this command")
		else:
			await ctx.send(error)

	@staticmethod
	def check_reason(message, reason): # this method append the reason to the message
		if reason:
			message = message + ' for reason ' + reason
		return message

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, member : nextcord.Member, *, reason = None):
		"""Ban a member with mention or their id"""

		dm = member.dm_channel
		if dm is None:
			dm = await member.create_dm()
		await dm.send(self.check_reason(message=f"You were banned in the server {ctx.guild.name}", reason=reason))
		await member.ban(reason = reason)
		await ctx.send(self.check_reason(message=f'Banned {member.mention}', reason = reason))

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, member, *, reason=None):
		"""Unban a member with [username]#[discriminator]"""

		bans_user = await ctx.guild.bans()
		name, discriminator = member.split('#')
		for ban_user in bans_user:
			user = ban_user.user
			if (name, discriminator) == (user.name, user.discriminator):
				await ctx.guild.unban(user)
				await ctx.send(self.check_reason(message=f'Unbanned {user.mention}', reason = reason))
				await user.send(self.check_reason(message=f"You were unbanned in the server {ctx.guild.name}", reason=reason))

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, member: nextcord.Member, *, reason=None):
		"""Mutes the specified user"""

		guild = ctx.guild
		mutedRole = nextcord.utils.get(guild.roles, name="Muted")
		if not mutedRole:
			mutedRole = await guild.create_role(name="Muted")
			for channel in guild.channels:
				await channel.set_permissions(mutedRole, speak=False, send_messages=False)
		await member.add_roles(mutedRole, reason=reason)
		await ctx.send(self.check_reason(message=f"Muted {member.mention}", reason=reason))
		await member.send(self.check_reason(message=f"You were muted in the server {ctx.guild.name}", reason=reason))

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
		"""Unmutes a specified user"""

		mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")

		await member.remove_roles(mutedRole)
		await ctx.send(self.check_reason(message=f"Unmuted {member.mention}", reason=reason))
		await member.send(self.check_reason(message=f"You were unmuted in the server {ctx.guild.name}", reason=reason))

	@commands.command()
	@has_permissions(manage_messages=True)
	async def clear(self, ctx, amounts):
		"""Clear messages"""
		await ctx.channel.purge(limit=int(amounts)+1)
		await ctx.send(f'Cleared {amounts} messages')

	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, ext):
		"""Load a new extension"""

		try:
			async with ctx.typing():
				self.bot.load_extension(ext)
			await ctx.send(f'Load {ext} complete')
		except Exception as e:
			await ctx.send('An error occurred: ' + str(e))

	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, ext):
		"""Unload a existed extension"""

		try:
			async with ctx.typing():
				self.bot.unload_extension(ext)
			await ctx.send(f'Unload {ext} complete')
		except Exception as e:
			await ctx.send('An error occurred: ' + str(e))

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, ext):
		"""Reload a existed extension"""

		try:
			async with ctx.typing():
				self.bot.reload_extension(ext)
			await ctx.send(f'Reload {ext} complete')
		except Exception as e:
			await ctx.send('An error occurred: ' + str(e))

	@commands.command()
	@commands.is_owner()
	async def presence(self, ctx, type, *activities):
		"""Change presence of bot"""
		try:
			activity_type = eval(f'nextcord.ActivityType.{type.lower()}')
			act = ' '.join(activities)
			await self.bot.change_presence(activity = nextcord.Activity(type=activity_type, name=act))
			await ctx.send(f'Changed presence to **{type.upper()}** {act}')
		except Exception as e:
			await ctx.send('An error occurred: ' + str(e))
	
	@commands.command()
	async def avatar(self, ctx, member: nextcord.Member):
		"""Show up avatar of member mentioned"""
		try:
			eb = nextcord.Embed(description=f"{member.mention} is using this avatar:", color=nextcord.Color.blue())
			url = member.avatar.url
			eb.set_image(url=url)
			await ctx.send(embed=eb)
		except Exception as e:
			await ctx.send('An error occurred: ' + str(e))
def setup(bot):
	bot.add_cog(Commands(bot))