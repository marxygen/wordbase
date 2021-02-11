import os

STORAGE_PATH = os.path.join(
    os.environ['USERPROFILE'], 'Documents', 'Wordbase Dictionaries')
DICTIONARY_EXTENSION = ".wordbase"

TRANSLATION_KEY = 'translation'
EXPLANATION_KEY = 'explanation'

ACTIVATE_CONSOLE_MODE = ['-C', '--console', '-c']
QUIT = ['quit', 'exit']
HELP = ['-H', '-h', '--help']
CHANGE_DEF_WDICT = 'wdict'
INITDIR = 'initdir'
ADDWORD = 'addword'
LISTWORDS = 'listwords'
EDITWORD = 'editword'


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


HELP_STR = """- quit / exit = Terminate the script
- initdir [path/to/file] = Create an empty dictionary. It will be used as your default dictionary
- wdict [path/to/dict] = Make the specified dictionary your default dictionary
- listwords = List all words in a dictionary
- addword [word] = Add a new word to the dictionary. If such word already exists, it will be overwritten
- editword [word] = Edit the information about this word. If this word doesn't exist in thid dictionary, it will be added
"""
