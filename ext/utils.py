import discord
from discord.ext import commands
import random
import json

def developer():
	def wrapper(ctx):
		with open('data/devlist.json') as f:
			devs = json.load(f)
			if ctx.author.id in devs:
				return True
				raise commands.MissingPermissions('Sorry, this command is only available for developers.')
			return commands.check(wrapper)

def random_color():
	color = random.randint(1, 0xffffff)
	return discord.Colour(color)