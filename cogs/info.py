import discord
from discord.ext import commands

class info:
    '''Info related commands!'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['ui'], no_pm=True)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member : discord.Member=None):
        '''Get information about a member of a server'''
        server = ctx.guild
        user = member or ctx.message.author
        avi = user.avatar_url
        roles = sorted(user.roles, key=lambda c: c.position)

        for role in roles:
            if str(role.color) != "#000000":
                color = role.color
        if 'color' not in locals():
            color = 0

        rolenames = ', '.join([r.name for r in roles if r.name != "@everyone"]) or 'None'
        time = ctx.message.created_at
        desc = '{0} is chilling in {1} mode.'.format(user.name, user.status)
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1

        em = discord.Embed(colour=color, description=desc, timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Member No.',value=str(member_number),inline = True)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Roles', value=rolenames, inline=True)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url=guild.icon_url)

        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(em)
            for page in em_list:
                await ctx.send(page)
                
    @commands.command(aliases=['server','si','svi'], no_pm=True)
    @commands.guild_only()
    async def serverinfo(self, ctx, guild_id : int=None):
        '''See information about the server.'''
        server = self.bot.get_server(id=guild_id) or ctx.guild
        total_users = len(guild.members)
        online = len([m for m in guild.members if m.status != discord.Status.offline])
        text_channels = len([x for x in guild.channels if isinstance(x, discord.TextChannel)])
        voice_channels = len([x for x in guild.channels if isinstance(x, discord.VoiceChannel)])
        categories = len(guild.channels) - text_channels - voice_channels
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = "Since {}. That's over {} days ago!".format(guild.created_at.strftime("%d %b %Y %H:%M"), passed)
        
        for role in roles:
            if str(role.color) != "#000000":
                color = role.color
        if 'color' not in local
        
        colour = color
        
        data = discord.Embed(description=created_at,colour=colour)
        data.add_field(name="Region", value=str(guild.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Categories", value=categories)
        data.add_field(name="Roles", value=len(guild.roles))
        data.add_field(name="Owner", value=str(guild.owner))
        data.set_footer(text="Server ID: " + str(guild.id))
        data.set_author(name=guild.name, icon_url=None or guild.icon_url)
        data.set_thumbnail(url=None or guild.icon_url)
        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            em_list = await embedtobox.etb(data)
            for page in em_list:
                await ctx.send(page)
     
    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member : discord.Member=None):
        '''Returns someone's avatar url'''
        member = member or ctx.author
        av = member.avatar_url
        if ".gif" in av:
            av += "&f=.gif"
        color = await ctx.get_dominant_color(av)
        em = discord.Embed(url=av, color=color)
        em.set_author(name=str(member), icon_url=av)
        em.set_image(url=av)
        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(em)
            for page in em_list:
                await ctx.send(page)
            try:
                async with ctx.session.get(av) as resp:
                    image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, 'avatar.png'))
            except discord.HTTPException:
                await ctx.send(av)
    
def setup(bot):
    bot.add_cog(info(bot))
