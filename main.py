import datetime
import logging
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from pokedex import KoreanPokedex, UnknownKoreanPokemonNameException

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.tree.command(name="포켓몬", description="포켓몬 정보")
@app_commands.describe(이름="포켓몬 이름")
async def pokedex(interaction: discord.Interaction, 이름: str) -> None:
    try:
        pokemon = KoreanPokedex().get_pokemon_info(이름)
        embed = discord.Embed(
            title=이름,
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        embed.add_field(name="속성", value=", ".join(pokemon['types']))
        embed.add_field(name="특성", value=", ".join(pokemon['abilities']))
        embed.add_field(name="개체값",
                        value="HP: {}, 공격: {}, 방어: {}, 특수공격: {}, 특수방어: {}, 스피드: {}"
                        .format(pokemon['stats']['hp'],
                                pokemon['stats']['atk'],
                                pokemon['stats']['def'],
                                pokemon['stats']['spa'],
                                pokemon['stats']['spd'],
                                pokemon['stats']['spe']),
                        inline=False)
        embed.add_field(name="알그룹", value=", ".join(pokemon['egg_groups']), inline=False)
        await interaction.response.send_message(embed=embed)

    except UnknownKoreanPokemonNameException:
        pass

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')


if __name__ == '__main__':
    bot.run(os.getenv("TOKEN"))
