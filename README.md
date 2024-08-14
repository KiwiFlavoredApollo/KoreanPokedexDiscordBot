# README

- python 3.12

Korean Pokedex Discrod Bot utilizing PokeAPI database

PokeAPI 데이터베이스를 활용한 한국어 포켓몬 도감 디스코드 봇

## Installation


### 1. Clone repository

```commandline
git clone https://github.com/KiwiFlavoredApollo/KoreanPokedexDiscordBot.git
cd KoreanPokedexDiscordBot
```

### 2. Edit environment variable

```yaml
services:
  discord-bot:
    build: .
    container_name: korean-pokedex
    restart: unless-stopped
    environment:
      DISCORD_BOT_TOKEN: $DISCORD_BOT_TOKEN
```

Replace `$DISCORD_BOT_TOKEN` with your token

### 3. Build docker container

```commandline
docker-compose up --build -d
```

## Pokemon Database

- [PokeAPI - Github](https://github.com/PokeAPI/pokeapi/tree/master/data/v2/csv)

## Gallery

![KoreanPokedexDiscordBot](https://i.imgur.com/022qC2N.png)

## Reference

- [Discord.py Masterclass](https://fallendeity.github.io/discord.py-masterclass/)