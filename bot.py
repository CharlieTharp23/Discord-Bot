from discord.ext import commands
import discord
import numpy as np
import Bot_info
import json
from datetime import datetime, timedelta

number_of_user = {}
temp_dict_of_data = {}


## [username, [day, hour, second], [day, hour, second]]

with open("data.json", "r") as file: 
    number_of_user = json.load(file)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is now Online")
    
    
@bot.event
async def on_voice_state_update(member, before, after):
    if f"{member}" not in number_of_user:
        number_of_user[f"{member}"] = 0

    if f"{member}" not in temp_dict_of_data:
        temp_dict_of_data[f"{member}"] = [[], []]


    Message_channel = bot.get_channel(Bot_info.CHANNEL_ID)
    try:
        await Message_channel.send(f"{member} has joined the channel: {member.voice.channel}")
        ## join VC information
        temp_dict_of_data[f"{member}"][0].append(datetime.now().day)
        temp_dict_of_data[f"{member}"][0].append(datetime.now().hour)
        temp_dict_of_data[f"{member}"][0].append(datetime.now().minute)
        temp_dict_of_data[f"{member}"][0].append(datetime.now().second)
    except: 
        await Message_channel.send(f"{member} is no longer in a voice channel!")
        ## Leave VC information
        temp_dict_of_data[f"{member}"][1].append(datetime.now().day)
        temp_dict_of_data[f"{member}"][1].append(datetime.now().hour)
        temp_dict_of_data[f"{member}"][1].append(datetime.now().minute)
        temp_dict_of_data[f"{member}"][1].append(datetime.now().second)
        await update_time(f"{member}")


async def update_time(member):
    numerical_data = []
    for i in range(0,4):
        start = temp_dict_of_data[member][0][i]
        end = temp_dict_of_data[member][1][i]
        numerical_data.append(end - start)
    convert_to_seconds(member, numerical_data)

def convert_to_seconds(member, numerical_data): 
    seconds = 0

    ## edge case if someone is on a call through midnight, but was not on for more than 24 hours 
    if temp_dict_of_data[member][0][0] > temp_dict_of_data[member][1][0] and numerical_data[0] < 1 :
        ## sets days to zero
        numerical_data[0] = 0
        ## finds the total from midnight and adds it to the rest of the hours 
        numerical_data[1] += (23 - temp_dict_of_data[member][0][0])

    seconds += (numerical_data[0] * 86400) ## # of seconds in a day
    seconds += (numerical_data[1] * 3600)
    seconds += (numerical_data[2] * 60)
    seconds += (numerical_data[3])

    print(f"{member} was in a call for: " + str(seconds))
    number_of_user[member] += seconds



bot.run(Bot_info.BOT_TOKEN)

## write to txt file
with open("data.json", "w") as file: 
    json.dump(number_of_user, file)
