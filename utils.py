 # Embed generator

import os
from os.path import exists
import datetime
import random
import logging
import sys

import discord
import openai

def clear_temp():
    '''
    Clears the temp folder
    '''

    for filename in os.listdir("./temp"):
        file_path = os.path.join("./temp", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def transcribe(filepath, config):

    whispermode = config['OPTIONS']['WhisperMode']
    model = config['OPTIONS']['WhisperModel']

    if whispermode == "local":
        import whisper
        whisper_model = whisper.load_model(model)
        result = whisper_model.transcribe(filepath)
        clear_temp()
        return result["text"]

    elif whispermode == "online":

        openai.api_key = config['SECRETS']['OpenAIToken']
        audio_file = open(filepath, "rb")
        result = openai.Audio.transcribe("whisper-1", audio_file)
        clear_temp()
        return result["text"]

    else:
        logging.error(f"Unrecognized WhisperMode in config! Can only be 'online' or 'local', '{whispermode}' found instead!\nExiting.")
        clear_temp()
        sys.exit()


def make_embed(transcript, author):

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

    embed=discord.Embed(description=f"> {transcript}")
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=name, icon_url=author.avatar.url)
    embed.set_footer(text=f"{random.choice(funnies)}")

    return embed
