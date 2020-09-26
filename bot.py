#!/usr/bin/python3
import os

import discord
import asyncio
import subprocess
import re
import random
from discord.ext import tasks, commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
bot = commands.Bot(command_prefix='?', description="None")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print (guild.name)

async def perforce_check():
    await bot.wait_until_ready()
    channel = bot.get_channel(759276587065147433)
    latest_change = ''
    while not bot.is_closed():
        p4_changes = subprocess.Popen('p4 changes -t -m 1 -l', stdout=subprocess.PIPE, shell=True)
        p4_changes = p4_changes.stdout.read().decode('ISO-8859-1')
        if latest_change != p4_changes:
            latest_change = p4_changes
            if '*pending*' in p4_changes:
                p4_changes=''
        else:
            p4_changes=''
        if p4_changes != '':
            change_body = p4_changes.split("\n", 2)[2]
            change_body = change_body.strip()
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

                name = p4_changes.split("\n", 1)[0]
                name = name.split(" by ", 1)[1]

                body = change_body.split(":", 1)[1]
                body = body.strip()
                await channel.send(content=f"A {random.choice(cool_words)} new **{clType}** was just submitted for **{category}** by {name}!\n>>> {body}")
                
            else:
                await channel.send(content=f"{p4_changes}")
        await asyncio.sleep(30)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == '!stat' or message.content == '!stats':
        depot_size = subprocess.run(['du', '-sh', '/perforce_depot/'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        depot_size = depot_size.split(' ', 1)[0]
        drive_size = subprocess.run(['df', '-h', '/'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        perforce_stats = subprocess.run(['p4', 'info', '-s'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        #response = f"Server stats:\nPerforce Depot Size:\n{depot_size}\nDrive Size:\n{drive_size}"
        
        #await message.channel.send(response)
        embed=discord.Embed(title="Server Stats", color=0xf50000)
        embed.add_field(name="Perforce depot size:", value=depot_size, inline=False)
        embed.add_field(name="Drive Size", value=f"```\n{drive_size}\n```", inline=False)
        embed.add_field(name="Perforce Stats", value=f"{perforce_stats}", inline=False)
        await message.channel.send(embed=embed)

#bot.add_cog(MyCog(bot))
bot.loop.create_task(perforce_check())
bot.run(TOKEN)
#client.run(TOKEN)
