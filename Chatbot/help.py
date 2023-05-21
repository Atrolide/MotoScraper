import discord

async def help_display(ctx):
    embed = discord.Embed(title='Bot Help', description='To start chatting with me, tag me @Moto Scraper!',
                          color=discord.Color.blue())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1090484337897648178/1109444270261284934/logov2.png")
    embed.add_field(name='', value='List of available commands:', inline=False)
    embed.add_field(name='/olxchart', value='Chart for OLX', inline=False)
    embed.add_field(name='/olxpiechart', value='Pie Chart for OLX', inline=False)
    embed.add_field(name='/otomotochart', value='Chart for Otomoto', inline=False)
    embed.add_field(name='/otomotopiechart', value='Pie Chart for Otomoto', inline=False)

    await ctx.send(embed=embed)