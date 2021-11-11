# Import necessary packages for operation
import eel 
import tkinter as tk
import tkinter.filedialog as fd
import pathlib
import pandas as pd
from time import sleep
from Concordance import Concordance

eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def filePathRetrieve():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filePath = fd.askopenfilenames(parent=root, title='Choose Files')
    return filePath

@eel.expose
def concordanceSubmit(files):
    concordance = Concordance(files)
    concordance.format()
    return 'Data Generated'

eel.start('index.html', size=(1100, 770), port=8080) 