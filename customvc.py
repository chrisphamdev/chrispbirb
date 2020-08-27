import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from discord import client


class allVoiceChannel:
    #keeps track of all CustomVoiceChannel instances
    def __init__(self):
        self.all_voice_channels = []


    #add CustomVoiceChannel instance to the list
    def sessionCreated(self, newVC):
        self.all_voice_channels += [newVC]


    #delete a custom voice channel from the list
    def session_delete(self, vc_to_be_deleted):
        for i in range(len(self.all_voice_channels)):
            if self.all_voice_channels[i] == vc_to_be_deleted:
                self.all_voice_channels.pop(i)
                break


    #check if voice chat exists
    def exist(self, discord_voice_channel):
        for vc in self.all_voice_channels:
            if discord_voice_channel.id == vc.get_id():
                return True

    
    #return equivalent CustomVoiceChannel object
    def get_vc(self, discord_voice_channel):
        for vc in self.all_voice_channels:
            if discord_voice_channel.id == vc.get_id():
                return vc


class CustomVoiceChannel:
    def __init__(self, session, ownerID):
        self.__session = session
        self.__owner = ownerID
        self.__userCount = -1
    
    def user_join(self):
        self.__userCount += 1
    
    def user_left(self):
        self.__userCount -= 1
    
    def is_empty(self):
        return self.__userCount <= 0

    def get_name(self):
        return self.__session.name

    def get_id(self):
        return self.__session.id

    def get_session(self):
        return self.__session

    def is_owner(self, discord_user):
        return discord_user.id == self.__owner