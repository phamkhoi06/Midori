import nextcord, random, json, requests
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from requests_html import HTMLSession

class getlink:
	#link
	prefix1 = "https://hentaiz.top/gallery/page/"
	prefix2 = "/?channels%5B%5D="
	kind_dict = {'non-hent':'', 'hent':'', 'video-hent':'', '3d-hent':'', 'video-irl':'', 'rl':'', 'rl-18':'', 'yuri':''}


	def get_id(self): # get id for every category
		session = HTMLSession()
		r = session.get('https://hentaiz.cc/gallery/')
		list_form = r.html.find('input.form-check-input')
		i=0
		for kind in self.kind_dict.keys():
			self.kind_dict[kind] = list_form[i].attrs.get('value')
			i += 1

	def checkvideo(self, kind):
		return True if (kind in ['video-hent', '3d-hent', 'video-irl']) else False

	def getlastpage(self, kind):
		session = HTMLSession()
		r = session.get("https://hentaiz.top/gallery/?channels%5B%5D=" + self.kind_dict.get(kind))
		btn = r.html.xpath('/html/body/div[1]/div[2]/nav/ul/li[5]/a', first=True)
		lastpage = int(btn.attrs.get('href').split('/')[5]) #get page from href attribute
		return lastpage

	def getlink(self, kind, lastpage):
		session = HTMLSession()
		page = random.randint(1,lastpage) #random page
		url = self.prefix1 + str(page) + self.prefix2 + self.kind_dict.get(kind)
		r = session.get(url)
		iv='img.img-fluid.mb-2.shadow-5-strong.rounded'
		if self.checkvideo(kind):
			iv='video.w-100'
		links = r.html.find(iv)
		for link in links:
			rs = link.attrs.get('src')
			yield rs


class nsfw(commands.Cog, getlink, name="NSFW Commands"):
	#property
	link_list = list()
	br_list = list()
	lastpage=0
	page_count=1
	list_kind = tuple(getlink.kind_dict.keys())
	kind='non-hent' # default kind
	firstTimeLaunch = False


	def __init__(self, bot):
		self.bot = bot
		#self.get_id()

	async def get_owner(self):
		owner = await self.bot.fetch_user(536530723239100426)
		self.name = owner.name
		self.discriminator = owner.discriminator

	def load(self):
		self.num = 0
		self.link_list.clear()
		for i in self.getlink(self.kind, self.lastpage):
			self.link_list.append(i)

	@commands.command()
	async def s(self, ctx):
		"""Refresh list of Images/Videos"""

		self.load()
		await ctx.send('Images/Videos was refreshed.')

	@commands.command()
	async def tag(self, ctx):
		"""List all supported tag for select command"""

		embed=nextcord.Embed()
		text="1.Non-hent\n2.Hent\n3.Video-hent\n4.Video-hent-3D\n5.Video-real-life\n6.Real-life\n7.Real-life-18\n8.Yuri"
		embed.add_field(name="All tag", value=text)
		embed.add_field(name="Usage", value=ctx.prefix + "select 1-8")
		await ctx.send(embed=embed)
	@commands.command()
	async def select(self, ctx, kind):
		"""Select tag with an interger corresponding to the tag you choice"""

		kind = int(kind)
		if kind not in range(1, 9): # range 1 --> 8
			await ctx.send('Change tag failed. Current Tag: ' + self.kind)
		else:
			self.kind = self.list_kind[kind-1]
			self.lastpage = self.getlastpage(self.kind)
			self.load()
			await ctx.send('Change tag successfully. Current Tag: ' + self.kind)

	@commands.command()
	async def w(self, ctx):
		"""This command will show images/videos sequentially"""
		await ctx.send('This command is being maintained')
		# if not self.firstTimeLaunch:
		# 	await self.get_owner()
		# 	self.lastpage = self.getlastpage(self.kind)
		# 	self.load() # load for the first time
		# 	self.firstTimeLaunch = True
		# if self.link_list:
		# 	url = random.choice(self.link_list)
		# 	self.link_list.remove(url)
		# 	if self.checkvideo(self.kind):
		# 		await ctx.send(f'```Midori Bot```{url}')
		# 	else:
		# 		embed=nextcord.Embed(title="Midori Bot", color=nextcord.Color.blue())
		# 		embed.set_image(url=url)
		# 		embed.set_footer(text=f"Bot developed by: {self.name}#{self.discriminator}")
		# 		await ctx.send(embed=embed)
		# else:
		# 	self.load() # refresh links list
		# 	await self.w(ctx)

	@nextcord.slash_command(description='Tìm kiếm ảnh ngẫu nhiên theo tag')
	async def br(self, interaction: Interaction, tags: str = SlashOption(description='Giữa các tag ngăn cách nhau bằng dấu cách(space)'), excludes: str = SlashOption(required=False, description='Thêm các tag vào danh sách loại trừ')):
		if not interaction.channel.is_nsfw():
			await interaction.send("**WARNING**: This command cant be used in non-nsfw channel")
		else:
			tags = tags.split(' ')
			#shrinked_tags = tags[2:]
			if(len(tags) < 2):
				pass
				#r = self.parse(f'https://danbooru.donmai.us/posts.json?tags={tags}&page={self.page_count}')
			else:
				r = self.parse(f'https://danbooru.donmai.us/posts.json?tags={tags[0]}+{tags[1]}&page={self.page_count}')
				for i in r:
					rating = i.get('rating')
					score = i.get('score')
					file_url = i.get('file_url')
					if rating != 'g' and score >= 5:
						self.br_list.append(file_url)
				print(self.br_list)

	@nextcord.slash_command(description='Tìm kiếm các tag có sẵn')
	async def tag_search(self, interaction: Interaction, tag: str):
		tag = tag.replace(' ', '_')
		url = (f'https://danbooru.donmai.us/tags.json?search[name_or_alias_matches]={tag}*&search[order]=count&search[hide_empty]=true')
		elms = self.parse(url)
		if not elms:
			await interaction.send(f"Cant find any tags for keyword `{tag.replace('_', ' ')}`")
		ac = str()
		for elm in elms[:10]:
			ac += f"Tag `{elm.get('name')}` in {elm.get('post_count'):,} posts\n"
		await interaction.send(ac)

	@staticmethod
	def parse(url):
		response = requests.get(url)
		return response.json()


def setup(bot):
	bot.add_cog(nsfw(bot))
