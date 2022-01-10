import discord 
from discord.ext import commands 
import os 
import time
import asyncio

bot= commands.Bot(command_prefix='$',case_insensitive=True)



@bot.event
async def on_ready():
  print(f'logged in as {bot.user}')
  await bot.change_presence(activity=discord.Game(name='?help'))
  
  
@bot.command(help='Pong!')
async def ping(ctx):
     msg= await ctx.channel.send("Pong!")
     await asyncio.sleep(0.5)
     await msg.edit(content=f'Pong!``` In {round(bot.latency * 1000)}ms```')



@bot.command(pass_context=True,help='Shows Creator\'s info.[cr]',aliases=['cr'])
async def creator(ctx):
  rid='<@821068903794737214>'
  e =  discord.Embed(title='Creator:',description=f'||{rid}||',color=discord.Color.red())
  e.set_thumbnail(url='https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSOwWVi9DS25CaBpNORNEKEsTCIxJ1uwcCqNI4_xe-EUTB769lp')
  await ctx.channel.send(embed=e)


@bot.command() 
async def pingme(ctx):
  memberx = '<@854022191809036288>'
  while(True):
    await ctx.channel.send(f'Hi {memberx}') 

@bot.command(help='Shows the User\'s avatar[av].',aliases=['av'])
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    e = discord.Embed(title=f'{avamember.name}',description='',color=discord.Color.blurple())
    e.set_image(url=userAvatarUrl)
    await ctx.channel.send(embed=e)
    
    
  
@bot.command(pass_context=True,help='Shows Server\'s name.[sn]',aliases=['sn'])
async def server_name(ctx):
  e = discord.Embed(title=f'{ctx.author.guild.name}',description='',color=discord.Color.blurple())
  e.set_thumbnail(url=ctx.author.guild.icon_url)
  await ctx.channel.send(embed=e)


@bot.command(pass_context=True,help='Shows the number of members in your server.')
async def members(ctx):
    embedVar = discord.Embed(title=f'{ctx.author.guild.name}',description=f'{ctx.guild.member_count} members.', color=0xFF0000)
    await ctx.send(embed=embedVar)
    
    
@bot.command(pass_context=True,help='Shows full info regarding members (bots,users,total).[finfo]',aliases=['finfo'])
async def fullinformation(ctx):
  membersInServer = ctx.guild.members
        # Filter to the list, returns a list of bot-members
  tmember=ctx.guild.member_count
  botsInServer = list(filter(filterOnlyBots, membersInServer))

  botsInServerCount = len(botsInServer)
        # (Total Member count - bot count) = Total user count
  usersInServerCount = ctx.guild.member_count - botsInServerCount
  embed=discord.Embed(title=f'{ctx.author.guild.name}',description=f'Total members : {tmember}\nUsers : {usersInServerCount}\nBots : {botsInServerCount}',color=discord.Color.blurple())
  await ctx.channel.send(embed=embed)

def filterOnlyBots(member):
    return member.bot
    
    
@bot.command(pass_context=True,help='Shows your name.')
async def name(ctx):
  await ctx.channel.send(f'{ctx.author.mention} Looks like you forget things much quick, buckaroo\n{ctx.author.name} is your name ✨')



@bot.command(pass_context=True,help='Shows server\'s info.[sinfo]',aliases=['sinfo'])
async def serverinformation(ctx):
  name = str(ctx.guild.name)
  owner = ctx.guild.owner
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description='',
      color=discord.Color.blue()
    )
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  await ctx.send(embed=embed)


@bot.command(help='Shows your account\'s age.[ma]',aliases=['ma'])
async def myage(ctx):
   e = discord.Embed(title=f'{ctx.author.created_at}',description='',color=discord.Color.blurple())
   await ctx.send(embed=e)

@bot.command(help='Shows a particular user\'s full info.[ui]',aliases=['ui'])
async def userinfo(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)



@bot.command(help='Kicks a member out of the server.')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} is kicked.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, but if you want to use this command you need to have **Kick Members** permission.")





@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in the member.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permission.")

#The below code bans player.
@bot.command(help='Bans a member from your server.')
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.channel.send(f'{member.mention} is banned.')
#The below code unbans player.
@bot.command(help='Unbans a member from your server.')
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#The below code runs the bot.


@bot.command(help="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" You have been muted from: {guild.name} reason: {reason}")
    
    
    
    
@bot.command(help="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f"You have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="Unmuted", description=f"Unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)





  
bot.run(os.getenv("Token"))