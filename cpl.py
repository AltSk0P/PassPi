import tkinter as tk
import sqlite3
from datetime import datetime

class Checkbuttons(tk.Frame):
    def __init__(self, parent=None, picks=[]):
        tk.Frame.__init__(self, parent)
        self.num = 3
        self.vars = []
        self.chkBoxes = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side='top', anchor='center', expand='YES')
            self.chkBoxes.append(chk)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)

    def reset(self):
        for chk in self.chkBoxes:
            chk.deselect()


class Screen(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.stage = 0
        self.input = ""
        self.frame = tk.Frame(self)

        self.setup()
        self.display()

    def setup(self):
        self.Entry = tk.Entry(self, width=50, justify='center')
        self.Entry.grid(row=0, column=1)
        self.Entry.bind('<Return>', self.parse)
        self.opts = Checkbuttons(self,['Student Success Coach','Study Space','Models'])
        self.opts.grid(row=0, column=1)
        self.submitButton = tk.Button(self, text="Submit",
                            command=self.submit)
        self.submitButton.grid(row=1, column=1)

    def parse(self,event):
        self.input = str(self.Entry.get())
        if (len(self.input)==6):
            self.stage=1
            self.Entry.delete(0, 'end')
            self.display()
        else:
            self.Entry.delete(0, 'end')

    def display(self):
        if (self.stage==0):
            self.input = ""
            self.opts.grid_remove()
            self.submitButton.grid_remove()
            self.Entry.grid()
            self.Entry.focus()
        else:
            self.Entry.grid_remove()
            self.opts.grid()
            self.opts.reset()
            self.submitButton.grid()

    def submit(self):
        conn = sqlite3.connect('.database/data.db')
        c = conn.cursor()
        print(list(self.opts.state()))
        params = (self.input, str(datetime.now()), 'Reason', str(datetime.now()))
        c.execute("INSERT INTO JOURNAL VALUES (?,?,?,?)",params)
        conn.commit()
        c.execute('SELECT * FROM JOURNAL')
        print(c.fetchall())
        #conn.close()
        #TODO write info
        self.stage=0
        self.display()


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("800x480")
    my_app = Screen(root)
    my_app.grid(row=0, column=0)
    root.mainloop()
