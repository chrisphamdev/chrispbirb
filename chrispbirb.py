import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from discord import client

token = 'NzQ3NjUxNzkxNTkxNTcxNDg3.X0R-_Q.V98Qk9lisHYSD3pB1tQxIkbIffU'
client = commands.Bot(command_prefix='>')


# Custom help message - to be done
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("```This is the help message\n ```")


@client.event
async def on_ready():
    print('Chrispbirb is now deployed.')


@client.event
async def on_voice_state_update(member, before, after):
    # Creating a new session when member joins
    if after.channel is not None:
        if after.channel.name == "Create New Session":
            channel_name = member.name + "'s session"

            # Get index of voice channels category
            category_index = -1
            for i in range(len(member.guild.categories)):
                if after.channel.category_id == member.guild.categories[i].id:
                    category_index = i

            # Create the new session on the same category as the initialize voice channel
            new_session = await member.guild.categories[category_index].create_voice_channel(channel_name)
            await member.move_to(new_session)

    # Remove the session as the user exit
    if before.channel is not None:
        if before.channel.name[-10:] == "'s session":
            await before.channel.delete()


@client.command()
async def hello(ctx):
    await ctx.send('Greetings {0.mention}'.format(ctx.author))


client.run(token)
