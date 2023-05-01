# ------ Modules ------ #

import discord
import datetime
import random
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

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Handeled Error Gocally")


# ------ Bot Commands ------ #

    @bot.command()
    async def ping(ctx):

        latency = bot.latency * 1000
        server_name = ctx.guild.name if ctx.guild else "Direct Message"
        uptime = datetime.datetime.now() - bot.start_time
        uptime_seconds = uptime.total_seconds()
        uptime_str = str(
            datetime.timedelta(seconds=uptime_seconds)).split(".")[0]
        num_servers = len(bot.guilds)
        timestamp = ctx.message.created_at.strftime("%m/%d/%Y %I:%M %p")

        await ctx.send(
            f"_*Pong !*_\n\n> Servers: {num_servers}\n> Latency: {latency:.2f}ms\n> Server Name: {server_name}\n\n`Uptime: {uptime_str}`\n`{timestamp}`"
        )

    @bot.command()
    async def love(ctx):

        await ctx.send(f"I Still Love You <@881073499429552168> :heart:")

    @bot.command()
    async def say(ctx, *, message=None):
        if message is None:
            await ctx.send("Please Enter A Message")
        else:
            await ctx.send(message)

    @bot.command()
    async def roll(ctx, num1=0, num2=100):

        await ctx.send(
            f"Your Roll [ {num1} - {num2} ] : {random.randint(num1, num2)}")

    @bot.command()
    async def slap(ctx, user: discord.Member, item: str):
        author = ctx.author
        response = f"{author.mention} Slapped {user.mention} With {item} !"
        await ctx.send(response)

    @bot.command()
    async def botslap(ctx, user: discord.Member, item: str):
        response = f"<@1101810424380391444> Slapped {user.mention} With {item} !"
        await ctx.send(response)

        bot.run(settings.DISCORD_API_TOKEN)

keep_alive.keep_alive()

if __name__ == "__main__":
    run()
