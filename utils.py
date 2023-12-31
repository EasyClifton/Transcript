"""Collection of various utils for different things."""


import os
from os.path import exists
import datetime
import random
import logging
import sys

# TODO: Rework and figure out the config system
import configutil

import discord

# Temp solution
config_filename = "config.ini"
config = configutil.read_config(config_filename)


def clear_temp():
    '''Clear the temp file folder.'''
    for filename in os.listdir("./temp"):
        file_path = os.path.join("./temp", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def get_audio_attachments(message):
    pass
    # This is for later


# This async doesn't do anything, does it? -need to learn
async def save_audio(attachment):
    '''
    Accept an attachment object and save the audio.

    :attachment: An attachment object to be saved.
    '''
    msg_hash = hash(attachment)
    filepath = f"./temp/{msg_hash}.ogg"
    if attachment.is_voice_message():
        await attachment.save(filepath)
        return filepath


# make async? -need to learn
def transcribe(filepath):
    """
    Send the text to Whisper for transcription.

    Looks at the 'WhisperMode' setting in the config and uses local or online (via the OpenAI API) Whisper for transcription.
    An OpenAI API key should be present in the config for the online option to work.
    :filepath: The path to the file to be transcribed.
    """
    whispermode = config['OPTIONS']['WhisperMode']
    model = config['OPTIONS']['WhisperModel']

    if whispermode == "local":
        import whisper
        whisper_model = whisper.load_model(model)
        result = whisper_model.transcribe(filepath)
        clear_temp()
        return result["text"]

    elif whispermode == "online":
        import openai
        openai.api_key = config['SECRETS']['OpenAIToken']
        audio_file = open(filepath, "rb")
        result = openai.Audio.transcribe("whisper-1", audio_file)
        clear_temp()
        return result["text"]

    else:
        logging.error(f"Unrecognized WhisperMode in config! Can only be 'online' or 'local', '{whispermode}' found instead!\nExiting.")
        clear_temp()
        sys.exit()


def make_embed(transcript, author, jump_url = None):
    """
    Make an embed with the transcription.

    If the `jump_url` argument is provided, a link will be added to the bottom of the embed to jump to the original voice message.
    :transcript: Raw transcript to be put into the embed.
    :author: Autor object for pretty formatting.
    :jump_url: Optional url to the original message.
    """
    funnies = ["Voice messages: Because reading minds is so 2022.",
           "Listening to voice messages so you don't have to.",
           "Voice messages: Making the introverts cringe since forever.",
           "Transcribing audio chaos into text clarity.",
           "Text > Voice. Always.",
           "Voice messages: Because who has time for efficient communication?",
           "Bringing order to the chaos of voice messages.",
           "Decoding voice messages, one mumble at a time.",]

    # TODO: Deal with this later
    #if message.author.nick is None:
    name = author.display_name
    #else:
    #    name = message.author.nick


    if transcript == "":
        # Add embed colors
        transcript = "*No text was returned by Whisper.*"
    else:
        transcript = f"> {transcript}"

    if jump_url is not None:
        transcript = f"{transcript}\n\n[Jump to message](<{jump_url}>)"

    embed=discord.Embed(description=transcript)
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=name, icon_url=author.avatar.url)
    embed.set_footer(text=f"{random.choice(funnies)}")

    return embed
