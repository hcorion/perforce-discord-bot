#!/usr/bin/python3
import os

import discord
import asyncio
import subprocess
import re
import random
import difflib
from P4 import P4
from discord.ext import tasks, commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?', description="None")

p4 = P4()
p4.user = os.getenv('P4USER')
p4.password = os.getenv('P4PASSWD')
p4.connect()
p4.run_login()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print (guild.name)

async def perforce_check():
    await bot.wait_until_ready()
    debugchannel = bot.get_channel(759276587065147433)
    channel = bot.get_channel(759509287596458034)
    #channel = debugchannel


    with open('last_change_file.txt', 'r+') as file:
        latest_change = file.read()

    while not bot.is_closed():
        
        p4_changes_arr = p4.run_changes("-t", "-m 1", "-l")
        p4_changes = p4_changes_arr[0]
        change = p4_changes["change"]
        time = p4_changes["time"]
        user = p4_changes["user"]
        client = p4_changes["client"]
        desc = p4_changes["desc"]

        output = "Change " + change + " on " + time + " by " + user + "@" + client + "\n\n" + desc
        output = output.strip()

        if latest_change != output:
            latest_change = output
            if '*pending*' in output:
                p4_changes=''
        else:
            p4_changes=''
        if p4_changes != '':
            with open('last_change_file.txt', 'w+') as file:
                file.write(output)

            change_body = desc
            cool_words = ["dope", "super cool", "sweet", "awesome", "amazing", "outstanding", "fantastic", "beautiful", "radical", "bangin'", "breathtaking", "wonderful", "magnificent", "terrific", 
                    "extraordinary", "splendid", "grand", "stupendous", "superb", "marvellous", "tremendous", "spectacular", "sensational", "glorious"]
            #This website is amazing https://regexr.com/
            featurePattern = re.compile("^(feat|feature) *\( *.* *\) *:")
            bugPattern = re.compile("^(bug|fix|bugfix) *\( *.* *\) *:")
            maintenancePattern = re.compile("^(maint|maintenance) *\( *.* *\) *:")
            if featurePattern.match(change_body) or bugPattern.match(change_body) or maintenancePattern.match(change_body):
                clType = "Feature"
                if bugPattern.match(change_body):
                    clType = "Bugfix"
                elif maintenancePattern.match(change_body):
                    clType = "Maintenance fix"
                category = change_body.split("(", 1)[1]
                category = category.split(")", 1)[0]

                body = change_body.split(":", 1)[1]
                body = body.strip()
                await channel.send(content=f"A {random.choice(cool_words)} new **{clType}** was just submitted for **{category}** by {user}!\n>>> {body}")
                
            else:
                await channel.send(content=f"{p4_changes}")
        await asyncio.sleep(30)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "!sit":
        sitting_options = ["Initiating sit protocols, please stand by.", "I'm afraid I can't do that {}",
                "Unable to find command \"sit\". Instead initiating \"Revenge of the Sith\" command.\n please wait."
                ]
        await message.channel.send(random.choice(sitting_options).format(message.author.mention))
    if re.search('ebi', message.content, re.IGNORECASE):
        await(message.add_reaction('\N{HEAVY BLACK HEART}'))
    if message.content == '!stat' or message.content == '!stats':
        depot_size = subprocess.run(['du', '-sh', '/perforce_depot/'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        depot_size = depot_size.split(' ', 1)[0]
        drive_size = subprocess.run(['df', '-h', '/'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        perforce_stats = subprocess.run(['p4', 'info', '-s'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        embed.add_field(name="Perforce depot size:", value=depot_size, inline=False)
        embed.add_field(name="Drive Size", value=f"```\n{drive_size}\n```", inline=False)
        embed.add_field(name="Perforce Stats", value=f"{perforce_stats}", inline=False)
        await message.channel.send(embed=embed)

#bot.add_cog(MyCog(bot))
bot.loop.create_task(perforce_check())
bot.run(TOKEN)
#client.run(TOKEN)
