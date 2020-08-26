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
            if member.nick is not None: #check if the member has a nickname
                channel_name = member.nick + "'s session"
            else:
                channel_name = member.name + "'s session"

            # Get index of voice channels category
            category_index = -1
            for i in range(len(member.guild.categories)):
                if after.channel.category_id == member.guild.categories[i].id:
                    category_index = i
                    break

            # Create the new session on the same category as the initialize voice channel
            new_session = await member.guild.categories[category_index].create_voice_channel(channel_name)

            # Add the voice channel id to the tracker
            custom_voice_channels[new_session.id] = -1 # -1 as the user join counts twice first time
            await member.move_to(new_session)
    
    
    #update the counter everytime someone enters a custom session
    if after.channel is not None:
        if after.channel.id in custom_voice_channels:
            custom_voice_channels[after.channel.id] += 1


    # Remove the session as the all user exit - TO FIX THE COUNTER DOESN'T UPDATE THE FIRST TIME AN USER EXITS (doesn't affect functionality)
    if before.channel is not None:
        if before.channel.id in custom_voice_channels:
            user_count = custom_voice_channels[before.channel.id]
            if before.channel.id in custom_voice_channels and user_count > 0:
                custom_voice_channels[before.channel.id] -= 1
            if before.channel.id in custom_voice_channels and user_count == 1:
                time.sleep(0.6) # so it lingers a bit before going into the unknown :(
                await before.channel.delete()


@client.command()
async def session(ctx, *, name): #still in development
    channel_name = name
    vc_spawn_index = -1
    if channel_name == "Create New Session":
        # warning message and break out of function if given invalid name
        await ctx.send('`Invalid channel name. Please retry.`')
        return

    # Find the Voice Channels category
    for i in range(len(ctx.guild.categories)):
        for vc in ctx.guild.categories[i].voice_channels:
            if vc.name == 'Create New Session':
                vc_spawn_index = i
                break
    
    new_session = await ctx.guild.categories[vc_spawn_index].create_voice_channel(channel_name)
    # Add the voice channel instance to the tracker
    custom_voice_channels[new_session.id] = -1 # -1 as the user join counts twice first time

    # This fragment of code delete the channel if it is inactive after creation (1 min timeout)
    time.wait(60)
    if custom_voice_channels[new_session.name] <= 0:
        await ctx.send('`Session timeout. The voice channel were inactive for too long.`')
        all_vc = ctx.guild.categories[vc_spawn_index].voice_channels
        for vc in all_vc:
            if vc.name == channel_name:
                to_be_deleted = vc
                break
        await to_be_deleted.delete()


@client.command()
async def hello(ctx):
    await ctx.send('Greetings {0.mention}'.format(ctx.author))


@client.command()
async def info(ctx):
    await ctx.send('`This bot was developed by the UoA staff team for the UoA Esports server.\nAny feedback will be kindly appreciated to Chris P Bacon#0047.`')


@client.command()
async def beg(ctx):
    await ctx.send('Any donation would be kindly appreciated in League\'s RP to the account Chris P Bacon#OCE :   ^)')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! This message took {round(client.latency * 1000)}ms.')




client.run(token)