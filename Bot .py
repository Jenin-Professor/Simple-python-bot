import discord
from discord.ext import commands
from itertools import cycle
import asyncio
import functools
import itertools
import math
import random
import youtube_dl
from async_timeout import timeout

TOKEN = "Enter your Bot Token"

Bot_name = "Enter your bot's name"


client = commands.Bot(command_prefix = "#")



client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="#help"))
	print("Bot is ready")

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason = None ):
	await member.kick(reason=reason)
	await ctx.send(f"Kicked {member.mention} from this server")

@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason = None ):

	await member.ban(reason=reason)
	await ctx.send(f"Banned {member.mention} from this server ")


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send("Unbanned someone")
			return


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
	if not member:
		await ctx.send("Please specify a member")
		return
	role = discord.utils.get(ctx.guild.roles, name="muted")
	await member.add_roles(role)
	await ctx.send(" `` Muted an insect `` ")



@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
	if not member:
		await ctx.send("Please specify a member")
		return
	role = discord.utils.get(ctx.guild.roles, name="muted")
	await member.remove_roles(role)
	await ctx.send("``unmuted someone``")






@client.command(aliases = ['pl'])
async def poll(ctx,*, msg):
	channel = ctx.channel
	try:
		op1 , op2 = msg.split("or")
		txt = f"React with ✅ for {op1} or ❎ for {op2}" 
	except:
		await channel.send("Please make it like this: [Choice1] or [Choice2]")
		return



	embed = discord.Embed(title="Poll", description = txt,colour = discord.Colour.red())
	message_ = await channel.send(embed=embed)
	#message_ = await ctx.send("React here ")
	await message_.add_reaction("✅")
	await message_.add_reaction("❎")
	await ctx.message.delete()

	await asyncio.sleep(10)
	cache_msg = await ctx.fetch_message(message_.id)
	rs = cache_msg.reactions

	users1 = await rs[0].users().flatten()
	users2 = await rs[1].users().flatten()
	op1p = len(users1)
	op2p = len(users2)

	if op1p > op2p:
		await ctx.send(op1+ " has won!")
	elif op1p < op2p:
		await ctx.send(op2+ " has won!")
	else:
		await ctx.send("It's a tie!")



@client.command(pass_context=True)
async def coinflip(ctx):
	choices = ["Heads", "Tails"]
	ranchoice = random.choice(choices)
	await ctx.send(ranchoice)

@client.command(pass_context = True)
async def say(ctx, *,msg):
	await ctx.message.delete()
	await ctx.send(msg)


@client.command(pass_context=True)
async def help(ctx):
  
  embed = discord.Embed(title="Help", color=0xFF69B4)

  embed.add_field(name= "#help_mod", value= "Shows moderation commands", inline = False)
  embed.add_field(name="#help_fun", value="Shows fun commands", inline=False)
  await ctx.send(embed=embed)


@client.command(pass_context=True)
async def hug(ctx, member : discord.Member ):
	embed = discord.Embed(title= f" {Bot_name} hugged {member}",color=0xFF69B4)
	embed.set_image(url="https://i.imgur.com/gMLlFNC.gif")
	await ctx.send(embed=embed)

@client.command(pass_context=True)
async def pat(ctx, member : discord.Member ):
	embed = discord.Embed(title= f" {Bot_name} gave pats to {member}",color=0xFF69B4)
	embed.set_image(url="https://i.imgur.com/2lacG7l.gif")
	await ctx.send(embed=embed)

@client.command(pass_context=True)
async def kiss(ctx, member : discord.Member ):
	embed = discord.Embed(title= f" {Bot_name} kissed {member}",color=0xFF69B4)
	embed.set_image(url="https://i.imgur.com/wQjUdnZ.gif")
	await ctx.send(embed=embed)
		
		
			



@client.command(pass_context=True)
async def help_mod(ctx):
  
  embed = discord.Embed(title="Help - MODERATION", color=0xFF69B4)

  embed.add_field(name= "prefix", value= "use '#' before commands", inline = False)
  embed.add_field(name="#ban", value="usage : #ban @member reason", inline=False)
  embed.add_field(name="#kick", value="usage : #kick @member reason", inline=False)
  embed.add_field(name="#unban", value="usage : #unban member#xxxx", inline=False)
  embed.add_field(name="#mute", value="usage : #mute @member", inline=False)
  embed.add_field(name="#unmute", value="usage : #unmute @member", inline=False)
  embed.add_field(name="#clear", value="usage : #clear <no of messages to be cleared>", inline=False) 
  await ctx.send(embed=embed)

@client.command(pass_context=True)
async def help_fun(ctx):
  
  embed = discord.Embed(title="Help - FUN", color=0xFF69B4)

  embed.add_field(name= "#poll", value= "usage : #poll x or y", inline = False)
  embed.add_field(name= "#coinflip", value= "use : flips a coin", inline = False)
  embed.add_field(name= "#say", value= "usage : #say <what u want the bot to say>", inline = False)
  embed.add_field(name= "#kiss", value= "usage : #kiss @member", inline = False)
  embed.add_field(name= "#hug", value= "usage : #hug @member", inline = False)
  embed.add_field(name= "#pat", value= "usage : #pat @member", inline = False)
  await ctx.send(embed=embed)


client.run(TOKEN)



