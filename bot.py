import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

client = commands.Bot( command_prefix = 'wc!' )

# Words
hello_words = [ 'Hello!', 'Hello', 'Hi!', 'Hi', 'Hey!', 'Hey', 'Привет!',
			    'Привет', 'Хай!', 'Хай', 'Хей!', 'Хэй', 'Эй!', 'Эй']

@client.event

async def on_ready():
	print("Ready!")

	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'wc!commands' ) )

@client.command( pass_context = True )

# First commands

async def hello( ctx ):
	author = ctx.message.author
	await ctx.send( f"Hello { author.mention }!" )

# clear message
@client.command( pass_context = True )

async def clear( ctx, amount = 10 ):
	await ctx.channel.purge( limit = amount )

# Kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )

# Help
@client.command( pass_context = True )
async def commands( ctx ):
	await ctx.send("wc!hello - Команда для теста")
	await ctx.send("wc!clear [messages] - Очистка чата")
	await ctx.send("wc!kick @user - Кикнуть участника")
	await ctx.send("wc!commands - эта же команда:)")
	await ctx.send("wc!join - Войти в голосовый канал")
	await ctx.send("wc!leave - Выйти из голосового канала")
	await ctx.send("wc!play [https://youtube.com/watch?v=abcdefhg] - Проиграть музыку из ютуба")

@client.command()
async def join( ctx ):
	global voice
	channel = ctx.message.author.voice.channel

	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send('Connected!')

@client.command()
async def leave( ctx ):
	channel = ctx.message.author.voice.channel

	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send('Disconnected!')

@client.command()
async def play( ctx, url : str ):
	song_there = os.path.isfile('song.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print("[info] Old file removed!")
	except PermissionError:
		print("[error] ne udalos udalit fail")
	await ctx.send('Please wait...')

	voice = get(client.voice_clients, guild = ctx.guild)

	ydl_opts = {
		'format' : 'bestaudio/best',
		"postprocessord" : [{
			"key" : "FFmpegExtractAudio",
			"preferredcodec" : "mp3",
			"preferredquality" : "192"
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("[message] Loading Music")
		ydl.download([url])

	for file in os.listdir('./'):
		if file.emdswith('.mp3'):
			name = file
			print("[Warning] Renaming File: {file}")
			os.rename(file, "song.mp3")

	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print("[log] {name} is end!"))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	song_name = name.rsplit('-', 2)
	await ctx.send(f'Сечас играет: {song_name[0]}')

client.run("Token here!")