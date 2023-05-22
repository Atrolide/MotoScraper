import discord

async def help_display(ctx):
    embed = discord.Embed(title='Bot Help', description='To start chatting with me, tag me **@Moto Scraper!**', color=discord.Color.blue())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1090484337897648178/1109444270261284934/logov2.png")
    embed.add_field(name='', value='\u200b', inline=False)
    embed.add_field(name='List of available commands:', value='\u200b', inline=False)
    embed.add_field(name='/olxchart', value='Chart for OLX\u200b', inline=True)
    embed.add_field(name='/olxpiechart', value='Pie Chart for OLX\u200b', inline=True)
    embed.add_field(name='/otomotochart', value='Chart for Otomoto\u200b', inline=True)
    embed.add_field(name='/otomotopiechart', value='Pie Chart for Otomoto\u200b', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=False)  # Add more spacing between fields
    embed.set_footer(text='Powered by Moto Scraper')

    await ctx.send(embed=embed)

