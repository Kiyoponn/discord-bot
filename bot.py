import discord
from discord import option
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

# Startup message


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# Commands
# Direct message command
@bot.command()
@commands.has_permissions(administrator=True)
@option("title", discord.SlashCommandOptionType.string, description="The message title", required=True)
@option("message", discord.SlashCommandOptionType.string, description="The message body", required=True)
async def dm(ctx, title, message):
    """Message the users with role @DMS."""
    member: discord.Member

    async for member in ctx.guild.fetch_members():
        memberRoles = [role.name for role in member.roles]
        if "DMS" in memberRoles or "DMs" in memberRoles or "Dms" in memberRoles or "dms" in memberRoles:
            channel = await member.create_dm()
            try:
                await channel.send(f'\n**{title}**\n{message}\n\n*- {ctx.author.name}*')
                embedSuccess = discord.Embed(
                    description=f'Message sent to *{member.mention}*. :thumbsup:',
                    colour=discord.Colour.green()
                )
                await ctx.respond(embed=embedSuccess, delete_after=8.0)

            except:
                embedFail = discord.Embed(
                    description=f'I couldn\'t send message to *{member.mention}*, please tell them to turn on their DMs.',
                    colour=discord.Colour.red()
                )
                await ctx.respond(embed=embedFail, delete_after=16.0)


# Purge command
@bot.command()
@commands.has_permissions(administrator=True)
@option("amount", discord.SlashCommandOptionType.integer, description="How much of message to delete", required=True)
async def purge(ctx, amount: int):
    """Deletes message in bulk (limit 100)."""
    if amount > 100:
        amount = 100

    counter = 0
    async for _ in ctx.channel.history(limit=100):
        counter += 1

    if counter == 0:
        embedMsg = discord.Embed(
            description=f'The chat is already clean. :wink:',
            colour=discord.Colour.green()
        )
        await ctx.respond(embed=embedMsg, delete_after=2.0)
    else:
        await ctx.channel.purge(limit=amount + 1)
        embedMsg = discord.Embed(
            description=f':wastebasket: Deleted {counter} message(s).',
            colour=discord.Colour.red()
        )
        await ctx.respond(embed=embedMsg, delete_after=2.0)


# Environment variable
bot.run(os.environ['TOKEN'])
