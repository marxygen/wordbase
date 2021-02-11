from presets import ACTIVATE_CONSOLE_MODE
from exceptions import *
from console import console_mode
try:
    import tkinter as tk
except ImportError:
    print('There was an error importing Tkinter. It might happen if you use Python 2.x.x. \
         In this case you have to install Python 3.x.x\nIf not, there is a possibility\
              that you\'re working in a separate virtual environment\nInstall with \n\tpip install tkinter')
    raise SystemExit

import sys
from Application import WordbaseApplication

if __name__ != "__main__":
    raise IncorrectExecutionException('This file is to be executed directly')

if len(sys.argv) > 1 and sys.argv[1] in ACTIVATE_CONSOLE_MODE:
    try:
        console_mode()
    except KeyboardInterrupt:
        print('Script terminated via Keyboard')
        if not input('Do you want to open the program window (yes/no)> ') == 'yes':
            raise SystemExit

if not sys.version_info[0] == 3:
    # tuple exception may result in an error in earlier versions of Python
    print('This project is designed to be executed with Python 3.x.x\nTerminating...')
    raise SystemExit

opendict = sys.argv[1] if len(
    sys.argv) > 1 and sys.argv[1] not in ACTIVATE_CONSOLE_MODE else None

root = tk.Tk()
root.title('Wordbase')
root.geometry("{0}x{1}+300+100".format(1000,
                                       root.winfo_screenheight()//2))
app = WordbaseApplication(
    master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), opendict=opendict)
app.mainloop()
