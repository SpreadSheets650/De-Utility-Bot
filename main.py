import os

import discord
from discord.ext import commands

DISCORD_API_TOKEN = os.getenv('TOKEN')


def run():
    intents = discord.Intents.default()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'BOT ID : {bot.user.id}')
        print(f'BOT Name : {bot.user}')
        print("-------------- BOT ONLINE --------------")

    bot.run(DISCORD_API_TOKEN)


if __name__ == "__main__":
    run()
