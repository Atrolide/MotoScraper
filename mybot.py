from discord.ext import commands
from discord import Embed

import os
from dotenv import load_dotenv
import asyncio
import json

from Charts.olx_charts import *
from Charts.otomoto_charts import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        user = message.author
        embed = Embed(title=f"Welcome to Moto Scraper {user.name}!", description="Choose a website:")
        embed.add_field(name="1. otomoto.pl", value="Description for otomoto.pl", inline=False)
        embed.add_field(name="2. olx.pl", value="Description for olx.pl", inline=False)
        await message.channel.send(embed=embed)

        async def get_website_choice():
            with open('possibilities.json') as file:
                possibilities = json.load(file)
            try:
                website_choice = await bot.wait_for('message', check=check, timeout=30)
                website_choice = website_choice.content
                if website_choice and website_choice in possibilities['otomoto']:
                    website_choice = 'otomoto'
                elif website_choice and website_choice in possibilities['olx']:
                    website_choice = 'olx'
                return website_choice.lower()
            except asyncio.TimeoutError:
                return None

        async def get_car_brand():
            with open('brands.json') as file:
                brands = json.load(file)
            try:
                car_brand = await bot.wait_for('message', check=check, timeout=30)
                car_brand = car_brand.content
                for brand, details in brands["brands"].items():
                    if car_brand in details["values"]:
                        return details["url_prefix"]
                return None
            except asyncio.TimeoutError:
                return None

        def check(m):
            return m.author == user and m.channel == message.channel

        _website_choice = await get_website_choice()

        # CASE OTOMOTO
        if _website_choice == 'otomoto':
            await message.channel.send("You chose otomoto.pl\nEnter the car brand:")
            _car_brand = await get_car_brand()
            await _scrape_otomoto(message.channel, _car_brand)

        # CASE OLX
        elif _website_choice == 'olx':
            await message.channel.send("You chose olx.pl\nEnter the car brand:")
            _car_brand = await get_car_brand()
            await scrape_olx(message.channel, _car_brand)

        # CASE WRONG WEBSITE
        else:
            await message.channel.send("Invalid choice. Please try again.")

    await bot.process_commands(message)


@bot.command(name="help")
async def bot_help(ctx):
    embed = discord.Embed(title='Bot Help', description='List of available commands:', color=discord.Color.blue())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1090484337897648178/1109444270261284934/logov2.png")
    embed.add_field(name='/olxchart', value='Chart for OLX', inline=False)
    embed.add_field(name='/olxpiechart', value='Pie Chart for OLX', inline=False)
    embed.add_field(name='/otomotochart', value='Chart for Otomoto', inline=False)
    embed.add_field(name='/otomotopiechart', value='Pie Chart for Otomoto', inline=False)

    await ctx.send(embed=embed)


@bot.command(name='jp2')
async def say_hello(ctx):
    embed = discord.Embed(title='JP2GMD', color=discord.Color.yellow())
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1087723173853798461/1109923636200079491/swiety-jan-pawel-ii-papiez-ikona-dwustronna-z-litania-format-a4.png")
    await ctx.send(embed=embed)


@bot.command(name='olx')
async def scrape_olx(ctx, car_brand):
    await ctx.send("...Scraping data from olx.pl...")
    # Call the scrape function
    links = get_ad_links(car_brand, 10)
    embedList = []

    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, images = scrapeOlx(link)
        embed = discord.Embed(title=f"{brand} {model} ({year})",
                              description=f"Mileage: {mileage} \nEngine Size: {engine_size}\nFuel Type: {fuel_type}\nHorse Power: {horse_power}\nPrice: {price}")

        embed.add_field(name="Ad Link:", value=link)
        # Loop through the images and add a new image field for each one
        for image in images:
            embed.set_image(url=image)
            embedList.append(embed)
            if len(embedList) == 10:
                await ctx.send(embeds=embedList)
                embedList = []

    if embedList:
        await ctx.send(embeds=embedList)


@bot.command(name='otomoto')
async def _scrape_otomoto(ctx, car_brand):
    await ctx.send("...Scraping data from otomoto.pl...")
    ad_data = scrape_otomoto(car_brand, 10)
    embedList = []

    for item in ad_data:
        if all(value for value in item.values()):
            title = f"{item['brand']} {item['model']} ({item['year']})"
            description = f"Mileage: {item['mileage']}\n" \
                          f"Engine Size: {item['engine_size']}\n" \
                          f"Fuel Type: {item['fuel_type']}\n" \
                          f"Horse Power: {item['horse_power']}\n" \
                          f"Price: {item['price']}"

            embed = discord.Embed(title=title, description=description.strip())
            embed.add_field(name="Ad Link:", value=item['ad_link'])
            embed.set_image(url=item['src'])  # Add the image using the src value

            embedList.append(embed)
            if len(embedList) == 10:
                await ctx.send(embeds=embedList)
                embedList = []

    if embedList:
        await ctx.send(embeds=embedList)


# CHARTS
@bot.command(name='olxbarchart')
async def scrape_olxchart(ctx):
    await olx_bar_chart(ctx)


@bot.command(name='olxpiechart')
async def scrape_olxchart(ctx):
    await olx_pie_chart(ctx)


@bot.command(name='otomotobarchart')
async def scrape_otomotochart(ctx):
    await otomoto_bar_chart(ctx)


@bot.command(name='otomotopiechart')
async def scrape_otomotopiechart(ctx):
    await otomoto_pie_chart(ctx)


load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))
