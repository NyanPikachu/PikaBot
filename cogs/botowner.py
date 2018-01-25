import discord
from discord.ext import commands

class owneronly:
    '''commands for bot owner only'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str)
       """Evaluates python code"""

       env = {
           'bot': self.bot,
           'ctx': ctx,
           'channel': ctx.channel,
           'author': ctx.author,
           'guild': ctx.guild,
           'message': ctx.message,
           '_': self._last_result,
           'source': inspect.getsource
       }

       env.update(globals())

       body = self.cleanup_code(body)
       if edit: await self.edit_to_codeblock(ctx, body)
       stdout = io.StringIO()
       err = out = None

       to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

       try:
           exec(to_compile, env)
       except Exception as e:
           err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
           return await err.add_reaction('\u2049')

       func = env['func']
       try:
           with redirect_stdout(stdout):
               ret = await func()
       except Exception as e:
           value = stdout.getvalue()
           err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
       else:
           value = stdout.getvalue()
           if self.bot.token in value:
               value = value.replace(self.bot.token, "[EXPUNGED]")
           if ret is None:
               if value:
                   try:
                       out = await ctx.send(f'```py\n{value}\n```')
                   except:
                       paginated_text = ctx.paginate(value)
                       for page in paginated_text:
                           if page == paginated_text[-1]:
                               out = await ctx.send(f'```py\n{page}\n```')
                               break
                           await ctx.send(f'```py\n{page}\n```')
           else:
               self._last_result = ret
               try:
                   out = await ctx.send(f'```py\n{value}{ret}\n```')
               except:
                   paginated_text = ctx.paginate(f"{value}{ret}")
                   for page in paginated_text:
                       if page == paginated_text[-1]:
                           out = await ctx.send(f'```py\n{page}\n```')
                           break
                       await ctx.send(f'```py\n{page}\n```')

       if out:
           await out.add_reaction('\u2705')  # tick
       elif err:
           await err.add_reaction('\u2049')  # x
       else:
           await ctx.message.add_reaction('\u2705')
    
    async def edit_to_codeblock(self, ctx, body, pycc='blank'):
        if pycc == 'blank':
            msg = f'{ctx.prefix}eval\n```py\n{body}\n```'
        else:
            msg = f'{ctx.prefix}cc make {pycc}\n```py\n{body}\n```'
        await ctx.message.edit(content=msg)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


def setup(bot):
    bot.add_cog(owneronly(bot))
