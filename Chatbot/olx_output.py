import discord
from Scrappers.Olx.single_page import scrapeOlx
from Scrappers.Olx.ad_links import get_ad_links
from Messages.chart_message import generate_chart_message

async def olx_output(ctx, car_brand):
    estimated_time = 10  # Estimated time in seconds
    # Generate the chart message and get the previous message object
    previous_message = await generate_chart_message(ctx, estimated_time)
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


    await previous_message.edit(content=":white_check_mark: Scraping completed!")
    if embedList:
        await ctx.send(embeds=embedList)