import csv
import json
import os

ENGLISH = 9
KOREAN = 3


class UnknownKoreanPokemonNameException(Exception):
    pass


class UnknownKoreanMoveNameException(Exception):
    pass


class UnknownPokemonSpeciesIdException(Exception):
    pass


class UnknownPokemonTypeIdException(Exception):
    pass


class UnknownPokemonAbilityIdException(Exception):
    pass


class UnknownPokemonEggGroupIdException(Exception):
    pass


class UnknownMoveDamageClassIdException(Exception):
    pass


class KoreanPokedex:
    def __init__(self):
        self.pokemon_species_name_db = self._import_csv('database/pokemon_species_names.csv')

        self.pokemon_types_db = self._import_csv('database/pokemon_types.csv')
        self.type_names_db = self._import_csv('database/type_names.csv')

        self.pokemon_abilities_db = self._import_csv('database/pokemon_abilities.csv')
        self.ability_names_db = self._import_csv('database/ability_names.csv')

        self.pokemon_stats_db = self._import_csv('database/pokemon_stats.csv')

        self.pokemon_egg_groups_db = self._import_csv('database/pokemon_egg_groups.csv')
        self.egg_group_names_db = self._import_csv('database/egg_groups.csv')

        self.moves_db = self._import_csv('database/moves.csv')
        self.move_names_db = self._import_csv('database/move_names.csv')
        self.move_damage_classes_db = self._import_csv('database/move_damage_classes.csv')

    def _import_json(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def _import_csv(self, path):
        with open(path, 'r', encoding='utf-8', newline='') as file:
            return list(csv.reader(file))

    def korean_to_english(self, name):
        species_id = self._get_species_id_by_korean_name(name)
        return self._get_pokemon_english_name(species_id)

    def _get_species_id_by_korean_name(self, name):
        _SPECIES_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        korean = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.pokemon_species_name_db)
        result = filter(lambda r: r[_NAME] == name, korean)
        result = list(result)

        if len(result) != 1:
            raise UnknownKoreanPokemonNameException
        return int(result[0][_SPECIES_ID])

    def _get_pokemon_english_name(self, species_id):
        _SPECIES_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        english = filter(lambda r: r[_LANGUAGE] == str(ENGLISH), self.pokemon_species_name_db)
        result = filter(lambda r: r[_SPECIES_ID] == str(species_id), english)
        result = list(result)

        if len(result) != 1:
            raise UnknownPokemonSpeciesIdException
        return str(result[0][_NAME])

    def get_pokemon_info(self, pokemon):
        species_id = self._get_species_id_by_korean_name(pokemon)
        return {
            "image": self._get_pokemon_image(species_id),
            "types": self._get_pokemon_type(species_id),
            "abilities": self._get_pokemon_abilities(species_id),
            "stats": self._get_pokemon_stats(species_id),
            "egg_groups": self._get_pokemon_egg_groups(species_id),
            "fandom": self._get_fandom_wiki_link(pokemon),
        }

    def _get_pokemon_type(self, species_id):
        _SPECIES_ID = 0
        _TYPE_ID = 1

        species_types = filter(lambda r: r[_SPECIES_ID] == str(species_id), self.pokemon_types_db)
        type_ids = map(lambda r: r[_TYPE_ID], species_types)
        type_names = list(map(lambda r: self._type_id_to_name(r), type_ids))
        return type_names

    def _get_pokemon_abilities(self, species_id):
        _SPECIES_ID = 0
        _ABILITY_ID = 1

        species_abilities = filter(lambda r: r[_SPECIES_ID] == str(species_id), self.pokemon_abilities_db)
        ability_ids = map(lambda r: r[_ABILITY_ID], species_abilities)
        ability_names = list(map(lambda r: self._ability_id_to_name(r), ability_ids))
        return ability_names

    def _get_pokemon_stats(self, species_id):
        _SPECIES_ID = 0
        _STAT_ID = 1
        _STAT_VALUE = 2

        species_stats = filter(lambda r: r[_SPECIES_ID] == str(species_id), self.pokemon_stats_db)
        stats = list(map(lambda r: int(r[_STAT_VALUE]), species_stats))
        return {
            "hp": stats[0],
            "atk": stats[1],
            "def": stats[2],
            "spa": stats[3],
            "spd": stats[4],
            "spe": stats[5],
            "total": sum(stats)
        }

    def _get_pokemon_egg_groups(self, species_id):
        _SPECIES_ID = 0
        _EGG_GROUP_ID = 1

        species_egg_groups = filter(lambda r: r[_SPECIES_ID] == str(species_id), self.pokemon_egg_groups_db)
        egg_group_ids = map(lambda r: r[_EGG_GROUP_ID], species_egg_groups)
        egg_group_names = list(map(lambda r: self._egg_group_id_to_name(r), egg_group_ids))
        return egg_group_names

    def _type_id_to_name(self, type_id):
        _TYPE_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        type_names = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.type_names_db)
        result = filter(lambda r: r[_TYPE_ID] == str(type_id), type_names)
        result = list(result)

        if len(result) != 1:
            raise UnknownPokemonTypeIdException
        return str(result[0][_NAME])

    def _ability_id_to_name(self, ability_id):
        _ABILITY_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        ability_names = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.ability_names_db)
        result = filter(lambda r: r[_ABILITY_ID] == str(ability_id), ability_names)
        result = list(result)

        if len(result) != 1:
            raise UnknownPokemonAbilityIdException
        return str(result[0][_NAME])

    def _egg_group_id_to_name(self, egg_group_id):
        _ABILITY_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        korean = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.egg_group_names_db)
        result = filter(lambda r: r[_ABILITY_ID] == str(egg_group_id), korean)
        result = list(result)

        if len(result) != 1:
            raise UnknownPokemonEggGroupIdException
        return str(result[0][_NAME])

    def get_move_info(self, move):
        _MOVE_ID = 0
        _TYPE = 3
        _POWER = 4
        _PP = 5
        _ACCURACY = 6
        _PRIORITY = 7
        _DAMAGE_CLASS_ID = 9
        _EFFECT_ID = 10

        move_id = self._get_move_id_by_korean_name(move)
        result = list(filter(lambda r: r[_MOVE_ID] == str(move_id), self.moves_db))

        if len(result) != 1:
            raise UnknownKoreanMoveNameException
        move_info = result[0]

        return {
            "type": self._type_id_to_name(move_info[_TYPE]),
            "damage_class": self._damage_class_id_to_name(move_info[_DAMAGE_CLASS_ID]),
            "power": move_info[_POWER],
            "pp": move_info[_PP],
            "accuracy": move_info[_ACCURACY],
            "priority": move_info[_PRIORITY],
            "fandom": self._get_fandom_wiki_link(move)
        }

    def _get_move_id_by_korean_name(self, name):
        _MOVE_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        korean = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.move_names_db)
        result = filter(lambda r: r[_NAME] == name, korean)
        result = list(result)

        if len(result) != 1:
            raise UnknownKoreanMoveNameException
        return int(result[0][_MOVE_ID])

    def _damage_class_id_to_name(self, damage_class_id):
        _DAMAGE_CLASS_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        korean = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.move_damage_classes_db)
        result = filter(lambda r: r[_DAMAGE_CLASS_ID] == damage_class_id, korean)
        result = list(result)

        if len(result) != 1:
            raise UnknownMoveDamageClassIdException
        return result[0][_NAME]

    def _get_fandom_wiki_link(self, keyword):
        _PREFIX = "https://pokemon.fandom.com/ko/wiki/"

        return "".join([_PREFIX, keyword])

    def _get_pokemon_image(self, species_id):
        if int(species_id) < 100:
            return "https://www.serebii.net/pokemon/art/{:03}.png".format(species_id)
        else:
            return "https://www.serebii.net/pokemon/art/{}.png".format(species_id)
