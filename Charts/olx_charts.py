from Messages.chart_message import generate_chart_message
import discord
from Scrappers.Olx.single_page import scrapeOlx
from Scrappers.Olx.ad_links import get_ad_links
from Scrappers.data_processor import preprocess_data
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


async def olx_pie_chart(ctx):
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

    labels = brand_counts.keys()
    values = brand_counts.values()

    # Create a larger figure to accommodate the pie chart
    plt.figure(figsize=(8, 6))

    # Create a pie chart
    plt.pie(values, labels=labels, autopct='%1.1f%%', pctdistance=0.90)

    # Set the title
    plt.title('Distribution of Cars by Brand')

    # Save the plot to a file
    plt.savefig('Images/olx_pie_chart.png')

    # Send the plot as a message
    with open('Images/olx_pie_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    # Show the plot
    plt.show()


async def olx_bar_chart(ctx):
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
    plt.savefig('Images/olx_bar_chart.png')

    # Send the plot as a message
    with open('Images/olx_bar_chart.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        await previous_message.edit(content=":white_check_mark: Chart generation completed!")

    # Show the plot
    plt.show()