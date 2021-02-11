from exceptions import CannotOpenDictionaryException
from operations import *
from presets import *
import os

CURRENT_DICTIONARY = None


def console_mode():
    global CURRENT_DICTIONARY
    print('-'*10, 'WORDBASE CONSOLE MODE', '-'*10)
    print('Looking for dictionaries...')
    dicts = get_available_dictionaries(os.getcwd())
    if not dicts:
        print(f'None found in {os.getcwd()}\n')
    else:
        print(f'Found {len(dicts)} dictionaries:')
        for index, d in enumerate(dicts):
            print(f'{index+1}) {d}')
    while True:
        command = input(
            f'\n{CURRENT_DICTIONARY if CURRENT_DICTIONARY else ""}> ')

        if command in QUIT:
            break
        elif command in HELP:
            print(HELP_STR)
        elif command.startswith(INITDIR):
            if len(command) == len(INITDIR):
                print(
                    f'Specify the path to the new dictionary using "{INITDIR} [path]".\nYou can use relative paths')
                continue
            path = command.split(' ')[1]
            if path.endswith('/') or path.endswith('\\'):
                path = path[:-1]
            if not path.endswith(DICTIONARY_EXTENSION):
                path += DICTIONARY_EXTENSION
            print(f'Attempting to create an empty dictionary in {path}')

            try:
                _ = get_items_in_dict(path)
                CURRENT_DICTIONARY = path
            except PermissionDeniedException:
                print(
                    'Error: script was denied permissions to operate the files. Pleake sure the script is launched appropriately')
            except EmptyDictionaryException:
                # ok, it was just created
                CURRENT_DICTIONARY = path
                print(f'Successfully initialized dictionary {path}')
                print(
                    f'This is your default working dictionary. Change it with "{CHANGE_DEF_WDICT} [path]" command')
                print(
                    'Any command you call that deals with a particular dictionary will be applied to this one')
            except Exception as e:
                print(f'Error: couldn\'t finish the operation: {e}')
        elif command.startswith(ADDWORD):
            path = CURRENT_DICTIONARY
            if not path:
                path = input(
                    'Default dictionary not specified. Please enter the dictionary to which to add this word > ')
            if not path:
                print('Error: invalid path')
                continue
            if len(command) == len(ADDWORD):
                print('Error: no word entered')
                continue
            word = command.split(' ')[1]
            translation = input('\tTranslation > ')
            explanation = input('\tExplanation > ')
            if not word or not translation or not explanation:
                print('Error: invalid input')
                continue
            try:
                append_info(path, word, translation, explanation)
                print('Completed successfully')
            except EmptyDictionaryException:
                try:
                    save_dictionary(
                        path, {word: create_word_item(translation, explanation)})
                    print('Completed successfully')
                except:
                    print('Error: couldn\'t complete the operation')
            except CannotSaveDictionaryException:
                print('Error: Couldn\'t save the dictionary')
        elif command in LISTWORDS:
            d = CURRENT_DICTIONARY
            if not d:
                d = input('Specify the dictionary > ')
            print(f'Listing items in {d}')
            try:
                items = get_items_in_dict(d)
                print(f'{len(items)} words found')
                for index, item in enumerate(items):
                    print(f'{index+1}) {item}')
            except EmptyDictionaryException:
                print('This dictionary is empty')
            except CannotOpenDictionaryException:
                print('Error: cannot open dictionary')
        elif command.startswith(CHANGE_DEF_WDICT):
            if len(command) == len(CHANGE_DEF_WDICT):
                print(
                    f'Error: specify the path to the dictionary: "{CHANGE_DEF_WDICT} [path]"')
                continue
            path = command.split(' ')[1]
            try:
                words = get_items_in_dict(path)
                print(f'Success! {path} is now your default dictionary!')
                print(f'{len(words)} words found in {path}')
                CURRENT_DICTIONARY = path
            except EmptyDictionaryException:
                print(f'Success! {path} is now your default dictionary!')
                print('This dictionary is empty')
                CURRENT_DICTIONARY = path
            except WordbaseException:
                print('Something went wrong. Please check the entered path')
                print('Your default working dictionary was not changed')
        elif command.startswith(EDITWORD):
            if len(command) == len(EDITWORD):
                print('Error: specify the word to edit')
                continue
            word = command.split(' ')[1]
            try:
                ...
            except:
                ...
        else:
            print(f'Unknown command: "{command}"')

    print('Terminating...')
    raise SystemExit
