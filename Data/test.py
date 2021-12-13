import tkinter as tk
import time
from datetime import datetime

import label as label


def set_label():
   currentTime = datetime.datetime.now()
   label['text'] = currentTime
   root.after(1, set_label)

   root = tk.Tk()
   label = tk.Label(root, text = "placeholder")
   label.pack()

   set_label()
   root.mainloop()