# https://discord.com/api/oauth2/authorize?client_id=1155250274835910766&permissions=139586829376&scope=bot
# TODO: ERROR CHECKING AND HANDLING!!!!

import configutil
import utils

import sys
import os
from os.path import exists
import logging

import discord
import whisper
import openai

discord_token = ''
config_filename = "config.ini"

# Clear temp files
utils.clear_temp()

# Checks whether the config exists and creates an empty one if it doesn't.

conf_exists = configutil.check_existance(config_filename)
if not conf_exists:
    create_default_config(filename=config_filename)
    logging.info("Default config file created. Make sure to fill it in.\nExiting.")
    sys.exit()

config = configutil.read_config(config_filename)

logging.info(f"Using {config['OPTIONS']['WhisperMode']} transcription mode.")

if not exists("./temp"):
    logging.error("No temp folder, creating!")
    os.makedirs("./temp")
    logging.info("Temp folder created.")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

discord_token = config['SECRETS']['DiscordToken']

@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


    if message.attachments:  # if message has an attachment(s)
        attachment = message.attachments[0]
        if attachment.is_voice_message():

            msg_hash = hash(attachment)

            await attachment.save(f"./temp/{msg_hash}.ogg")

            filepath = f"./temp/{msg_hash}.ogg"

            transcription = utils.transcribe(filepath=filepath, config=config)

            embed = utils.make_embed(transcript=transcription, author=message.author)
            await message.reply(embed=embed)

client.run(discord_token)

