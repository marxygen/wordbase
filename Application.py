from tkinter import *
from tkinter import messagebox, filedialog
import os
from presets import *
import json
from json.decoder import JSONDecodeError
from datetime import datetime as dt
from operations import *
from exceptions import *


class SearchResults(object):
    def __init__(self, master, word, translation, explanation):
        top = self.top = Toplevel(master)
        top.attributes("-topmost", True)
        top.resizable(False, False)
        self.w = word
        self.t = translation
        self.e = explanation
        top.geometry("{0}x{1}+600+200".format(400,
                                              300))

        self.header = Label(top,
                            text=word, padx=10, font=20)
        self.header.grid(row=1, column=1)
        self.translation = Label(top, text=translation, font=15)
        self.translation.grid(row=2, column=1)
        self.explanation = Text(top, width=47, height=12, padx=10, pady=10)
        self.explanation.delete(1.0, "end")
        self.explanation.insert(1.0, explanation)
        self.explanation.grid(row=3, column=1)

        self.copybttn = Button(top, text='Copy to clipboard',
                               command=self.copy_to_clipboard)
        self.copybttn.grid(row=4, column=1)

    def copy_to_clipboard(self):
        try:
            import clipboard
            clipboard.copy(f'{self.w} - {self.t} ({self.e})')
            self.top.destroy()
            messagebox.showinfo(
                'Copied', 'Information about this word was copied to your clipboard')
        except:
            messagebox.showerror(
                'Clipboard not available', 'To use clipboard on this machine, Python needs "clipboard" module, which is not installed. Install it via PIP to access this functionality')


class PickDictionary(object):
    def __init__(self, master, onselected, available_dicts):
        top = self.top = Toplevel(master)
        self.onselected = onselected
        self.available_dicts = []
        self.selected_dict = []
        self.available_dicts = available_dicts
        top.resizable(False, False)
        top.geometry("{0}x{1}+600+200".format(400,
                                              300))
        self.top.protocol("WM_DELETE_WINDOW", self.cleanup)

        self.header = Label(top,
                            text='There are several dictionaries in your working directory. Pick one\nIf you want to import a dictionary from elsewhere,\njust dismiss this window and use menu button on the main page', padx=10)
        self.header.grid(row=1, column=1)
        self.avd = Listbox(top, width=70, height=12, selectmode='SINGLE')
        self.avd.grid(row=2, column=1)

        self.pickbttn = Button(top, text='Pick this one',
                               command=self.pick)
        self.pickbttn.grid(row=3, column=1)

        self.onload()

    def onload(self):
        for index, dictionary in enumerate(self.available_dicts):
            self.avd.insert(index+1, dictionary)

    def pick(self):
        if not self.avd.curselection():
            messagebox.showerror(
                'Selection empty', 'Please select a dictionary to process it or close this window')
            pass

        self.selected_dict = self.available_dicts[self.avd.curselection()[0]]
        self.cleanup()

    def cleanup(self):
        self.callback()
        self.top.destroy()

    def callback(self):
        self.onselected(self.selected_dict)


class OpenDictionary(object):
    def __init__(self, master, onselected):
        top = self.top = Toplevel(master)
        self.onselected = onselected
        self.chosen_dir = None
        self.chosen_filename = None
        top.resizable(False, False)
        top.geometry("{0}x{1}+600+200".format(300,
                                              200))
        self.top.protocol("WM_DELETE_WINDOW", self.cleanup)

        self.dirl = Label(
            top, text='Directory: [Not selected]')
        self.dirl.grid(row=1, column=1)
        self.opendb = Button(top, text='Select directory',
                             command=self.open_dir)
        self.opendb.grid(row=2, column=1)
        self.filel = Label(top, text='Filename: ')
        self.filel.grid(row=3, column=1)
        self.fileinp = Entry(top, text='')
        self.fileinp.grid(row=4, column=1)
        self.openfb = Button(top, text='Select file', command=self.open_file)
        self.openfb.grid(row=5, column=1)
        self.expll = Label(
            top, text='If you want to create a new dictionary, type its name\ninto the field above')
        self.expll.grid(row=6, column=1)

        self.sendb = Button(top, text='Confirm', command=self.cleanup)
        self.sendb.grid(row=7, column=1)

    def open_dir(self):
        opened = filedialog.askdirectory()
        if not opened:
            return
        self.chosen_dir = opened
        opened = opened if len(opened) < 40 else opened[:37] + '...'
        self.dirl.config(text=f'Directory: {opened}')

    def open_file(self):
        """
        Opens a open file dialog to let the user open the file
        """
        opened = filedialog.askopenfilename(initialdir=self.chosen_dir, title="Select file", filetypes=[(
            'Wordbase dictionary files', '*.wordbase')]) if self.chosen_dir else filedialog.askopenfilename(initialdir='/', title="Select file", filetypes=[('Wordbase dictionary files', '*.wordbase')])

        if not opened:
            return

        self.chosen_filename = opened
        self.fileinp.config(text=self.chosen_filename)

    def cleanup(self):
        self.callback()
        self.top.destroy()

    def callback(self):
        if self.fileinp.get().replace(' ', '') != '':
            self.chosen_filename = self.fileinp.get()
        if not self.chosen_dir or not self.chosen_filename:
            self.onselected(None)
            return

        if not self.chosen_filename.endswith(DICTIONARY_EXTENSION):
            self.chosen_filename = self.chosen_filename.replace(
                '.', '') + DICTIONARY_EXTENSION

        self.onselected(os.path.join(
            self.chosen_dir, self.chosen_filename))


