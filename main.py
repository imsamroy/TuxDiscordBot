import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Load all cogs in the cogs directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: cogs.{filename[:-3]}')

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("BOT TOKEN")
