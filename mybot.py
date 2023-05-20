import discord
from discord.ext import commands
from single_page import scrapeOlx
from ad_links import get_ad_links
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import Counter
import networkx as nx
import os
from dotenv import load_dotenv
from otomoto import scrape_otomoto, _get_ad_links

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="help")
async def bot_help(ctx):
    embed = discord.Embed(title='Bot Help', description='List of available commands:', color=discord.Color.blue())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1090484337897648178/1109444270261284934/logov2.png")
    embed.add_field(name='/olx', value='Scraps the olx', inline=False)
    embed.add_field(name='/otomoto', value='Scraps otomoto', inline=False)
    # Add more fields for other commands



    await ctx.send(embed=embed)


@bot.command(name='jp2')
async def say_hello(ctx):
    await ctx.send(f'JP2GMD')


@bot.command(name='olx')
async def scrape_olx(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
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
async def _scrape_otomoto(ctx):
    ad_data = scrape_otomoto()
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


@bot.command(name='olxchart')
async def scrape_olxchart(ctx):
    # Call the scrape function
    links = get_ad_links()
    data = []
    for link in links:
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, img = scrapeOlx(link)
        data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

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
        brand, model, year, mileage, engine_size, fuel_type, horse_power, price, img = scrapeOlx(link)
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

    plt.savefig('network_plot.png')

    # Send the plot as a message
    with open('network_plot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

    plt.show()


load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))
