from tkinter import *
from tkinter import messagebox, filedialog
import os
from presets import *
from datetime import datetime as dt
from operations import *
from exceptions import *


class SearchQueryResults(object):
    def __init__(self, master, showword, available_words):
        top = self.top = Toplevel(master)
        self.selected_word = None
        self.showword = showword
        self.available_words = available_words
        top.resizable(False, False)
        top.geometry("{0}x{1}+600+200".format(400,
                                              300))
        self.top.protocol("WM_DELETE_WINDOW", self.cleanup)

        self.header = Label(top,
                            text='Search successful\nPick a word to view it. All words below match your search query', padx=10)
        self.header.grid(row=1, column=1)
        self.avd = Listbox(top, width=70, height=12, selectmode='SINGLE')
        self.avd.grid(row=2, column=1)

        self.pickbttn = Button(top, text='Pick this one',
                               command=self.pick)
        self.pickbttn.grid(row=3, column=1)

        self.onload()

    def onload(self):
        for index, word in enumerate(self.available_words):
            translation, explanation = parse_word_item(word[1])
            self.avd.insert(
                index+1, f'{word[0]} - {translation} ({explanation[:30] + ("..." if len(explanation) > 30 else "")})')

    def pick(self):
        if self.avd.curselection():
            self.selected_word = self.available_words[self.avd.curselection()[
                0]]
            self.cleanup()

    def cleanup(self):
        self.top.destroy()
        self.callback()

    def callback(self):
        if self.selected_word:
            translation, explanation = parse_word_item(self.selected_word[1])
            self.showword(self.selected_word[0], translation, explanation)


