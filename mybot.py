import discord
from discord.ext import commands
from discord import Embed

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import Counter
import networkx as nx
import os
from dotenv import load_dotenv
import asyncio
import json

from Scrappers.single_page import scrapeOlx
from Scrappers.ad_links import get_ad_links
from Scrappers.otomoto import scrape_otomoto

from Messages.chart_message import generate_chart_message

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
    embed.add_field(name='/olxchart', value='Chart for olx', inline=False)
    embed.add_field(name='/olxscatter', value='Comparing chart', inline=False)
    embed.add_field(name='/otomotochart', value='Chart for otomoto', inline=False)

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
def preprocess_data(ad_data):
    data = []

    for item in ad_data:
        if all(value is not None for value in item):
            brand = item[0]
            model = item[1]
            year = item[2]
            mileage = item[3]
            engine_size = item[4]
            fuel_type = item[5]
            horse_power = item[6]
            data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    return data


@bot.command(name='olxchart')
async def scrape_olxchart(ctx):
    estimated_time = 10  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    # Call the scrape function
    links = get_ad_links(None, 10)
    ad_data = [scrapeOlx(link) for link in links]
    data = preprocess_data(ad_data)

    # Get a list of all the brands
    brands = [record[0] for record in data]

    # Count the number of cars by brand
    brand_counts = Counter(brands)

    # Create a larger figure to accommodate all the bars
    num_brands = len(brand_counts)
    min_bar_width = 0.3  # Minimum width of the bars
    bar_width = max(min_bar_width, 0.8 / num_brands)
    figsize_width = max(8, num_brands * bar_width * 1.5)  # Minimum width of 8 inches
    plt.figure(figsize=(figsize_width, 6))
    plt.subplots_adjust(bottom=0.3, left=0.1)  # Adjust margins

    # Create a bar chart
    plt.bar(brand_counts.keys(), brand_counts.values(), width=bar_width)

    # Set the title and axis labels
    plt.title('Number of Cars by Brand')
    plt.xlabel('Brand')
    plt.ylabel('Count')

    # Rotate and align the X-axis tick labels
    plt.xticks(rotation=45, ha='right')

    # Set the Y-axis tick formatter to show only whole numbers
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Save the plot to a file
    plt.savefig('bar_chart.png')

    # Send the plot as a message
    with open('Images/bar_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    # Show the plot
    plt.show()


@bot.command(name='olxscatter')
async def scrape_olxscatter(ctx):
    estimated_time = 10  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    # Call the scrape function
    links = get_ad_links(None, 10)
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, img = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    # Convert the year values to integers
    data = [(brand, model, int(year), mileage, engine_size, fuel_type, horse_power) for
            brand, model, year, mileage, engine_size, fuel_type, horse_power in data]

    # Sort the data based on the year in ascending order
    data.sort(key=lambda x: x[2])

    # Get a list of all the mileage and year values
    mileage = [int(record[3].replace(',', '').replace(' km', '').replace(' ', '')) for record in
               data]  # Convert mileage to numeric type
    year = [record[2] for record in data]

    # Create a scatter plot
    plt.scatter(year, mileage)

    # Set the title and axis labels
    plt.title('Mileage vs Year')
    plt.xlabel('Year')
    plt.ylabel('Mileage (km)')

    # Set the Y-axis tick values and labels based on the scraped mileage values
    max_mileage = max(mileage)
    step_size = max_mileage // 5  # Divide the maximum mileage into 5 ticks
    y_ticks = list(range(0, max_mileage + step_size, step_size))
    y_labels = [f'{value / 1000}k' for value in
                y_ticks]  # Example labels showing mileage in thousands, adjust as needed

    plt.yticks(y_ticks, y_labels)

    # Set the X-axis tick locator to show only whole numbers
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add more space to the left side of the plot
    plt.subplots_adjust(left=0.2, bottom=0.1)

    # Save the plot to a file
    plt.savefig('Images/scatter_plot.png')

    # Send the plot as a message
    with open('Images/scatter_plot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    # Show the plot
    plt.show()


@bot.command(name='olxnetwork')
async def scrape_olxnetwork(ctx):
    estimated_time = 10  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    # Call the scrape function
    links = get_ad_links(None, 10)
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, img = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for each brand, model, and fuel type
    for brand, model, year, mileage, engine_size, fuel_type, horse_power in data:
        G.add_node(brand)
        G.add_node(model)
        G.add_node(fuel_type)

        # Add edges between the nodes
        G.add_edge(brand, model)
        G.add_edge(model, fuel_type)

    # Set the positions of the nodes using the spring layout algorithm
    pos = nx.spring_layout(G)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw_networkx(G, pos, node_color='lightblue', node_size=800, font_size=10, with_labels=True)

    # Set the axis labels and title
    plt.xlabel('Car Brands, Models, and Fuel Types', fontsize=14)
    plt.ylabel('')
    plt.title('Relationships between Car Brands, Models, and Fuel Types', fontsize=16)

    # Remove the axes and show the plot
    plt.axis('off')

    plt.savefig('Images/network_plot.png')

    # Send the plot as a message
    with open('Images/network_plot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    plt.show()


@bot.command(name='otomotochart')
async def scrape_otomotochart(ctx):
    estimated_time = 10  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    ad_data = scrape_otomoto(None, 10)
    data = []

    for item in ad_data:
        if all(value is not None for value in item.values()):
            brand = item['brand']
            data.append(brand)

    brand_counts = Counter(data)

    num_brands = len(brand_counts)
    min_bar_width = 0.3
    bar_width = max(min_bar_width, 0.8 / num_brands)
    figsize_width = max(8, num_brands * bar_width * 1.5)
    plt.figure(figsize=(figsize_width, 6))
    plt.subplots_adjust(bottom=0.3, left=0.1)

    plt.bar(brand_counts.keys(), brand_counts.values(), width=bar_width)

    plt.title('Number of Cars by Brand (Otomoto)')
    plt.xlabel('Brand')
    plt.ylabel('Count')

    plt.xticks(rotation=45, ha='right')

    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.savefig('Images/otomoto_bar_chart.png')

    with open('Images/otomoto_bar_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    plt.show()


@bot.command(name='otomotopiechart')
async def scrape_otomotopiechart(ctx):
    estimated_time = 10  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    ad_data = scrape_otomoto(None, 10)
    data = []

    for item in ad_data:
        if all(value is not None for value in item.values()):
            brand = item['brand']
            data.append(brand)

    brand_counts = Counter(data)

    labels = brand_counts.keys()
    values = brand_counts.values()

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', pctdistance=0.90)

    plt.title('Distribution of Cars by Brand (Otomoto)')

    plt.savefig('Images/otomoto_pie_chart.png')

    with open('Images/otomoto_pie_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    plt.show()


load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))