class WordbaseApplication(Frame):
    def __init__(self, master=None, width=300, height=300):
        super().__init__(master)
        self.master.resizable(False, False)
        self.master = master
        self.width = width
        self.height = height
        self.current_dictionary = None
        self.create_widgets()
        self.startup()

    def _get_available_dictionaries(self, path=STORAGE_PATH):
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(DICTIONARY_EXTENSION)]

    def _pick_dictionary(self):
        self.master.withdraw()
        self.pickdict = PickDictionary(
            self.master, self._dict_selected, self._get_available_dictionaries())
        self.master.wait_window(self.pickdict.top)

    def load_dictionary(self, dictionary):
        self.listbox.delete(0, 'end')
        path = os.path.normpath(dictionary)
        self.current_dictionary = path
        try:
            # Keep in mind that files might be very large
            # We will remove nodes from memory as we add them to the list
            self.lbtitle.config(
                text=f'Content of dictionary {os.path.split(self.current_dictionary)[1].replace(DICTIONARY_EXTENSION, "")}')
            numof_entries = 0
            start = dt.now()
            words = get_items_in_dict(self.current_dictionary)
            for (index, (word, item)) in enumerate(list(words.items())):
                # word is now a dictionary
                translation, explanation = parse_word_item(item)
                self.listbox.insert(
                    index+1, f'{word} - {translation} ({explanation[:10] + "..."})')
                del words[word]
                numof_entries += 1

            # with open(path, 'r' if os.path.exists(path) else 'a+') as file:
            #     words = json.load(file)
            #     for (index, (word, item)) in enumerate(list(words.items())):
            #         # word is now a dictionary
            #         translation, explanation = parse_word_item(item)
            #         self.listbox.insert(
            #             index+1, f'{word} - {translation} ({explanation[:10] + "..."})')
            #         del words[word]
            #         numof_entries += 1
            elapsed = dt.now() - start
            self.numofels.config(
                text=f'{numof_entries} entries listed in {elapsed} seconds')
        except EmptyDictionaryException as ede:
            self.numofels.config(text='Dictionary is empty')
        except CannotOpenDictionaryException as cod:
            self.numofels.config(text='Couldn\'t open this dictionary')

    def _dict_selected(self, path):
        self.master.update()
        self.master.deiconify()
        if not path:
            messagebox.showwarning(
                'No dictionary selected', 'It seems like you haven\'t selected a dictionary. No data will be loaded.\nopen a dictionary using the menu button')
            return

        self._save_and_load(path)

    def _open_dictionary(self):
        """
        Displays the OpenDictionary window; the dialog will call the open_dictionary method with data passed in
        """

        self.opendict = OpenDictionary(self.master, self._dict_selected)
        self.master.wait_window(self.opendict.top)

    def open_dictionary(self):
        """
        Displays the OpenDictionary dialog
        If no dictionary was selected, displays a warning message
        If a dictionary was selected, loads it
        """
        self.master.withdraw()
        self._open_dictionary()

    def _save_and_load(self, dictionary):
        """
        Saves the dictionary to class params and loads it
        """
        self.current_dictionary = dictionary
        self.load_dictionary(self.current_dictionary)

    def startup(self):
        """
        On startup we check the directory for files
        If we find one, we use it
        If we find multiple, we ask the user to open one
        """
        try:
            dicts = self._get_available_dictionaries()
            if not dicts:
                # no dictionaies
                self.open_dictionary()
                return

            if len(dicts) == 1:
                self._save_and_load(dicts[0])
                return

            # there are more than one dictionary available
            # show the opening tool
            self._pick_dictionary()
        except WindowsError as e:
            # Cannot find the path
            # 1. Create it
            # 2. Show Dictionary creation dialog
            try:
                os.mkdir(STORAGE_PATH)
            except:
                # Cannot create a directory
                # Inform the user
                messagebox.showerror(title='Cannot create working directory',
                                     message=f'There was an error creating directory \'{STORAGE_PATH}\'. You will have to specify the path for dictionary yourself or grant this program Administrator permissions')
                # Show the dictionary selection dialog
                self.open_dictionary()
        except Exception as e:
            messagebox.showerror('An error occurred', e)
            raise SystemExit

    def _clear_fields(self):
        self.wordt.delete()
        self.trant.delete()
        self.explt.delete()

    def search_for_word(self):
        """
        Goes through the dictionary trying to find the designated word
        """
        target = self.queryfield.get()
        if not target.replace(' ', ''):
            messagebox.showerror(
                'Invalid query', 'You\'ve entered an invalid query')
            return
        target_data = None
        try:
            word, translation, explanation = find_word(
                self.current_dictionary, target)

            # display the data
            info = SearchResults(self.master, word, translation, explanation)
            self.master.wait_window(info.top)

        except WordNotFoundException:
            messagebox.showerror(
                'No information about this word', f'Couldn\'t find this word')
            return
        except CannotCompleteSearchException as e:
            print(e)
            messagebox.showerror(
                'Error occurred', 'The search query couldn\t be executed')
            return

    def add_word(self):
        word = self.wordt.get().strip()
        translation = self.trant.get().rstrip()
        explanation = self.explt.get("1.0", END).rstrip()

        if not word or not translation or not explanation:
            messagebox.showerror(
                'Invalid input', 'Please make sure you filled out all the fields')
            return

        try:
            data = None
            with open(self.current_dictionary, 'r') as file:
                data = json.load(file)

            data[word] = create_word_item(translation, explanation)

            with open(self.current_dictionary, 'w') as file:
                json.dump(data, file)

            messagebox.showinfo(
                'Success', f'The word "{word}" is now in this dictionary!')

            self.load_dictionary(self.current_dictionary)
            return
        except JSONDecodeError:
            # this is the first word
            try:
                with open(self.current_dictionary, 'w+') as file:
                    json.dump(
                        {word: create_word_item(translation, explanation)}, file)

                messagebox.showinfo(
                    'Success', f'The word "{word}" is now in this dictionary!')

                self.load_dictionary(self.current_dictionary)
            except Exception as e:
                # failed
                messagebox.showerror(
                    'Error', f'Couldn\'t perform the operation: {e}')
        except Exception as e:
            messagebox.showerror(
                'Error', f'Couldn\'t perform the operation: {e}')

    def create_widgets(self):
        self.menubar = Menu(self.master)
        self.menubar.add_command(
            label="Open dictionary", command=self.open_dictionary)
        self.master.config(menu=self.menubar)

        self.lbtitle = Label(text='')
        self.lbtitle.grid(row=0, column=1)

        self.listbox = Listbox(width=50, height=23)
        self.listbox.grid(row=1, column=1, padx=(10, 10), pady=(0, 0))

        self.numofels = Label(text='')
        self.numofels.grid(row=2, column=1)

        self.ActionsLabel = Label(text='Search', font=25)
        self.ActionsLabel.grid(row=0, column=2)

        self.SearchLabel = Label(text='Search for ')
        self.SearchLabel.grid(row=1, column=2, sticky='N')

        self.queryfield = Entry()
        self.queryfield.grid(row=1, column=3, sticky='N')

        self.searchbttn = Button(
            text='Search this word', command=self.search_for_word)
        self.searchbttn.grid(row=1, column=4, sticky='N')

        self.addwd = Label(text='Add a new word', font=25)
        self.addwd.place(x=328, y=55)

        self.wordl = Label(text='Word: ')
        self.wordl.place(x=328, y=90)
        self.wordt = Entry()
        self.wordt.place(x=370, y=90)

        self.tran = Label(text='Translation: ')
        self.tran.place(x=328, y=120)
        self.trant = Entry()
        self.trant.place(x=400, y=120)

        self.expl = Label(text='Explanation: ')
        self.expl.place(x=328, y=140)
        self.explt = Text(width=30, height=10)
        self.explt.place(x=328, y=160)

        self.addbttn = Button(text='Add', command=self.add_word)
        self.addbttn.place(x=328, y=330)