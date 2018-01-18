import discord
from discord.ext import commands
import asyncio
import pickle
import random
import io
import os
import sys
import traceback
import textwrap
from contextlib import redirect_stdout

#eval!!!
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')
bot = commands.Bot(command_prefix="$", description="This is an example bot", owner_id=279974491071709194)

devs = [
    279974491071709194
]

@bot.command()
@commands.is_owner()
async def eval(ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')
                


#normal commands.ill put into cogs later
@bot.event
async def on_ready():
    print("Bot is online!")
    


@bot.command()
async def ping(ctx):
    """Latency check"""
    embed = discord.Embed(title="Pong!", description=f"{bot.ws.latency* 1000:.4f} ms", color=0x00ff00)
    await ctx.send(embed=embed)
    
@bot.command()
async def say(ctx, msg: str):
    """owner only command- print a message"""
    await ctx.message.delete()
    await ctx.send(msg)
    
@bot.command()
async def coinflip(ctx):
    """Flips a coin!"""
    flip = random.choice(["Heads", "Tails"])
    await ctx.send(flip)
    
@bot.command()
async def hug(ctx, user: discord.Member=None):
    """hugs a user"""
   if not user:
      await ctx.send(f"Please mention someone for this command to work {ctx.author.mention}" )
   embed = discord.Embed(title="Hug!".format(user.name), description= f"{ctx.author} has sent {user} a hug !", color=0xffb6c1)
   embed.set_thumbnail(url=user.avatar_url)
   await ctx.send(embed=embed)
         
@bot.command()
async def info(ctx, user: discord.Member=None):
    """user info"""
    if not user:
        user = ctx.author
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
    
@bot.command()
async def serverinfo(ctx): 
    """server info"""
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Pika Bot")
    embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    await ctx.send(embed=embed)
    
bot.run(os.environ.get("TOKEN"))
