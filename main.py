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

class AgeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="18+", value="18+"),
            discord.SelectOption(label="18-", value="18-")
        ]
        super().__init__(
            placeholder="Select your age group",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id] = {"age": self.values[0]}
        await interaction.response.send_message(
            view=GenderView(),
            ephemeral=True
        )


class AgeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(AgeSelect())


class GenderSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Male", value="Male"),
            discord.SelectOption(label="Female", value="Female")
        ]
        super().__init__(
            placeholder="Select your gender",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["gender"] = self.values[0]
        await interaction.response.send_message(
            view=GamesView(),
            ephemeral=True
        )


class GenderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(GenderSelect())
class GamesSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Free Fire", value="Free Fire"),
            discord.SelectOption(label="BGMI", value="BGMI"),
            discord.SelectOption(label="GTA V", value="GTA V"),
            discord.SelectOption(label="Roblox", value="Roblox")
        ]

        super().__init__(
            placeholder="Select the games you play",
            min_values=1,
            max_values=4,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["games"] = self.values

        member = interaction.guild.get_member(interaction.user.id)

        roles_to_add = []

        roles_to_add.append(
            interaction.guild.get_role(VERIFIED_ROLE)
        )

        age = user_data[interaction.user.id]["age"]

        if age == "18+":
            roles_to_add.append(
                interaction.guild.get_role(AGE18PLUS_ROLE)
            )
        else:
            roles_to_add.append(
                interaction.guild.get_role(AGE18MINUS_ROLE)
            )

        gender = user_data[interaction.user.id]["gender"]

        if gender == "Male":
            roles_to_add.append(
                interaction.guild.get_role(MALE_ROLE)
            )
        else:
            roles_to_add.append(
                interaction.guild.get_role(FEMALE_ROLE)
            )

        games = user_data[interaction.user.id]["games"]

        if "Free Fire" in games:
            roles_to_add.append(
                interaction.guild.get_role(FREE_FIRE_ROLE)
            )

        if "BGMI" in games:
            roles_to_add.append(
                interaction.guild.get_role(BGMI_ROLE)
            )

        if "GTA V" in games:
            roles_to_add.append(
                interaction.guild.get_role(GTAV_ROLE)
            )

        if "Roblox" in games:
            roles_to_add.append(
                interaction.guild.get_role(ROBLOX_ROLE)
            )

        roles_to_add = [r for r in roles_to_add if r is not None]

        await member.add_roles(*roles_to_add)

        await interaction.response.send_message(
            "✅ Verification completed! Roles assigned successfully.",
            ephemeral=True
        )


class GamesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(GamesSelect())


class VerifyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="🔐 Verify",
            style=discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Select your age:",
            view=AgeView(),
            ephemeral=True
        )


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(VerifyButton())


@bot.tree.command(
    name="setupverify",
    description="Create verification panel"
)
async def setupverify(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🔐 Server Verification",
        description=(
            "Welcome to Mentalism!\n\n"
            "Click the Verify button below.\n"
            "You will be asked:\n"
            "• Age\n"
            "• Gender\n"
            "• Games you play\n\n"
            "Roles will be assigned automatically."
        ),
        color=discord.Color.green()
    )

    await interaction.channel.send(
        embed=embed,
        view=VerifyView()
    )

    await interaction.response.send_message(
        "✅ Verification panel created.",
        ephemeral=True
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    bot.add_view(VerifyView())

    guild = discord.Object(id=GUILD_ID)

    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


bot.run(TOKEN)
