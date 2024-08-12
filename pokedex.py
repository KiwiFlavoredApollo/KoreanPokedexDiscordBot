import csv
import json

ENGLISH = 9
KOREAN = 3


class UnknownKoreanPokemonNameException(Exception):
    pass


class UnknownPokemonSpeciesIdException(Exception):
    pass


class KoreanPokedex:
    def __init__(self):
        self.species_db = self._import_csv('database/pokemon_species_names.csv')
        self.types_db = self._import_csv('database/type_names.csv')
        self.ability_db = self._import_csv('database/ability_names.csv')

    def _import_json(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def _import_csv(self, path):
        with open(path, 'r', encoding='utf-8', newline='') as file:
            return list(csv.reader(file))

    def _translate_pokemon_name_korean_to_english(self, korean):
        species_id = self._get_species_id(korean)
        return self._get_pokemon_english_name(species_id)

    def _get_species_id(self, korean_pokemon_name):
        _SPECIES_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        korean = filter(lambda r: r[_LANGUAGE] == str(KOREAN), self.species_db)
        result = filter(lambda r: r[_NAME] == korean_pokemon_name, korean)
        result = list(result)

        if len(result) != 1:
            raise UnknownKoreanPokemonNameException
        return int(result[0][_SPECIES_ID])

    def _get_pokemon_english_name(self, species_id):
        _SPECIES_ID = 0
        _LANGUAGE = 1
        _NAME = 2

        english = filter(lambda r: r[_LANGUAGE] == str(ENGLISH), self.species_db)
        result = filter(lambda r: r[_SPECIES_ID] == str(species_id), english)
        result = list(result)

        if len(result) != 1:
            raise UnknownPokemonSpeciesIdException
        return str(result[0][_NAME])
