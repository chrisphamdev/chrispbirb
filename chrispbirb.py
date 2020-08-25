from env_loader import load_env
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from discord import client

env = load_env("/")
token = env.get("TOKEN")
client = commands.Bot(command_prefix='>')


# keep track of the custom voice sessions
custom_voice_channels = {}


# Custom help message - to be done
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("`Hop in the \"Create New Session\" voice channel to generate a voice chat for your use`")


@client.event
async def on_ready():
    print('Chrispbirb has been deployed.')


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

            # Add the voice channel instance to the tracker
            custom_voice_channels[new_session.name] = -1 # -1 as the user join counts twice first time
            await member.move_to(new_session)
    
    
    #update the counter everytime someone enters a custom session
    if after.channel is not None:
        if after.channel.name in custom_voice_channels:
            custom_voice_channels[after.channel.name] += 1


    # Remove the session as the all user exit - TO FIX THE COUNTER DOESN'T UPDATE THE FIRST TIME AN USER EXITS (doesn't affect functionality)
    if before.channel is not None:
        if before.channel.name in custom_voice_channels:
            user_count = custom_voice_channels[before.channel.name]
            if before.channel.name in custom_voice_channels and user_count > 0:
                custom_voice_channels[before.channel.name] -= 1
            if before.channel.name in custom_voice_channels and user_count == 1:
                time.sleep(1)
                await before.channel.delete()


@client.command()
async def hello(ctx):
    await ctx.send('Greetings {0.mention}'.format(ctx.author))


client.run(token)
