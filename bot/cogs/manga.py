import discord
from discord.ext import commands
import aiohttp

import bs4

class Finder():

	def __init__(self):
		
		self.base_header="https://myanimelist.net/manga.php?q="

	async def find(self,name):

		async with aiohttp.ClientSession() as session:

			html_1=await self.fetch(session,self.base_header+name)
			link=await self.find_name(html_1)
			print(link)
			html_2=await self.fetch(session,link)

			details=await self.find_page(html_2)

			details["Link"]=link

			return details 

	async def fetch(self,session,url):

		async with session.get(url) as resp:


			return await resp.text()


	async def find_page(self,page):

		soup=bs4.BeautifulSoup(page,'html.parser')
		soup.prettify()

		Title=soup.find("span",attrs={"itemprop":"name"})
		Title=Title.find("span",class_="title-english").text
		
		Synopsis=soup.find('span',attrs={'itemprop':'description'}).text
		Score=soup.find('div',attrs={'class':"fl-l score"}).text
		image_get=soup.find('div',attrs={'style':'text-align: center;'})
		Image=image_get.find('img')['data-src']

		details={"Title":Title,"Synopsis":Synopsis,"Image":Image,"Score":Score}
		return details


	async def find_name(self,page):

		soup=bs4.BeautifulSoup(page,'html.parser')
		soup.prettify()

		div=soup.find("a",class_="hoverinfo_trigger fw-b")
		link =div.get('href')

		return link 


class Manga(commands.Cog):

	def __init__(self,bot):

		self.finder=Finder()
		self.bot=bot
		

	@commands.command()
	async def manga(self,ctx,arg1,*args):

		title=arg1

		for arg in args:
			title+=" "+arg

		self.details=await self.finder.find(title)

		await self.emb(self.details,ctx)
		
	async def emb(self,details,ctx):

		title=details.get(f"Title")
		synopsis=details.get(f"Synopsis")
		image=details.get("Image")
		score="**"+details.get(f"Score")+"**"
		link=details.get("Link")

		embed=discord.Embed(type="rich",title=title,description=synopsis,url=link,colour=5957435)
		embed.add_field(name="Score",value=score)
		embed.set_image(url=image)
		embed.set_footer(text="Sourced from MyAnimeList(MAL)", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9kgrRYpaVc53JFQ6iDuPN5eDMuTDFVr05ChTAg52_nEYMh1it")

		await ctx.send(embed=embed)




def setup(bot):
	
	bot.add_cog(Manga(bot))
