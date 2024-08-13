import datetime
import logging
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from pokedex import KoreanPokedex, UnknownKoreanPokemonNameException, UnknownKoreanMoveNameException

if os.getenv('PYCHARM_HOSTED') == '1':
    os.chdir('./app')

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.tree.command(name="포켓몬", description="포켓몬 정보")
@app_commands.describe(이름="포켓몬 이름")
async def get_pokemon_info(interaction: discord.Interaction, 이름: str) -> None:
    try:
        pokemon = KoreanPokedex().get_pokemon_info(이름)
        embed = discord.Embed(
            title=이름,
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        embed.set_image(url=pokemon["image"])
        embed.add_field(name="속성", value=", ".join(pokemon['types']))
        embed.add_field(name="특성", value=", ".join(pokemon['abilities']))
        embed.add_field(name="개체값",
                        value="HP: {}, 공격: {}, 방어: {}, 특수공격: {}, 특수방어: {}, 스피드: {}, 총합: {}"
                        .format(pokemon['stats']['hp'],
                                pokemon['stats']['atk'],
                                pokemon['stats']['def'],
                                pokemon['stats']['spa'],
                                pokemon['stats']['spd'],
                                pokemon['stats']['spe'],
                                pokemon['stats']['total']),
                        inline=False)
        embed.add_field(name="알그룹", value=", ".join(pokemon['egg_groups']), inline=False)
        embed.add_field(name="참고문헌",
                        value=" • ".join([
                            "[팬덤 위키]({})".format(pokemon["fandom"]),
                        ]))
        await interaction.response.send_message(embed=embed)

    except UnknownKoreanPokemonNameException:
        pass


@bot.tree.command(name="기술", description="기술 정보")
@app_commands.describe(이름="기술 이름")
async def get_move_info(interaction: discord.Interaction, 이름: str) -> None:
    try:
        move = KoreanPokedex().get_move_info(이름)
        embed = discord.Embed(
            title=이름,
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        embed.add_field(name="속성", value=move["type"])
        embed.add_field(name="분류", value=move["damage_class"])
        embed.add_field(name="위력", value=move["power"])
        embed.add_field(name="명중률", value=move["accuracy"])
        embed.add_field(name="PP", value=move["pp"])
        embed.add_field(name="우선도", value=move["priority"])
        embed.add_field(name="참고문헌",
                        value=" • ".join([
                            "[팬덤 위키]({})".format(move["fandom"]),
                        ]))
        await interaction.response.send_message(embed=embed)

    except UnknownKoreanMoveNameException:
        pass


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')


if __name__ == '__main__':
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
