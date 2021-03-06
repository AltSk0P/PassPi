import tkinter as tk
import sqlite3
import time as time
from datetime import timedelta
from datetime import datetime
import random

class Checkbuttons(tk.Frame):
    def __init__(self, parent=None, picks=[]):
        tk.Frame.__init__(self, parent)
        self.num = picks.__sizeof__()
        self.vars = []
        self.chkBoxes = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var, font=("Arial", 18))
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
        #Set initial variables and connect to database
        tk.Frame.__init__(self, *args, **kwargs)
        self.stage = 0
        self.input = ""
        self.frame = tk.Frame(self)
        self.connection = sqlite3.connect('.database/data.db')

        # Setup the GUI
        self.setup()
        self.loadLines()

        # Start display
        self.display()

    def setup(self):
        self.Label = tk.Label(self,text='SCAN YOUR ID',foreground='#981a31',font=("Arial Black", 32))
        self.Label.grid(row=0,column=1)
        self.Entry = tk.Entry(self, width=30, justify='center',font=("Arial Black", 14))
        self.Entry.grid(row=1, column=1)
        self.Entry.bind('<Return>', self.parse)
        self.Reasons = ['Student Success Coach','Study Space','Models']
        self.opts = Checkbuttons(self,self.Reasons)
        self.opts.grid(row=0, column=1)
        self.submitButton = tk.Button(self, text="Submit",
                            command=self.submit,font=("Arial Black", 18))
        self.submitButton.grid(row=1, column=1)
        self.EndLabel1 = tk.Label(self,text='WELCOME',foreground='#981a31',font=("Arial Black", 32))
        self.EndLabel1.grid(row=1,column=1)
        self.EndLabel2 = tk.Label(self, text='HAVE A GREAT DAY', foreground='#981a31', font=("Arial Black", 32))
        self.EndLabel2.grid(row=1, column=1)

    def req(self,mode,**kwargs):
        conn = self.connection
        with conn:
            print("Requested a "+mode+" operation.")
            c = conn.cursor()
            ID = kwargs.get('ID',None)
            SignIn = kwargs.get('SignIn',None)
            reason = kwargs.get('reason',None)
            if mode=='find':
                params = (self.input,)
                c.execute(
                    "SELECT * FROM JOURNAL WHERE ID=? AND SignIn>=datetime('now', 'localtime', 'start of day') AND SignIn<datetime('now', '+1 day','localtime','start of day') AND SignOut IS NULL", params)
                return c.fetchall()
            elif mode=='update':
                params = (str(datetime.now()),ID,SignIn,)
                c.execute(
                    "UPDATE JOURNAL SET SignOut=? WHERE ID=? AND SignIn=?", params)
            elif mode=='selectall':
                c.execute('SELECT * FROM JOURNAL')
                return c.fetchall()
            elif mode == 'insert':
                params = (self.input, str(datetime.now()), reason, None)
                c.execute("INSERT INTO JOURNAL VALUES (?,?,?,?)", params)

    def parse(self,event):
        if self.stage == 0:
            try:
                self.input = str(int(str(self.Entry.get())))
            except ValueError:
                self.Entry.delete(0, 'end')
                return

            self.Entry.delete(0, 'end')
            if (len(self.input)==6):
                self.passRecord()
        else:
            self.Entry.delete(0, 'end')

    def passRecord(self):
        list = self.req('find')
        print("Find operation returned: ")
        print(list)
        if not list:
            self.stage = 1
            self.display()
        else:
            for a,b,c,d in list:
                self.req('update', ID=a, SignIn=b)
                self.stage=3
                self.display()
        #print(self.req('selectall'))

    def display(self):
        if self.stage == 0:
            self.input = ""
            self.EndLabel1.grid_remove()
            self.EndLabel2.grid_remove()
            self.opts.grid_remove()
            self.submitButton.grid_remove()
            self.Label.grid()
            self.Entry.grid()
            self.Entry.focus()
        elif self.stage == 1:
            self.Entry.grid_remove()
            self.Label.grid_remove()
            self.opts.grid()
            self.opts.reset()
            self.submitButton.grid()
            #self.job = self.after(20,self.submit())
        elif self.stage == 2: # Walkin Welcome
            self.opts.grid_remove()
            self.submitButton.grid_remove()
            self.EndLabel1['text'] = self.randomText(True)
            self.EndLabel1.grid()
            self.EndLabel1.update()
            self.backToStage0()
        elif self.stage == 3: # Walkout Goodbye
            self.input = ""
            self.Entry.grid_remove()
            self.Label.grid_remove()
            self.EndLabel2['text'] = self.randomText(False)
            self.EndLabel2.grid()
            self.EndLabel1.update()
            self.backToStage0()

    def backToStage0(self):
        time.sleep(1.5)
        self.stage=0
        self.display()

    def reasons(self,list):
        output = ''
        i = 0 # amount of iterations
        n = 0 # how many were actually inserted (for comma delimiter positioning)
        for item in list:
            if item == 1:
                if n > 0:
                    output+=', '
                output += self.Reasons[i]
                n += 1
            i+=1
        return output

    def submit(self):
        reasonList = list(self.opts.state())
        reason = self.reasons(reasonList)
        self.req('insert',reason=reason)
        #print(self.req('selectall'))
        self.stage=2
        self.display()

    def loadLines(self):
        self.greetLines = []
        self.byeLines = []
        with open("locale") as f:
            content = f.readlines()
            for line in content:
                if line[0] != '#': # if not a comment
                    try:
                        if line[0] == 'I':
                            self.greetLines += [line[3:]]*int(line[1])
                        else:
                            self.byeLines += [line[3:]] * int(line[1])
                    except IndexError:
                        print("IndexError thrown")

    def randomText(self,isIn):
        if isIn: # display Greetings
            return random.choice(self.greetLines)
        else:
            return random.choice(self.byeLines)


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("800x480")
    root.attributes("-fullscreen", True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    my_app = Screen(root)
    my_app.grid(row=0, column=0)
    root.mainloop()
