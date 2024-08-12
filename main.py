import discord
from discord import app_commands
from discord.ext import commands

from pokedex import KoreanPokedex

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.tree.command(name="도감", description="")
async def echo(interaction: discord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pokedex = KoreanPokedex()
    bot.run("YOUR_BOT_TOKEN")
