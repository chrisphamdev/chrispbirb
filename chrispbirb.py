''' This bot was developed by Chris Pham, along with the UoA Esports staff team
'''
from env_loader import load_env
import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import customvc
from customvc import CustomVoiceChannel
from customvc import allVoiceChannel
import logging
import random
from discord.utils import get


#handles the logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


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


#@cooldown(rate=2, per=600.0,  type=BucketType.user)
@client.command()
async def session(ctx, *, custom_name):
    if custom_name == "Create New Session":
        await ctx.send("Invalid name.")
        return
    new_vc_name = custom_name

    # check if the user is in a voice channel
    if ctx.author.voice == None:
        await ctx.send("You have to be in a channel!")
        return

    # check if the user is the owner of the channel    
    current_vc = ctx.author.voice.channel
    if all_custom_vc.exist(current_vc):
        vc_object = all_custom_vc.get_vc(current_vc)
        if not vc_object.is_owner(ctx.author):
            await ctx.send("You're not the owner of this voice session.")
        else:
            await current_vc.edit(name=new_vc_name)

    
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! This message took {round(client.latency * 1000)}ms to respond.')

@client.command()
async def flip(ctx):
    coin = random.randrange(1,3)
    if coin == 1:
        await ctx.send('Heads!')
    if coin == 2:
        await ctx.send('Tails!')


@client.command()
async def mottronghai(ctx, option1, option2):
    option = random.randrange(1,3)
    if option == 1:
        await ctx.send(option1)
    if option == 2:
        await ctx.send(option2)

@client.command()
async def amonguslfg_setup(ctx):
    text = '\nReact to the emojis under this message to get the Among Us LFG role. \n \n The [1] and [2] emojis give you the role for 1 and 2 hour(s) respectively, while the \'AmongUs\' emoji gives you the role permanently. Simply remove your reaction to this emoji and the role will be removed just like in the #get-roles channel. \n \nBe mindful that this role can be pinged by anyone!'
    embedVar=discord.Embed(title="Among Us LFG Role", description=text, color=0x14cad7)
    embedVar.set_image(url='https://images.dexerto.com/uploads/2020/08/25181313/among-us-taking-over-twitch-final.jpg')
    msg = await ctx.send(embed=embedVar)

    for emoji in ctx.author.guild.emojis:
        if emoji.name == 'AmongUs' or emoji.name == 'amongus':
            amongus_emoji = emoji
            break
    
    await msg.add_reaction('1\N{variation selector-16}\N{combining enclosing keycap}')
    await msg.add_reaction('2\N{variation selector-16}\N{combining enclosing keycap}')
    await msg.add_reaction(amongus_emoji)

@client.event
async def on_raw_reaction_add(data):
    #replace message id with id of get role message
    if data.message_id == 760760458360651836:
        for elm in data.member.guild.channels:
            if elm.name == 'among-us' or elm.name == 'nerd-chat':
                host_channel = elm
                break
        msg = await host_channel.fetch_message(data.message_id)

        #replace this with id of 'Among Us LFG' role
        role_id = 760392204710969354
        if data.emoji.name == '1️⃣':
            role = get(data.member.guild.roles, id=role_id)
            await data.member.add_roles(role)
            await msg.remove_reaction(emoji=data.emoji, member=data.member)
            await asyncio.sleep(3600)
            await data.member.remove_roles(role)
        if data.emoji.name == '2️⃣':
            role = get(data.member.guild.roles, id=role_id)
            await data.member.add_roles(role)
            await msg.remove_reaction(emoji=data.emoji, member=data.member)
            await asyncio.sleep(7200)
            await data.member.remove_roles(role)
        if data.emoji.name == 'amongus' or data.emoji.name == 'AmongUs':
            role = get(data.member.guild.roles, id=role_id)
            await data.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(data):
    #replace message id with id of get role message
    if data.message_id == 760760458360651836:
        #replace this with the id of 'Among Us LFG' role
        role_id = 760392204710969354
        #obtain the member object of the reacted member
        member = client.get_user(data.user_id)
        server = client.get_guild(data.guild_id)
        for mem in server.members:
            if mem.id == member.id:
                reacted_member = mem
                break
        
        if data.emoji.name == 'amongus' or data.emoji.name == 'AmongUs':
            role = get(reacted_member.guild.roles, id=role_id)
            await reacted_member.remove_roles(role)
    
client.run(token)