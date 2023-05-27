# --------- Modules --------- #

import os
import random
import asyncio
import discord
import datetime
import requests
import keep_alive
from discord.ext import commands

# --------- BOT Setup --------- #

intents = discord.Intents.all()
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --------- BOT Initialisation --------- #


@bot.event
async def on_ready():

  bot.start_time = datetime.datetime.now()

  print(f'------------------------------')
  print(f'{bot.user.name} Is ONLINE')
  print(f'------------------------------')

  await bot.tree.sync()
  await bot.change_presence(activity=discord.Game(name="With Utilities"))


# --------- BOT Commands / Cogs --------- #


@bot.tree.command(name="ping", description="Get Bot's Letacy")
async def ping(interaction):
  latency = bot.latency * 1000
  server_name = interaction.guild.name if interaction.guild else "Direct Message"
  uptime = datetime.datetime.now() - bot.start_time
  uptime_seconds = uptime.total_seconds()
  uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]
  num_servers = len(bot.guilds)

  embed = discord.Embed(title="_*Pong !*_", color=0x2f3136)
  embed.add_field(name="---------------------", value="     ", inline=False)
  embed.add_field(name="Servers", value=num_servers, inline=False)
  embed.add_field(name="Latency", value=f"{latency:.2f}ms", inline=False)
  embed.add_field(name="Server Name", value=server_name, inline=False)
  embed.add_field(name="Uptime", value=uptime_str, inline=False)

  await interaction.response.send_message(embed=embed)





@bot.tree.command(name="say", description="Repeates After You")
async def say(interaction, *, message: str = None):
  if message is None:
    await interaction.response.send_message("Please Enter A Message")
  else:
    await interaction.response.send_message(message)


@bot.tree.command(name="roll", description="Rolls A Dice For You")
async def roll(interaction, num1: int = 0, num2: int = 100):

  embed = discord.Embed(title="Roll Dice", color=0x2f3136)
  embed.add_field(name="Range", value=f"{num1} - {num2}", inline=False)
  embed.add_field(name="Result",
                  value=f"{random.randint(num1, num2)}",
                  inline=False)

  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="slap", description="Slaps Someone")
async def slap(interaction, user: discord.Member, item: str):
  response = interaction.user
  if user.id == 727012870683885578:
    user = response
  response = f"{response.mention} Slapped {user.mention} With {item} !"

  embed = discord.Embed(title="Slap !", description=response, color=0x2f3136)

  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="infouser", description="Get Information About A User")
async def user(interaction, member: discord.Member = None):
  if member is None:
    member = interaction.user

  roles = [role.name for role in member.roles[1:]]
  roles_str = ", ".join(roles) if len(roles) > 0 else "None"

  embed = discord.Embed(title=f"{member.display_name}'s Info",
                        color=int("0x2f3136", 16))
  embed.add_field(name="User ID", value=member.id, inline=False)
  embed.add_field(name="Nickname",
                  value=member.nick if member.nick else "None",
                  inline=False)
  embed.add_field(name="Roles", value=roles_str, inline=False)
  embed.add_field(name="Join Date",
                  value=member.joined_at.strftime("%Y-%m-%d | %H:%M:%S UTC"),
                  inline=False)
  embed.add_field(name="Account Creation",
                  value=member.created_at.strftime("%Y-%m-%d | %H:%M:%S UTC"),
                  inline=False)
  embed.set_thumbnail(url=member.avatar.url)

  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="weather", description="Get Weather Of A Location")
