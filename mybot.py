import discord
from discord.ext import commands
from single_page import scrapeOlx
from ad_links import get_ad_links
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx
import os
from dotenv import load_dotenv
import pandas as pd


intents = discord.Intents.default()

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='jp2')
async def say_hello(ctx):
    await ctx.send(f'JP2GMD')

# NORMAL MESSAGES 
# @bot.command(name='olx')
# async def scrape_olx(ctx):
#     # Call the scrape function
#     links = get_ad_links()
#     data = []
#     for link in links:
#         brand, model, year, mileage, engine_size, fuel_type, horse_power = scrapeOlx(link)
#         data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))
#
#     # Send each list as a separate message
#     for record in data:
#         brand, model, year, mileage, engine_size, fuel_type, horse_power = record
#         message = f"{brand} - {model} - {year} - {mileage} - {engine_size} - {fuel_type} - {horse_power}"
#         await ctx.send(message)
#

# TABLE

@bot.command(name='olx')
async def scrape_olx(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []

    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, images = scrapeOlx(link)
        embed = discord.Embed(title=f"{brand} {model} ({year})",
                              description=f"Mileage: {mileage} \nEngine Size: {engine_size}\nFuel Type: {fuel_type}\nHorse Power: {horse_power}\nPrice: {price}")

        # Loop through the images and add a new image field for each one
        for image in images:
            embed.set_image(url=image)
            print(embed)
            await ctx.send(embed=embed)




@bot.command(name='olxchart')
async def scrape_olxchart(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    # Get a list of all the brands
    brands = [record[0] for record in data]

    # Count the number of cars by brand
    brand_counts = Counter(brands)

    # Create a bar chart
    plt.bar(brand_counts.keys(), brand_counts.values())

    # Set the title and axis labels
    plt.title('Number of Cars by Brand')
    plt.xlabel('Brand')
    plt.ylabel('Count')

    # Save the plot to a file
    plt.savefig('bar_chart.png')

    # Send the plot as a message
    with open('bar_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

    # Show the plot
    plt.show()


@bot.command(name='olxscatter')
async def scrape_olxscatter(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    # Get a list of all the mileage and year values
    mileage = [record[3] for record in data]
    year = [record[2] for record in data]

    # Create a scatter plot
    plt.scatter(year, mileage)

    # Set the title and axis labels
    plt.title('Mileage vs Year')
    plt.xlabel('Year')
    plt.ylabel('Mileage')

    # Save the plot to a file
    plt.savefig('scatter_plot.png')

    # Send the plot as a message
    with open('scatter_plot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

    # Show the plot
    plt.show()


@bot.command(name='olxnetwork')
async def scrape_olxnetwork(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power = scrapeOlx(link)
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

    plt.savefig('network_plot.png')

    # Send the plot as a message
    with open('network_plot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

    plt.show()

load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))
