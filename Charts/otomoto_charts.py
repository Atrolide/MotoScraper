from Messages.chart_message import generate_chart_message
import discord
from Scrappers.Otomoto.otomoto import scrape_otomoto
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

async def otomoto_bar_chart(ctx):
    estimated_time = 80  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    ad_data = scrape_otomoto(None, 50)
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

async def otomoto_pie_chart(ctx):
    estimated_time = 80  # Estimated time in seconds

    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)

    ad_data = scrape_otomoto(None, 50)
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