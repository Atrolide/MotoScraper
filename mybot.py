import discord
from discord.ext import commands
import main
from single_page import scrapeOlx
from ad_links import get_ad_links

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='hello')
async def say_hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')


@bot.command(name='jp2')
async def say_hello(ctx):
    await ctx.send(f'JP2GMD')


@bot.command(name='olx')
async def scrape_olx(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    # Send each list as a separate message
    for record in data:
        brand, model, year, mileage, engine_size, fuel_type, horse_power = record
        message = f"{brand} - {model} - {year} - {mileage} - {engine_size} - {fuel_type} - {horse_power}"
        await ctx.send(message)




bot.run('token')
