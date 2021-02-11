import os

STORAGE_PATH = os.path.join(
    os.environ['USERPROFILE'], 'Documents', 'Wordbase Dictionaries')
DICTIONARY_EXTENSION = ".wordbase"

TRANSLATION_KEY = 'translation'
EXPLANATION_KEY = 'explanation'


def create_word_item(translation, explanation):
    """
    Builds a JSON dictionary representing the given word
    """
    return {TRANSLATION_KEY: translation, EXPLANATION_KEY: explanation}


def parse_word_item(item):
    """
    Returns (word, translation, explanation) for a given item
    """
    if not [TRANSLATION_KEY, EXPLANATION_KEY] == list(item.keys()):
        return False
    return (item[TRANSLATION_KEY], item[EXPLANATION_KEY])
