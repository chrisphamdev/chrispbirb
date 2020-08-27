''' This bot was developed by Chris Pham, along with the UoA Esports staff team
'''
from env_loader import load_env
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from discord import client
import customvc
from customvc import CustomVoiceChannel
from customvc import allVoiceChannel

env = load_env("/")
token = env.get("TOKEN")
client = commands.Bot(command_prefix='>')


# keep track of the custom voice sessions
all_custom_vc = allVoiceChannel()


# Custom help message - to be done
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("`Hop in the \"Create New Session\" voice channel to generate a voice chat for your use, and use the command '>session name' to modify your session name if you wish to`")


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

            """# Make sure that the channel is above the bottom channel (persumably the AFK channel)
            if (member.guild.id == 154456736319668224):
                for i in range(len(member.guild.categories[category_index].voice_channels)):
                    if member.guild.categories[category_index].voice_channels[i].id == 154457743439167488: # ID of AFK channel
                        afk_channel_index = i
                        break
                await member.guild.categories[category_index].voice_channels[afk_channel_index].edit(position=afk_channel_index+1)
                await new_session(position=afk_channel_index-1)
                print(member.guild.categories[category_index].voice_channels)"""

            # Add the voice channel id to the tracker
            new_room = CustomVoiceChannel(new_session, member.id)
            all_custom_vc.sessionCreated(new_room)
            await member.move_to(new_session)

    
    
    #update the counter everytime someone enters a custom session
    if after.channel is not None:
        if all_custom_vc.exist(after.channel):
            vc = all_custom_vc.get_vc(after.channel)
            vc.user_join()


    # Remove the session as the all user exit - TO FIX THE COUNTER DOESN'T UPDATE THE FIRST TIME AN USER EXITS (doesn't affect functionality)
    if before.channel is not None:
        if all_custom_vc.exist(before.channel):
            vc = all_custom_vc.get_vc(before.channel)
            vc.user_left()
            if vc.is_empty():
                await before.channel.delete()
                all_custom_vc.session_delete(vc)


@client.command()
async def hello(ctx):
    await ctx.send('Greetings {0.mention}'.format(ctx.author))


@client.command()
async def info(ctx):
    await ctx.send('`This bot was developed by the UoA staff team for the UoA Esports server.\nAny feedback will be kindly appreciated to Chris P Bacon#0047.`')


@client.command()
async def beg(ctx):
    await ctx.send('Any donation would be kindly appreciated in League\'s RP to the account Chris P Bacon#OCE :   ^)')


# can only change name twice for some reason
@client.command()
async def session(ctx, *, name):
    new_vc_name = name

    #check if the user is in a voice channel
    if ctx.author.voice == None:
        await ctx.send("You have to be in a channel!")
        return

    # check if the user is the owner of the channel    
    current_vc = ctx.author.voice.channel
    if all_custom_vc.exist(current_vc):
        vc_object = all_custom_vc.get_vc(current_vc)
    if not vc_object.is_owner(ctx.author):
        await ctx.send("You're not the owner of this voice session.")
        return
    
    await current_vc.edit(name=new_vc_name)

    
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! This message took {round(client.latency * 1000)}ms.')


client.run(token)