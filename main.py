# ------ Modules ------ #

import discord
import datetime
import settings
import keep_alive
from discord.ext import commands


# ------ Main Method ------ #

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():

        bot.start_time = datetime.datetime.now()

        print("----------------- BOT INFO -----------------")
        logger.info(f"ID: {bot.user.id}")
        logger.info(f"User: {bot.user}")
        print("---------------- BOT ONLINE ----------------")

  

    @bot.command(
      aliases = ['p']
    )
    async def ping(ctx):
      
        latency = bot.latency * 1000
        server_name = ctx.guild.name if ctx.guild else "Direct Message"
        uptime = datetime.datetime.now() - bot.start_time
        uptime_seconds = uptime.total_seconds()
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]
        num_servers = len(bot.guilds)
        timestamp = ctx.message.created_at.strftime("%m/%d/%Y %I:%M %p")

        await ctx.send(f"_*Pong !*_\n\n> Servers: {num_servers}\n> Latency: {latency:.2f}ms\n> Server Name: {server_name}\n\n`Uptime: {uptime_str}`\n`{timestamp}`")

    @bot.command()
    async def love(ctx):

        await ctx.send(f"I Still Love You <@881073499429552168> :heart:")

    bot.run(settings.DISCORD_API_TOKEN)
    
keep_alive.keep_alive()

if __name__ == "__main__":
    run()
