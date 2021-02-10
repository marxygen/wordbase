from tkinter import *
from tkinter import messagebox, filedialog
import os
from presets import STORAGE_PATH, DICTIONARY_EXTENSION


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
            top, text='Directory: [Not picked]')
        self.dirl.grid(row=1, column=1)
        self.pickdb = Button(top, text='Pick directory',
                             command=self.pick_dir)
        self.pickdb.grid(row=2, column=1)
        self.filel = Label(top, text='Filename: ')
        self.filel.grid(row=3, column=1)
        self.fileinp = Entry(top, text='')
        self.fileinp.grid(row=4, column=1)
        self.pickfb = Button(top, text='Pick file', command=self.pick_file)
        self.pickfb.grid(row=5, column=1)
        self.expll = Label(
            top, text='If you want to create a new dictionary, type its name\ninto the field above')
        self.expll.grid(row=6, column=1)

        self.sendb = Button(top, text='Confirm', command=self.cleanup)
        self.sendb.grid(row=7, column=1)

    def pick_dir(self):
        picked = filedialog.askdirectory()
        if not picked:
            return
        self.chosen_dir = picked
        picked = picked if len(picked) < 40 else picked[:37] + '...'
        self.dirl.config(text=f'Directory: {picked}')

    def pick_file(self):
        """
        Opens a pick file dialog to let the user pick the file
        """
        picked = filedialog.askopenfilename(initialdir=self.chosen_dir, title="Select file", filetypes=[(
            'Wordbase dictionary files', '*.wordbase')]) if self.chosen_dir else filedialog.askopenfilename(initialdir='/', title="Select file", filetypes=[('Wordbase dictionary files', '*.wordbase')])

        if not picked:
            return

        self.chosen_filename = picked
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
            self.chosen_filename == self.chosen_filename.replace(
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
        return [os.path.join(path, f) for f in os.listdir(path) if os.isfile(os.path.join(path, f)) and f.endswith(DICTIONARY_EXTENSION)]

    def load_dictionary(self, dictionary):
        print(dictionary)

    def _dict_selected(self, path):
        self.master.update()
        self.master.deiconify()
        if not path:
            messagebox.showwarning(
                'No dictionary selected', 'It seems like you haven\'t selected a dictionary. No data will be loaded.\nPick a dictionary using the menu button')
            return

        self._save_and_load(path)

    def _pick_dictionary(self):
        """
        Displays the OpenDictionary window; the dialog will call the pick_dictionary method with data passed in
        """

        self.pickdict = OpenDictionary(self.master, self._dict_selected)
        self.master.wait_window(self.pickdict.top)

    def pick_dictionary(self):
        """
        Displays the OpenDictionary dialog
        If no dictionary was selected, displays a warning message
        If a dictionary was selected, loads it
        """
        self.master.withdraw()
        self._pick_dictionary()

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
        If we find multiple, we ask the user to pick one
        """
        try:
            dicts = self._get_available_dictionaries()
            if len(dicts) == 1:
                self._save_and_load(dicts[0])
                return

            # there are more than one dictionary available
            # show the picking tool
            self.pick_dictionary()
        except WindowsError as e:
            # Cannot find the path
            # 1. Create it
            # 2. Show Dictionary creation dialog
            try:
                os.mkdir(STORAGE_PATH)
                raise
            except:
                # Cannot create a directory
                # Inform the user
                messagebox.showerror(title='Cannot create working directory',
                                     message=f'There was an error creating directory \'{STORAGE_PATH}\'. You will have to specify the path for dictionary yourself or grant this program Administrator permissions')
                # Show the dictionary selection dialog
                self.pick_dictionary()
        except Exception as e:
            messagebox.showerror('An error occurred', e)
            raise SystemExit

    def create_widgets(self):
        self.menubar = Menu(self.master)
        self.menubar.add_command(label="Manage dictionaries")
        self.master.config(menu=self.menubar)

        self.listbox = Listbox(width=50, height=25)

        self.listbox.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))