class GetSearchQuery(object):
    def __init__(self, master, got_query):
        top = self.top = Toplevel(master)
        top.attributes("-topmost", True)
        top.resizable(False, False)
        self.got_query = got_query
        top.geometry("{0}x{1}+400+200".format(400,
                                              300))

        self.header = Label(top,
                            text='Enter the search query', padx=10, font=20)
        self.header.grid(row=1, column=1)
        self.query = Text(top, width=48, height=10, padx=10, pady=10)
        self.query.grid(row=2, column=1)
        self.send = Button(top, text='Search this query',
                           command=self.query_entered, padx=10, pady=10)
        self.send.grid(row=4, column=1)

    def query_entered(self):
        if not self.query.get(0.0, END).strip():
            self.top.withdraw()
            messagebox.showerror(
                'Invalid query', 'The query you entered is invalid. No search will be performed')
            self.top.update()
            return
        self.top.withdraw()
        self.got_query(self.query.get(0.0, END).strip())


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
            return

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
    def __init__(self, master=None, width=300, height=300, opendict=None):
        super().__init__(master)
        self.master.resizable(False, False)
        self.master = master
        self.width = width
        self.height = height
        self.current_dictionary = opendict
        self.selected_word = None
        self.create_widgets()
        self.startup()

    def _pick_dictionary(self):
        self.master.withdraw()
        self.pickdict = PickDictionary(
            self.master, self._dict_selected, get_available_dictionaries())
        self.master.wait_window(self.pickdict.top)

    def load_dictionary(self, dictionary):
        self.curtr.delete(0, END)
        self.curexpl.delete(1.0, END)
        self.selected_word = None
        self.curtr.config(state='readonly')
        self.curexpl.config(state='disabled')
        self.applychanges.config(state='disabled')
        self.curword.config(text='Word: [Not selected]')

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
                    index+1, f'{word} - {translation} ({explanation[:30] + ("..." if len(explanation) > 30 else "")})')
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
        Unless one was specified using command line arguments
        If we find one, we use it
        If we find multiple, we ask the user to open one
        """
        if self.current_dictionary:
            self.load_dictionary(self.current_dictionary)
            messagebox.showinfo('Requested dictionary opened',
                                f'You requested to open the dictionary {self.current_dictionary[:30] + ("..." if len(self.current_dictionary) > 30 else "")}.\n It is done')
            return
        try:
            dicts = get_available_dictionaries()
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

    def _show_search_results(self, word, translation, explanation):
        res = SearchResults(self.master, word, translation, explanation)
        self.master.wait_window(res.top)

    def _clear_fields(self):
        self.wordt.delete(0, END)
        self.trant.delete(0, END)
        self.explt.delete(1.0, END)

    def search_for_word(self):
        """
        Goes through the dictionary trying to find the designated word
        """
        target = self.queryfield.get()
        if not target.replace(' ', ''):
            messagebox.showerror(
                'Invalid query', 'You\'ve entered an invalid query')
            return
        try:
            word, translation, explanation = find_word(
                self.current_dictionary, target)

            # display the data
            self._show_search_results(word, translation, explanation)

        except WordNotFoundException:
            messagebox.showerror(
                'No information about this word', f'Couldn\'t find this word')
            return
        except CannotCompleteSearchException as e:
            print(e)
            messagebox.showerror(
                'Error occurred', 'The search query couldn\t be executed')
            return

    def delete_wd(self):
        if not self.listbox.curselection():
            messagebox.showerror(
                'Selection empty', 'Please select a word to delete it')
            return

        try:
            word = list(get_items_in_dict(self.current_dictionary).items())[
                self.listbox.curselection()[0]][0]
            if not word:
                raise CannotDeleteWordException
            delete_word(self.current_dictionary, word)
            self.load_dictionary(self.current_dictionary)
            messagebox.showinfo(
                'Word deleted', f'The word {word} was successfully removed from this dictionary')
        except CannotDeleteWordException:
            messagebox.showerror(
                'Deletion error', 'Couldn\'t delete this word')
        except CannotOpenDictionaryException:
            messagebox.showerror(
                'Deletion error', 'Couldn\'t open the dictionary. Make sure you didn\'t delete it')
        except CannotSaveDictionaryException:
            messagebox.showerror(
                'Deletion error', 'Couldn\'t save the dictionary after deleting the word. It might still be there')

    def add_word(self):
        word = self.wordt.get().strip()
        translation = self.trant.get().rstrip()
        explanation = self.explt.get("1.0", END).rstrip()

        if not word or not translation or not explanation:
            messagebox.showerror(
                'Invalid input', 'Please make sure you filled out all the fields')
            return

        try:
            append_info(self.current_dictionary, word,
                        translation, explanation)

            messagebox.showinfo(
                'Success', f'The word "{word}" is now in this dictionary!')
            self._clear_fields()

            self.load_dictionary(self.current_dictionary)
            return
        except EmptyDictionaryException:
            # this is the first word
            try:
                save_dictionary(self.current_dictionary, {
                                word: create_word_item(translation, explanation)})

                messagebox.showinfo(
                    'Success', f'The word "{word}" is now in this dictionary!')
                self._clear_fields()

                self.load_dictionary(self.current_dictionary)
            except CannotSaveDictionaryException:
                # failed
                messagebox.showerror(
                    'Error', 'Couldn\'t save the dictionary')
        except CannotSaveDictionaryException:
            messagebox.showerror(
                'Error', 'Couldn\'t save the dictionary')
        except CannotOpenDictionaryException:
            messagebox.showerror(
                'Error', 'Couldn\'t open the dictionary')

    def word_selected(self, event):
        """
        Is called by the listbox when a word is selected
        """
        if not self.listbox.curselection():
            return

        word_data = list(get_items_in_dict(self.current_dictionary).items())[
            self.listbox.curselection()[0]]
        self.selected_word = word_data[0]

        # load data about this word

        self.curtr.delete(0, END)
        self.curexpl.delete(1.0, END)

        self.curtr.config(state='normal')
        self.curexpl.config(state='normal')

        self.curword.config(text=f'Word: {self.selected_word}')
        translation, explanation = parse_word_item(word_data[1])
        self.curtr.insert(0, translation)
        self.curexpl.insert(0.0, explanation)
        self.applychanges.config(state='normal')

    def apply_changes_to_word(self):
        if not self.selected_word:
            # this node will never be executed
            # but if a future update will introduce a bug
            # it will notify the user about it
            messagebox.showerror('No word selected',
                                 'Please select a word in the list to edit it')
            self.applychanges.config(state='disabled')
            return

        translation = self.curtr.get().rstrip()
        explanation = self.curexpl.get("1.0", END).rstrip()
        if not translation or not explanation:
            messagebox.showerror(
                'Invalid input', 'Please make sure you entered the correct information')
            return

        try:
            append_info(self.current_dictionary,
                        self.selected_word, translation, explanation)
            messagebox.showinfo(
                'Change successful', f'The word {self.selected_word} has been updated!')
            self.load_dictionary(self.current_dictionary)
        except CannotOpenDictionaryException:
            messagebox.showerror('Word change error',
                                 'Cannot open the dictionary. Please make sure the dictionary file is still there')
        except CannotSaveDictionaryException:
            messagebox.showerror('Word change error',
                                 'Cannot save the dictionary. The changes might not have been applied')

    def initiate_phrase_search(self):
        sq = GetSearchQuery(self.master, self.search_query)
        self.master.wait_window(sq.top)

    def search_query(self, query):
        try:
            results = find_words_with_query(self.current_dictionary, query)
            if not results:
                messagebox.showwarning(
                    'No matches', f'There are no words mathing your query: {query[:30] + ("..." if len(query) > 30 else "")}')
                return

            sqr = SearchQueryResults(
                self.master, self._show_search_results, results)
            self.master.wait_window(sqr.top)

        except EmptyDictionaryException:
            messagebox.showerror(
                'Error', 'Cannot perform search: the dictionary appears empty')
        except CannotOpenDictionaryException:
            messagebox.showerror('Error', 'Cannot open the dictionary')

    def create_widgets(self):
        self.menubar = Menu(self.master)
        self.menubar.add_command(
            label="Open dictionary", command=self.open_dictionary)
        self.menubar.add_command(
            label="Delete selected word", command=self.delete_wd)
        self.menubar.add_command(
            label="Search a phrase", command=self.initiate_phrase_search)
        self.master.config(menu=self.menubar)

        self.lbtitle = Label(text='')
        self.lbtitle.grid(row=0, column=1)

        self.listbox = Listbox(width=50, height=23)
        self.listbox.grid(row=1, column=1, padx=(10, 10), pady=(0, 0))
        self.listbox.bind("<<ListboxSelect>>", self.word_selected)

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

        # Word info
        self.winfo = Label(text='Word Info', font=7)
        self.winfo.place(x=700, y=5)

        self.curword = Label(text='Word: [Not selected]')
        self.curword.place(x=700, y=30)

        self.curtrl = Label(text='Translation: ')
        self.curtrl.place(x=700, y=60)
        self.curtr = Entry(state='readonly')
        self.curtr.place(x=780, y=60)

        self.expll = Label(text='Explanation: ')
        self.expll.place(x=700, y=82)
        self.curexpl = Text(width=30, height=10, state='disabled')
        self.curexpl.place(x=700, y=105)

        self.applychanges = Button(
            text='Apply', state='disabled', command=self.apply_changes_to_word)
        self.applychanges.place(x=700, y=275)
