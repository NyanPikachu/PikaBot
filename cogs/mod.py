from discord.ext import commands
from .utils import checks, db, time, cache
from collections import Counter, defaultdict
from inspect import cleandoc

import re
import json
import discord
import enum
import datetime
import asyncio
import argparse, shlex
import logging


#converters

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            can_execute = ctx.author.id == ctx.bot.owner_id or \
                          ctx.author == ctx.guild.owner or \
                          ctx.author.top_role > m.top_role

            if not can_execute:
                raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
            return m.id

class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        ban_list = await ctx.guild.bans()
        try:
            member_id = int(argument, base=10)
            entity = discord.utils.find(lambda u: u.user.id == member_id, ban_list)
        except ValueError:
            entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)
        if entity is None:
            raise commands.BadArgument("Not a valid previously-banned member.")
        return entity

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret

#commands go here! i'm just lazy don't judge me :(

class mod:
    '''Moderation commands!'''
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: ActionReason = None):
        """Kicks a member
        
        This kick command needs a reason , however if non is provided the bot will just tell the action preformer
        
        """
        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await member.kick(reason=reason)
        await ctx.send('\N{OK HAND SIGN}')
        
    
    
    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason: ActionReason = None):
        """Bans a member from the server.
        You can also ban from ID to ban regardless whether they're
        in the server or not.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.ban(discord.Object(id=member), reason=reason)
        await ctx.send('\N{OK HAND SIGN}')

    
    
    
    
    
    
def setup(bot):
    bot.add_cog(mod(bot))
