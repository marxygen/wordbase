from exceptions import *
import os
import json
from json.decoder import JSONDecodeError
from presets import *


def get_items_in_dict(dictionary):
    path = os.path.normpath(dictionary)
    try:
        with open(path, 'r' if os.path.exists(path) else 'a+') as file:
            words = json.load(file)
            return words
    except JSONDecodeError:
        raise EmptyDictionaryException
    except PermissionError:
        raise PermissionDeniedException
    except Exception:
        raise CannotOpenDictionaryException('Couldn\'t open the dictionary')


def find_word(dictionary, target):
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


def find_words_with_query(dictionary, query):
    try:
        words = get_items_in_dict(dictionary)
        return [word for word in words.items() if query in parse_word_item(word[1])[1]]
    except EmptyDictionaryException:
        raise
    except CannotOpenDictionaryException:
        raise


def get_available_dictionaries(path=STORAGE_PATH):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(DICTIONARY_EXTENSION)]
