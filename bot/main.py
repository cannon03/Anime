from discord.ext import commands
import asyncio

Token = ""

extensions = ['cogs.anime']

class Free(commands.Bot):

	def __init__(self):
		super().__init__(command_prefix="$")

		for extension in extensions:

			self.load_extension(extension)


	async def on_ready(self):

		print(f"Logged in as {self.user}")


if __name__ == '__main__':
	free= Free()
	free.run(Token)