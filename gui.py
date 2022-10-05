import tkinter as tk
from tkinter import messagebox as m_box
from test import Logowanie
from tkinter import Menu
import re



class Window1:
    def __init__(self, master):
        self.master = master
        self.master.geometry('500x400')
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text='Log', fg='blue', font='Helvetica 16 bold italic')
        self.label.place(x = 190, y = 100)
        self.button1 = tk.Button(self.frame, text = 'Log In', width = 25, command = self.new_window).grid(padx = 20, pady = 300)
        self.token_label = tk.Label(self.master, text='Token')
        self.token_label.place(x = 120, y = 197)
        self.email_label = tk.Label(self.master, text='E-mail')
        self.email_label.place(x = 120, y = 147)
        self.token_entry = tk.Entry(self.master, width = 25)
        self.token_entry.place(x = 175, y = 200)
        self.email_entry = tk.Entry(self.master, width = 25)
        self.email_entry.place(x = 175, y = 150)
        self.frame.pack()
        self.jira_user = None


    def userLogin(self):
        self.jira_user = Logowanie('https://globalcontrol5.atlassian.net/', self.email_entry.get(),
                                   self.token_entry.get())
        print('Zalogowano')
        return self.jira_user

    def new_window(self):
        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(self.regex, self.email_entry.get())):
            self.userLogin()
            self.master.withdraw()
            self.toplevel = tk.Toplevel(self.master)
            Window2(self.toplevel, self.userLogin())
        else:
            m_box.showerror('Error','Błędny email')

class Window2():
    def __init__(self, master, userLogin):
        self.master = master
        self.master.geometry('500x400')
        self.login = userLogin
        self.menu = tk.Menu(self.master, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
        self.file = Menu(self.menu, tearoff=1, background='#ffcc99', foreground='black')
        self.file.add_command(label="New")
        self.file.add_command(label="Open")
        self.file.add_command(label="Save")
        self.file.add_command(label="Save as")
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Take Data From Jira', width = 25, command = self.take_data)
        self.quitButton.pack()
        self.frame.pack()


    # def take_data(self):


def main():
    root = tk.Tk()
    app = Window1(root)
    root.mainloop()

if __name__ == '__main__':
    main()