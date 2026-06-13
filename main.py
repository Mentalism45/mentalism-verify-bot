import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

VERIFIED_ROLE = 1515064961536360654

FREE_FIRE_ROLE = 1458482373602578514
BGMI_ROLE = 1515064606949900348
GTAV_ROLE = 1515064885573324850
ROBLOX_ROLE = 1515065097603776734

MALE_ROLE = 1515268315646263296
FEMALE_ROLE = 1515268390409732096

AGE18PLUS_ROLE = 1458481456828514455
AGE18MINUS_ROLE = 1458481619425034293

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_data = {}
