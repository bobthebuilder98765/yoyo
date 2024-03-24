import discord
import requests
import bs4
import random
import warnings
import os
import asyncio
from discord.ext import commands
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from webserver import keep_alive

warnings.filterwarnings("ignore", category=InsecureRequestWarning)
client = commands.Bot(command_prefix='/', intents=discord.Intents.all())

def get_jokes(URL):
    jokes = []
    headers = {"Content-Type": "text/html; charset=utf-8"}
    response = requests.get(URL, headers=headers, verify=False)
    soup = bs4.BeautifulSoup(response.content, "html.parser", from_encoding="windows-1255")
    elements = soup.find_all(style="font-weight:bold;color:#274cb4;margin-top:7px;text-align: center")
    for element in elements:
        jokes.append(element.text)
    return jokes

@client.hybrid_command()
async def urmom(ctx: commands.Context, user: discord.Member = None):
    jokes = get_jokes("https://jokes.yo-yoo.co.il/?cat=%E0%EE%E0%F9%EA")
    jokes += get_jokes("https://jokes.yo-yoo.co.il/?cat=%E0%EE%E0%F9%EA&page=2")
    joke = random.choice(jokes)
    if user is None:
        user = ctx.author
    message = f"{user.mention} {joke}"
    await ctx.send(message)

@client.hybrid_command()
async def plank(ctx: commands.Context):
    jokes = get_jokes("https://jokes.yo-yoo.co.il/?cat=%F7%F8%F9")
    joke = random.choice(jokes)
    await ctx.send(joke)

@client.hybrid_command()
async def dark(ctx: commands.Context):
    jokes = get_jokes("https://jokes.yo-yoo.co.il/?cat=%E4%E5%EE%E5%F8%20%F9%E7%E5%F8")
    joke = random.choice(jokes)
    await ctx.send(joke)


@client.event
async def on_ready():
    await client.tree.sync()
    print(f'{client.user} has connected to Discord!')
    await client.tree.sync()


keep_alive()
TOKEN = os.environ.get("token")
client.run(TOKEN)
