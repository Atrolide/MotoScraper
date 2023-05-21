import discord
from Scrappers.Otomoto.otomoto import scrape_otomoto

async def otomoto_output(ctx, car_brand):
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