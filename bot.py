import discord
from discord.ext import commands

import asyncio

from math import floor
from random import random
from time import sleep

from yandex_music import Client

from radio import Radio

# API instance
client = Client(token='y0_AgAAAAAkRDbEAAG8XgAAAADSuq1Se2RpFxjbTO2IihKJsUSBXzUXBKE')
# Get random station
_station = client.rotor_stations_dashboard()['stations'][0].station
_station_id = f'{_station.id.type}:{_station.id.tag}'
_station_from = _station.id_for_from
# Radio instance
radio = Radio(client)


config = {
    'token': 'MTAzNjA1MDE5OTc5NTIxMjQxOA.GPaZ6F.L_fK0V5vWoT-Aa7pvd1uRJwn_xGfoomTl0-yN4',
    'prefix': 't!',
}
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.command("join")
async def join(ctx):
    connected = ctx.author.voice
    if not connected:
        await ctx.send("You need to be connected in a voice channel to use this command!")
        return
    global vc
    vc = await connected.channel.connect()

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command("radio")
async def radio_on(ctx):
    server = ctx.message.guild
    if not server.voice_client:
        await ctx.send("Where to play?")
        return
    voice_channel = server.voice_client
    async with ctx.typing():
        # start radio and get first track
        filename = radio.start_radio(_station_id, _station_from)
        filename.download("boba.mp3", codec="mp3", bitrate_in_kbps=320)
        voice_channel.play(discord.FFmpegPCMAudio(source="boba.mp3"))
        voice_channel
    await ctx.send('**Now playing:** {}'.format(filename["title"]))


bot.run(config['token'])