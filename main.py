import os
import discord
from discord.ext import commands
from discord.ui import View, Select

TOKEN = os.getenv("DISCORD_TOKEN")

VERIFY_CHANNEL_ID = 1505853378704445552

VERIFIED_ROLE = 1515064961536360654

MALE_ROLE = 1515268315646263296
FEMALE_ROLE = 1515268390409732096

AGE18PLUS_ROLE = 1458481456828514455
AGE18MINUS_ROLE = 1458481619425034293

FREEFIRE_ROLE = 1458482373602578514
BGMI_ROLE = 1515064606949900348
GTAV_ROLE = 1515064885573324850
ROBLOX_ROLE = 1515065097603776734

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class GenderSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Male", emoji="👨"),
            discord.SelectOption(label="Female", emoji="👩")
        ]

        super().__init__(
            placeholder="👤 Select Gender",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        male_role = interaction.guild.get_role(MALE_ROLE)
        female_role = interaction.guild.get_role(FEMALE_ROLE)

        await member.remove_roles(male_role, female_role)

        if self.values[0] == "Male":
            await member.add_roles(male_role)
        else:
            await member.add_roles(female_role)

        await interaction.response.send_message(
            "✅ Gender role updated!",
            ephemeral=True
        )


class AgeSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="18+", emoji="🔞"),
            discord.SelectOption(label="18-", emoji="🧒")
        ]

        super().__init__(
            placeholder="🎂 Select Age",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        plus_role = interaction.guild.get_role(AGE18PLUS_ROLE)
        minus_role = interaction.guild.get_role(AGE18MINUS_ROLE)

        await member.remove_roles(plus_role, minus_role)

        if self.values[0] == "18+":
            await member.add_roles(plus_role)
        else:
            await member.add_roles(minus_role)

        await interaction.response.send_message(
            "✅ Age role updated!",
            ephemeral=True
        )


class GamesSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Free Fire", emoji="🔥"),
            discord.SelectOption(label="BGMI", emoji="🏆"),
            discord.SelectOption(label="GTA V", emoji="🚗"),
            discord.SelectOption(label="Roblox", emoji="🎮")
        ]

        super().__init__(
            placeholder="🎮 Select Games",
            min_values=1,
            max_values=4,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user

        verified_role = interaction.guild.get_role(VERIFIED_ROLE)

        game_roles = [
            interaction.guild.get_role(FREEFIRE_ROLE),
            interaction.guild.get_role(BGMI_ROLE),
            interaction.guild.get_role(GTAV_ROLE),
            interaction.guild.get_role(ROBLOX_ROLE)
        ]

        await member.add_roles(verified_role)

        for role in game_roles:
            await member.remove_roles(role)

        role_map = {
            "Free Fire": FREEFIRE_ROLE,
            "BGMI": BGMI_ROLE,
            "GTA V": GTAV_ROLE,
            "Roblox": ROBLOX_ROLE
        }

        for game in self.values:
            role = interaction.guild.get_role(role_map[game])
            await member.add_roles(role)

        await interaction.response.send_message(
            "🎉 Verification completed successfully!",
            ephemeral=True
        )


class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(GenderSelect())
        self.add_item(AgeSelect())
        self.add_item(GamesSelect())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    channel = bot.get_channel(VERIFY_CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="✨ MENTALISM VERIFICATION ✨",
            description=(
                "━━━━━━━━━━━━━━━━━━\n\n"
                "🔐 Complete verification to unlock the server.\n\n"
                "👤 **Gender**\n"
                "• Male\n"
                "• Female\n\n"
                "🎂 **Age**\n"
                "• 18+\n"
                "• 18-\n\n"
                "🎮 **Games**\n"
                "• 🔥 Free Fire\n"
                "• 🏆 BGMI\n"
                "• 🚗 GTA V\n"
                "• 🎮 Roblox\n\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "✅ Receive your roles automatically\n"
                "💬 Unlock community channels\n"
                "🎯 Access game-specific chats"
            ),
            color=discord.Color.purple()
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/embed/avatars/0.png"
        )

        embed.set_footer(
            text="Mentalism ✨ • Gaming Community"
        )

        await channel.purge(limit=10)

        await channel.send(
            embed=embed,
            view=VerifyView()
        )

    print("Verification panel sent.")


bot.run(TOKEN)
