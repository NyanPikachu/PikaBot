import discord
from discord.ext import commands
import os
from ext import utils

class Utility:
	'''Utility commands!'''
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user: discord.Member=None):
		"""shows avatar of a certain user"""
		if not user:
			user = ctx.author
		av = user.avatar_url
		em = discord.Embed(color=utils.random_color())
		em.set_athor(name=f'{ctx.author.name}\'s avatar!')
		em.set_image(url=av)
		await ctx.send(embed=em)

	@commands.command(aliases=['ui'])
	@commands.guild_only()
	async def userinfo(self, ctx, user: discord.Member=None):
		"""user info"""
		if not user:
			user = ctx.author
		embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=utils.random_color())
		embed.add_field(name="Name", value=user.name, inline=True)
		embed.add_field(name="ID", value=user.id, inline=True)
		embed.add_field(name="Status", value=user.status, inline=True)
		embed.add_field(name="Game", value=str(user.activity))
		embed.add_field(name="Highest role", value=user.top_role.name or "Empty")
		embed.add_field(name="Joined", value=user.joined_at)
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def serverinfo(self, ctx): 
		"""server info"""
		embed = discord.Embed(name=f"{user.name}'s info", description="Here's what I found.", color=utils.random_color())
		embed.set_author(name="Pika Bot")
		embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
		embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
		embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
		embed.add_field(name="Members", value=len(ctx.message.guild.members))
		embed.add_field(name="Owner", value=(ctx.message.guild.owner))
		embed.add_field(name="Created at", value=(ctx.message.guild.created_at))
		embed.set_thumbnail(url=ctx.message.guild.icon_url)
		await ctx.send(embed=embed)

	@commands.command()
	async def id(self, ctx, identity: discord.Member or discord.TextChannel):
		"""Returns a channel or user id"""
		await ctx.send(f'id: `{identity.id}`')

def setup(bot):
    bot.add_cog(Utility(bot))
