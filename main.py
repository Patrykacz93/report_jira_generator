import tkinter
from tkinter import *
from PIL import ImageTk, Image
from test import Logowanie
from tkinter import messagebox as m_box
from tkcalendar import Calendar
import customtkinter
import re
from docxtpl import DocxTemplate
import os

class Window:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (330 / 2)
        self.master.geometry('%dx%d+%d+%d' % (600, 330, x, y))
        self.master.configure()
        # self.master.overrideredirect(True)
        customtkinter.set_appearance_mode("Light")

        self.frame = customtkinter.CTkFrame(self.master,
                                            width=300,
                                            height=300,
                                            corner_radius=10,
                                            background='white')

        self.img = ImageTk.PhotoImage(Image.open('logo2.png'))

        self.image = Label(self.frame, image=self.img, border=0)
        self.image.pack()

        self.mail_var = StringVar()
        self.token_var = StringVar()

        self.frame_mail = customtkinter.CTkFrame(self.frame)


        self.label2 = customtkinter.CTkLabel(self.frame_mail,
                                           text='E-mail: ',
                                           width=120,
                                           height=25,
                                           corner_radius=8,
                                           text_color='black',
                                           text_font='OpenSans, 14')

        self.label2.pack(pady=10, side=LEFT)


        self.email_entry = customtkinter.CTkEntry(self.frame_mail,
                                             textvariable=self.mail_var,
                                             width=170,
                                             height=35,
                                             corner_radius=8)

        self.email_entry.pack(padx=10, pady=10, side=LEFT)
        self.frame_mail.pack()

        self.token_frame = customtkinter.CTkFrame(self.frame)

        self.label3 = customtkinter.CTkLabel(self.token_frame,
                                             text='Token: ',
                                             width=120,
                                             height=25,
                                             corner_radius=8,
                                             text_color='black',
                                             text_font='OpenSans, 14')

        self.label3.pack(pady=10, side=LEFT)

        token_entry = customtkinter.CTkEntry(self.token_frame,
                                             textvariable=self.token_var,
                                             width=170,
                                             height=35,
                                             corner_radius=8,
                                             show='*')

        token_entry.pack(padx=10, pady=10, side=LEFT)

        self.token_frame.pack()

        button = customtkinter.CTkButton(self.frame,
                                         text = "Log In",
                                         command=self.submit,
                                         width=120,
                                         height=32,
                                         border_width=0,
                                         corner_radius=8,
                                         text_color='white',
                                         text_font='OpenSans, 14')
        button.pack(padx=10, pady=10)

        self.frame.pack(fill='both',expand=True,padx=10, pady=10)

    def userLogin(self):
        self.jira_user = Logowanie('https://globalcontrol5.atlassian.net/', self.mail_var.get(),
                                   self.token_var.get())
        print('Zalogowano')
        return self.jira_user

    def submit(self):
        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(self.regex, self.mail_var.get())):
            self.userLogin()
            self.master.withdraw()
            self.toplevel = Toplevel(self.master)
            SecondWindow(self.toplevel, self.update)
        else:
            m_box.showerror('Error', 'Błędny email')

    def update(self):
        return self.mail_var.get(), self.token_var.get()


class SecondWindow:
    def __init__(self, master, update):
        self.master = master
        self.master.geometry('700x530')
        self.frame = Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.first_window_update_function = update

        button = Button(self.master, text="Take data", command=self.get_csd_data).place(x= 10, y= 480)
        button1 = Button(self.master, text="Save to PDF", command=self.get_csd_data).place(x=110, y=480)
        button2 = Button(self.master, text="Save to DOCX", command=self.save_to_docx).place(x=210, y=480)

        self.csd_var = StringVar()
        csd_label = Label(self.master, text='Wprowadź numer CSD a następnie kliknij "Take data"').place(x= 10, y= 370)
        csd_label_2 = Label(self.master, text='CSD: ').place(x= 10, y= 398)
        csd_entry = Entry(self.master, textvariable=self.csd_var, width=10).place(x= 50, y= 400)

        label = Label(self.master, text='Numer CSD:').place(x=10, y=30)
        label1 = Label(self.master, text='Tytuł sprawy:').place(x=10, y=80)
        label2 = Label(self.master, text='Przypisany:').place(x=10, y=130)
        label3 = Label(self.master, text='Komponent:').place(x=10, y=180)
        label4 = Label(self.master, text='Ilość:').place(x=10, y=230)
        label5 = Label(self.master, text='Reporter:').place(x=10, y=280)

        creation_date = Calendar(self.master, selectmode = 'day').place(x=350, y=30)



    def get_csd_data(self):
        self.sec_jira_user = Logowanie('https://globalcontrol5.atlassian.net/',
                                        self.first_window_update_function()[0],
                                        self.first_window_update_function()[1])

        label_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[0]).place(x=250, y=30)
        label1_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[1]).place(x=250, y=80)
        label2_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[3]).place(x=250, y=130)
        label3_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0]).place(x=250, y=180)
        label4_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[4]).place(x=250, y=230)
        label5_1 = Label(self.master, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[5]).place(x=250, y=280)

    def save_to_docx(self):
        self.dokument = DocxTemplate('RETURN AUTHORIZATION FORM_2.0.docx')
        self.context = {'rma': 'RMA/2022/01/01',
                        'cp': 'BTiB',
                        'mail': self.sec_jira_user.take_csd_data(self.csd_var.get())[5],
                        'csd': self.sec_jira_user.take_csd_data(self.csd_var.get())[0],
                        'date': '10.10.2022',
                        'device': self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0],
                        'sn': '233445',
                        'fw': '2.1',
                        'problem': 'nie dziala'}

        self.nowydoc = self.dokument.render(self.context)
        self.dokument.save('newRETURN AUTHORIZATION FORM_2.0.docx')


root = Tk()
window = Window(root)
root.mainloop()