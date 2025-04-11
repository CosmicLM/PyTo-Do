from tkinter import Tk

root = Tk()

root.mainloop()

class Page(Tk.Frame):
    '''Enables switching between pages of a window.'''
    def __init__(self):
        super(Page, self).__init__()
        self.widgets={}
        self.grid(column=0,row=0)