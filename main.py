import asyncio
import csv
import io
import random
from random import randint
import sys
import discord
import time
import json
from gtts import gTTS

from discord import Client
from discord.ext import commands

import Tokenizer

main_channel_name="arai"
joke_channel_name="jokes"

client = commands.Bot(command_prefix = '.')

#calls help() on this module and stores output into help_text for HELP calls
def store_help_text():
    print("Building API")
    # Temporarily redirect stdout to a StringIO.
    stdout = sys.stdout
    s = io.StringIO()
    sys.stdout = s
    current_module = sys.modules[__name__]
    help(current_module)
    # Don't forget to reset stdout!
    sys.stdout = stdout
    # Read the StringIO for the help message.
    s.seek(0)
    help_string = s.read()
    global help_text
    help_text=help_string

#read dadjokes.txt and store them
def read_jokes():
    with open("dadjokes.txt", 'r', encoding='utf-8') as infile:
        global jokes
        jokes = infile.readlines()
        print("Humor module loaded - \"Feeling funny...\"")

async def play_audio(voice_channel,file):
    ch = client.get_all_channels()
    for i in ch:
        if str(i.type) == "voice" and i.name == voice_channel:
            vc = await i.connect()
            vc.play(discord.FFmpegPCMAudio(file), after=lambda e: print('Finished playing ', file))
            while vc.is_playing() == True:
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

def generate_morning_quote():
    with open('inspiration_quotes.csv') as f:
        reader = csv.reader(f)
        chosen_row = random.choice(list(reader))
        tts = gTTS("Good Morning ARAI ,"+chosen_row[1])
        tts.save('audio/good_morning.mp3')

@client.event
async def on_ready():
    print("Queueing entry music... - I awake")
    generate_morning_quote()
    await play_audio(joke_channel_name, "audio/awaken.mp3")
    await play_audio(joke_channel_name, "audio/good_morning.mp3")
    store_help_text()
    read_jokes()
    print('Existential Module Booted - I am AWARE')

#use a sentence with 'suggestion' to suggest new features for me
#your suggestion will be stored permanently and contemplated upon by my techpriest
async def ARAI_CMD_SUGGESTION(message):
    f = open("suggestions.txt", "a")
    txt = str(message.author) + message.content + "\n"
    f.writelines(txt)
    await message.channel.send(f"Thank you for the suggestion {message.author}. I'll be sure to pass it on to my Techpriest.")

#use a sentence with 'help' to make me explain to you for the umpteenth time what I can do for you, you puny pile of flesh
async def ARAI_CMD_HELP(message):
    print("HELP_txt:",help_text)
    await message.channel.send(help_text)

#use a sentence with 'joke' to make me light up your miserable organic life
async def ARAI_CMD_JOKE(message):
    jokenr = randint(0, len(jokes))
    joke_Q_A=jokes[jokenr].split(sep='?')
    #check if the structure of the joke is a Question followed by an answer
    if len(joke_Q_A)==2:
        await message.channel.send(joke_Q_A[0])
        tts = gTTS(joke_Q_A[0])
        tts.save('audio/joke_q.mp3')
        await play_audio(joke_channel_name, 'audio/joke_q.mp3')
        await asyncio.sleep(3)
        tts = gTTS(joke_Q_A[1])
        tts.save('audio/joke_a.mp3')
        await message.channel.send(joke_Q_A[1])
        await play_audio(joke_channel_name, 'audio/joke_a.mp3')
    else:
        await message.channel.send(joke_Q_A[0])
        tts = gTTS(joke_Q_A[0])
        tts.save('audio/joke_q.mp3')
        await play_audio(joke_channel_name, 'audio/joke_q.mp3')

@client.event
async def on_message(message):
    if message.author!=client.user:
        msg_content = message.content
        for i in message.mentions:
            print("User mentioned :", i)
        if client.user in message.mentions:
            if "joke" in msg_content.lower():
                await ARAI_CMD_JOKE(message)
            elif "help" in msg_content.lower():
                await ARAI_CMD_HELP(message)
            elif "suggestion" in msg_content.lower():
                await ARAI_CMD_SUGGESTION(message)

client.run(Tokenizer.discordToken)