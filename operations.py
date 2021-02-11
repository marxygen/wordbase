from exceptions import *
import os
import json
from json.decoder import JSONDecodeError
from presets import parse_word_item


def get_items_in_dict(dictionary):
    path = os.path.normpath(dictionary)
    try:
        with open(path, 'r' if os.path.exists(path) else 'a+') as file:
            words = json.load(file)
            return words
    except JSONDecodeError as e:
        raise EmptyDictionaryException
    except Exception as e:
        raise CannotOpenDictionaryException('Couldn\'t open the dictionary')


def find_word(dictionary, target):
    try:
        words = get_items_in_dict(dictionary)
        target_data = words.get(target)
        if not target_data:
            raise WordNotFoundException
        return target, *parse_word_item(target_data)
    except WordNotFoundException:
        raise
    except Exception:
        raise CannotCompleteSearchException
