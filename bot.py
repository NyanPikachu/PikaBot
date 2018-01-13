import discord
from discord.ext import commands
import asyncio
import pickle
import random
import os
import sys

bot = commands.Bot(command_prefix="$", description="This is an example bot", owner_id=279974491071709194)

@bot.event
async def on_ready():
    print("Bot is online!")
    
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f"Pong!{bot.ws.latency* 1000:.4f} ms")
    
    
@bot.command(pass_context=True)
async def say(ctx, msg: str):
    await ctx.message.delete()
    await ctx.send(msg)
    
@bot.command(pass_context=True)
async def coinflip(ctx):
    flip = random.choice(["Heads", "Tails"])
    await ctx.send(flip)
    
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
    
@bot.command(pass_context=True)
async def serverinfo(ctx): 
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Pika Bot")
    embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    await ctx.send(embed=embed)
    
bot.run(os.environ.get("TOKEN"))