async def weather(interaction, *, location: str):
  api_key = '34379a10e456c41b137b3f30379215e5'
  url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description'].capitalize()
    icon = data['weather'][0]['icon']
    precipitation = data.get('rain', {}).get('1h', 0)
    humidity = data['main']['humidity']

    embed = discord.Embed(title=f'Weather In {city}, {country}',
                          description=description,
                          color=0x2f3136)
    embed.add_field(name='Temperature', value=f'{temp}°C', inline=True)
    embed.add_field(name='Feels Like', value=f'{feels_like}°C', inline=True)
    embed.add_field(name='', value=f'-------------------------', inline=False)
    embed.add_field(name='Humidity', value=f'{humidity} %', inline=False)
    embed.add_field(name='Precipitation',
                    value=f'{precipitation} mm',
                    inline=True)
    embed.set_thumbnail(url=f'https://openweathermap.org/img/wn/{icon}.png')

    await interaction.response.send_message(embed=embed)
  else:
    await interaction.response.send_message(
      f'Error: Could Not Get Weather Information For {location}.')


def get_random_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  data = response.json()
  joke_setup = data['setup']
  joke_punchline = data['punchline']
  return joke_setup, joke_punchline


@bot.tree.command(name="joke", description="Tells You A Random Joke")
async def joke(interaction):
  joke_setup, joke_punchline = get_random_joke()

  embed = discord.Embed(title="Joke", color=0x2f3136)
  embed.add_field(name=" ", value=joke_setup, inline=False)
  embed.add_field(name=" ", value=joke_punchline, inline=False)

  embed.set_footer(text="React With 🔄 To Get Another Joke!")

  joke_message = await interaction.channel.send(embed=embed)
  await joke_message.add_reaction("🔄")


@bot.tree.command(name="quote", description="Tells You A Random Quote")
async def quote(interaction):
  response = requests.get("https://api.quotable.io/random")
  data = response.json()
  content = data['content']
  response = data['response']

  embed = discord.Embed(title="Thoughtful Quote",
                        description=f"{content}",
                        color=0x2f3136)
  embed.add_field(name=" ", value=f"- {response}", inline=False)
  embed.set_footer(text="React With 🔄 To Get Another Quote!")

  quote_message = interaction.channel.send(embed=embed)
  await quote_message.add_reaction("🔄")


@bot.event
async def on_reaction_add(reaction, user):

  if str(reaction.emoji) == "🔄" and not user.bot:
    message = reaction.message
    if message.embeds and message.embeds[0].title == "Joke":
      joke_setup, joke_punchline = get_random_joke()

      embed = discord.Embed(title="Joke", color=0x2f3136)
      embed.add_field(name=" ", value=joke_setup, inline=False)
      embed.add_field(name=" ", value=joke_punchline, inline=False)

      embed.set_footer(text="React With 🔄 To Get Another Joke !")

      await message.edit(embed=embed)
      await message.remove_reaction("🔄", user)

    if message.embeds and message.embeds[0].title == "Thoughtful Quote":
      response = requests.get("https://api.quotable.io/random")
      data = response.json()
      content = data['content']
      response = data['response']

      embed = discord.Embed(title="Thoughtful Quote",
                            description=f"{content}",
                            color=0x2f3136)
      embed.add_field(name=" ", value=f"- {response}", inline=False)
      embed.set_footer(text="React With 🔄 To Get Another Quote!")

      await message.edit(embed=embed)
      await message.remove_reaction("🔄", user)


afk_users = {}


@bot.tree.command(name="afk", description="Sets User To AFK")
async def afk(interaction, *, message: str = None):
  afk_users[interaction.response.id] = message or True
  embed = discord.Embed(
    title="AFK Status Set",
    description=f"{interaction.response.display_name} Is Now AFK",
    color=0x2f3136)
  await interaction.response.send_message(embed=embed)
  await interaction.response.edit(
    nick=f'[AFK] {interaction.response.display_name}')


@bot.tree.command(name="removeafk", description="Removes User AFK")
async def removeafk(interaction):
  if interaction.response.id in afk_users:
    del afk_users[interaction.response.id]
    original_name = afk_users[interaction.response.id]['original_name']
    embed = discord.Embed(
      title="Removed AFK",
      description=f"{interaction.response.display_name} Is No Longer AFK",
      color=0x2f3136)
    await interaction.response.edit(nick=original_name)
    await interaction.response.send_message(embed=embed)
  else:
    embed = discord.Embed(
      title="Removed AFK",
      description=f"{interaction.response.display_name}, You Were Not AFK",
      color=0x2f3136)
  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="gif", description="Get A Gif For Keyword")
