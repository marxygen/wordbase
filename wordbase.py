from exceptions import *
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

if not sys.version_info[0] == 3 or not sys.version_info[1] < 8:
    # if Python 3.[< 8].x is running, tuple unpacking won't be executed and will result in an error
    print('This project is designed to be executed with Python 3.x.x\nTerminating...')
    raise SystemExit

root = tk.Tk()
root.title('Wordbase')
root.geometry("{0}x{1}+300+100".format(root.winfo_screenwidth()//2,
                                       root.winfo_screenheight()//2))
app = WordbaseApplication(
    master=root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
app.mainloop()
