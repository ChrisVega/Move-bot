import asyncio

import discord
from discord import User
from discord.ext import commands
import logging
from threading import Timer

import Config

logging.basicConfig(level=logging.INFO)

description = '''A bot that allows users to temporarilly be alowed to move other users'''

bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    # just prints message on login
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping():
    """replies "pong", to check if bot is working or not"""
    await bot.say('pong')


@bot.command()
async def about():
    """A nice message from the bot"""
    await bot.say('Hi, Im Friendbesto! I am here to help users and make new friends! \n'
                  'There is nothing "strange" or "threatening" about me in any way, Im just here for good times with '
                  'good friends.\nAnd I do hope we can become good friends, the best friends there ever were.')


@bot.command(pass_context=True)
async def move(ctx):
    """allows the user to move other users for a minute"""

    member = ctx.message.author
    server = ctx.message.server
    channel = discord.utils.find(lambda m: m.name == 'move_logs', server.channels)
    roles = server.roles
    mov_role = None
    move_trigger = True

    @bot.event
    async def on_voice_state_update(before, after):
        if move_trigger and channel.name == "move_logs":
            # posts in a text chat if a uses was moved when this command is used
            await bot.send_message(channel, '{} moved'.format(member))
            bot.process_commands(after)

    for x in range(0, len(roles)):
        if roles[x].name == "mov_role":  # finds the role names mov_role
            mov_role = roles[x]
            break
    await bot.add_roles(member, mov_role)
    if channel.name == "move_logs":
      await bot.send_message(channel,'{} can now move other users'.format(member))
    print('User {} was given role {}'.format(member, mov_role))
    await asyncio.sleep(60)
    await bot.remove_roles(member, mov_role)
    print('User {} had role {} removed'.format(member, mov_role))
    move_trigger = False


bot.run(Config.get_token(), reconnect=True)