async def gif(interaction, *, message: str):
  keyword = message
  if keyword:
    url = f'https://api.giphy.com/v1/gifs/search?q={keyword}&api_key=nNoanEdlMAxSHdkQqUm1gWyX0UHomLUY&limit=10'
    response = requests.get(url)
    data = response.json()['data']

    if data:
      gif = random.choice(data)
      gif_url = gif['images']['original']['url']
      gif_message = await interaction.channel.send(gif_url)
      await interaction.response.send_message("Gottcha !", ephemeral=True)
      await gif_message.add_reaction("🔄")

      def check(reaction, user):
        return str(reaction.emoji) == "🔄" and user == interaction.user

      while True:
        try:
          reaction, user = await bot.wait_for('reaction_add',
                                              timeout=30.0,
                                              check=check)
          if not user.bot:
            new_gif = random.choice(data)
            new_gif_url = new_gif['images']['original']['url']
            await gif_message.edit(content=new_gif_url)
            await gif_message.remove_reaction("🔄", user)

        except TimeoutError:
          await gif_message.clear_reactions()

    else:
      await interaction.response.send_message(
        "No GIFs Found For The Keyword. Please Try A Different Keyword.")
  else:
    await interaction.response.send_message(
      "Please Provide A Keyword To Search For GIF.")


@bot.tree.command(name="help",
                  description="Shows Help Menu For De Utility Bot")
async def help_command(interaction):
  embed_page1 = discord.Embed(
    title="Utility Bot - Help",
    description="Welcome to the Utility Bot Help Menu!\n\n"
    "Here are some commands you can use:\n"
    "-------------------------------------------------------\n"
    "**1. `/ping`** - Get bot's latency and information\n"
    "**2. `/say`** - Repeats after you\n"
    "**3. `/roll`** - Rolls a dice\n"
    "**4. `/slap`** - Slaps someone\n"
    "**5. `/infouser`** - Get information about a user\n"
    "**6. `/weather`** - Get weather of a location\n"
    "**7. `/joke`** - Tells you a random joke\n"
    "**8. `/quote`** - Tells you a random quote\n"
    "**8. `/gif`** - Get a GIF for a keyword\n"
    "**10. `/afk`** - Set yourself as AFK\n"
    "**11. `/removeafk`** - Remove your AFK status\n\n"
    "-------------------------------------------------------",
    color=0x2f3136)

  await interaction.response.send_message(embed=embed_page1)


@bot.event
async def on_message(message):
  if not message.author.bot and message.id in afk_users:
    afk_message = afk_users[message.id]
    embed = discord.Embed(
      title="AFK Status",
      description=
      f"{message.author.display_name} Is Currently AFK \n Reason: {afk_message}",
      color=0x2f3136)
    await message.channel.send(embed=embed)
  await bot.process_commands(message)

  if bot.user.mention in message.content:
    embed = discord.Embed(
      title="Introduction",
      description=
      "Hi there, I am De Utility\n\nI am a multiutility bot. \nTo get started with me, use `!bhelp`"
    )
    embed.add_field(name="Prefix: !", value="", inline=False)
    embed.add_field(name="My Developers:",
                    value="SOHAM#3097 \nlelouchlamperouge#5197",
                    inline=False)
    embed.add_field(name=" ", value="", inline=False)
    embed.add_field(
      name=" ",
      value=
      "Invite Link: [Click here](https://discord.com/api/oauth2/authorize?client_id=1101810424380391444&permissions=8&scope=bot)",
      inline=False)
    await message.channel.send(embed=embed)


keep_alive.keep_alive()
token = os.environ['TOKEN']
bot.run(token)
