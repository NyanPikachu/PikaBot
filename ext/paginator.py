import discord
from collections import OrderedDict
import asyncio


class Paginator:
    def __init__(self, ctx, base, embeds, obj):
        self.ctx = ctx
        self.bot = ctx.bot
        self.base = base
        self.pointers = ['👈','👉','❌']
        self.embeds = embeds
        self.cursor = 0
        self.obj = obj

    async def _add_handler(self):
        def reaction_check(reaction,user):
            return user == self.ctx.author and reaction.ctx.id == self.base.id and reaction.emoji in self.pointers
        while True: 
            reaction, user = await self.bot.wait_for(self.obj, event='reaction_add', check=reaction_check)
            op = self.pointers.index(reaction.emoji)
            if op == 1 and self.cursor < len(self.embeds) - 1:
                self.cursor += 1
                await self.base.edit(embed=self.embeds[self.cursor])
            elif op == 0 and self.cursor > 0:
                self.cursor -= 1
                await self.base.edit(embed=self.embeds[self.cursor])
            elif op == 2:
                await self.base.delete()
                break    
            else:
                pass

    async def _remove_handler(self):
        def reaction_check(reaction,user):
            return user == self.ctx.author and reaction.ctx.id == self.base.id and reaction.emoji in self.pointers
        while True: 
            reaction, user = await self.bot.wait_for(self.obj, event='reaction_remove', check=reaction_check)
            op = self.pointers.index(reaction.emoji)
            if op == 1 and self.cursor < len(self.embeds) - 1:
                self.cursor += 1
                await self.base.edit(embed=self.embeds[self.cursor])
            elif op == 0 and self.cursor > 0:
                self.cursor -= 1
                await self.base.edit(embed=self.embeds[self.cursor])
            else:
                pass                    

    async def run(self, content=None):
        content = content or None
        await self.base.edit(content=content,embed=self.embeds[0])
        for pointer in self.pointers:
            await self.base.add_reaction(pointer)
        asyncio.ensure_future(self._add_handler())
        asyncio.ensure_future(self._remove_handler())