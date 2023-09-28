# TODO: ERROR CHECKING AND HANDLING!!!!

import configutil
import utils

import sys
import os
from os.path import exists
import logging

import discord
from discord.ext import commands

DISCORD_TOKEN = ''
CONFIG_FILENAME = "config.ini"

# Checks whether the config exists and creates an empty one if it doesn't.
conf_exists = configutil.check_existance(config_filename)
if not conf_exists:
    create_default_config(filename=config_filename)
    logging.info("Default config file created. Make sure to fill it in.\nExiting.")
    sys.exit()

config = configutil.read_config(CONFIG_FILENAME)

logging.info(f"Using {config['OPTIONS']['WhisperMode']} transcription mode.")

# Make sure the temp dir exists and create it if it doesn't'
if not exists("./temp"):
    logging.error("No temp folder, creating!")
    os.makedirs("./temp")
    logging.info("Temp folder created.")

# Clear temp files
utils.clear_temp()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

DISCORD_TOKEN = config['SECRETS']['DiscordToken']


@client.event
async def setup_hook():
    await client.load_extension("commands")


@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.attachments:  # if message has an attachment(s)
        attachment = message.attachments[0]
        if attachment.is_voice_message():

            filepath = await utils.save_audio(attachment)

            transcription = utils.transcribe(filepath=filepath) #config=config # Pass the config file TODO: rework thisssss

            embed = utils.make_embed(transcript=transcription, author=message.author)
            await message.reply(embed=embed)

    await client.process_commands(message)

client.run(DISCORD_TOKEN)

