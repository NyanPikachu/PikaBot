import discord
from discord.ext import commands
import random
import json
def developer()
    def wrapper(ctx):
        with open('data/devs.json') as f:
            devs = json.load(f)
        if ctx.author.id in devs:
            return True
        raise commands.MissingPermissions('Sorry, this command is only available for developers.')
    return commands.check(wrapper)
    
def paginate(text: str):
    '''A simple text paginator'''
    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr
    if appd_index != len(text) - 1:
        pages.append(text[last:curr])
    return list(filter(lambda a: a != '', pages))
    
def random_color()
    color = ('#%06x' % random.randint(8, 0xFFFFFF)
    color = int(color[1:], 16)
    color = discord.Color(value=color)
    return color
