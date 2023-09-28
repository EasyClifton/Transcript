"""A cog that handles commands."""

import utils

import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def transcribe(self, ctx, message: discord.Message=None):
        """
        Find and transcribe a referenced message.

        If the message issuing the command is a reply to a voice message, the voice message will be transcribed.
        If a message ID is provided as a command argument, the message will be looked up (in the current channel) and transcribed
        :message: Message link or ID to be transcribed.
        """
        replied_to = True if ctx.message.reference is not None else False
        if replied_to:
            message_reference = ctx.message.reference.resolved
            #await ctx.send(message_reference.content)
            print(message_reference)


            if message_reference.attachments:  # if message has an attachment(s)
                attachment = message_reference.attachments[0]
                if attachment.is_voice_message():

                    filepath = await utils.save_audio(attachment)

                    transcription = utils.transcribe(filepath=filepath)

                    embed = utils.make_embed(transcript=transcription, author=message_reference.author, jump_url=message_reference.jump_url)
                    #await message_reference.reply(embed=embed)
                    await ctx.reply(embed=embed)

                else:
                    await ctx.reply("No audio >:(")
                    #original_msg_content = message_reference.content
        else:
            await ctx.reply("No message to transcribe! Please reply to one or provide it as an argument!")


async def setup(bot):
    await bot.add_cog(Commands(bot))
