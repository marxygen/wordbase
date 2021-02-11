from exceptions import *
import os
import json
from json.decoder import JSONDecodeError
from presets import parse_word_item, create_word_item


def get_items_in_dict(dictionary):
    path = os.path.normpath(dictionary)
    try:
        with open(path, 'r' if os.path.exists(path) else 'a+') as file:
            words = json.load(file)
            return words
    except JSONDecodeError as e:
        print(e)
        raise EmptyDictionaryException
    except Exception as e:
        print(e)
        raise CannotOpenDictionaryException('Couldn\'t open the dictionary')


def find_word(dictionary, target):
    path = os.path.normpath(dictionary)
    try:
        words = get_items_in_dict(dictionary)
        target_data = words.get(target)
        if not target_data:
            raise WordNotFoundException

        # alternatively, return target, *parse_word_item(target_data), but ONLY for Python 3.8.x or greater
        translation, explanation = parse_word_item(target_data)
        return target, translation, explanation
    except WordNotFoundException:
        raise
    except Exception as e:
        print(e)
        raise CannotCompleteSearchException


def save_dictionary(path, data):
    path = os.path.normpath(path)
    try:
        with open(path, 'w' if os.path.exists(path) else 'a+') as file:
            json.dump(data, file)
    except Exception as e:
        print(e)
        raise CannotSaveDictionaryException


def delete_word(dictionary, word):
    try:
        words = get_items_in_dict(dictionary)
        del words[word]
        save_dictionary(dictionary, words)
    except CannotOpenDictionaryException:
        raise
    except CannotSaveDictionaryException:
        raise
    except Exception as e:
        print(e)
        raise CannotDeleteWordException


def append_info(dictionary, word, translation, explanation):
    """
    This function adds a new word to the dictionary or modifies the existing word
    """
    try:
        words = get_items_in_dict(dictionary)
        words[word] = create_word_item(translation, explanation)
        save_dictionary(dictionary, words)
    except CannotSaveDictionaryException:
        raise
    except CannotOpenDictionaryException:
        raise
