import time
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from jira_login import Logowanie
from tkinter import messagebox as m_box
from tkcalendar import Calendar
import customtkinter
import re
from docxtpl import DocxTemplate
import textwrap
import json
import threading

class Window:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (330 / 2)
        self.master.geometry('%dx%d+%d+%d' % (600, 330, x, y))
        self.master.title('Automatic Report Generator')
        self.master.configure(background = 'white')

        # self.master.overrideredirect(True)
        customtkinter.set_appearance_mode("Light")

        self.frame = customtkinter.CTkFrame(self.master,
                                            width=300,
                                            height=300,
                                            corner_radius=10,
                                            background='white')

        self.img = ImageTk.PhotoImage(Image.open('static_file/logo2.png'))

        self.image = Label(self.frame, image=self.img, border=0)
        self.image.pack()

        self.mail_var = StringVar()
        self.token_var = StringVar()
        self.checkbox_var = StringVar()

        with open ("logininfo.json", 'r') as rf:
            data = json.load(rf)

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
        if not data:
            self.email_entry.insert(0, '')
        else:
            self.email_entry.insert(0, data['login'])

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

        self.token_entry = customtkinter.CTkEntry(self.token_frame,
                                             textvariable=self.token_var,
                                             width=170,
                                             height=35,
                                             corner_radius=8,
                                             show='*')
        if not data:
            self.token_entry.insert(0, '')
        else:
            self.token_entry.insert(0, data['password'])

        self.token_entry.pack(padx=10, pady=10, side=LEFT)

        self.token_frame.pack()

        checkbox = customtkinter.CTkCheckBox(self.frame, text="Remember Login and Password", variable=self.checkbox_var,
                                            onvalue="checked", offvalue="unchecked")
        checkbox.pack(padx=10, pady=10)

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

        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

    def userLogin(self):
        self.jira_user = Logowanie('https://globalcontrol5.atlassian.net/', self.mail_var.get(),
                                   self.token_var.get())
        print('Zalogowano')
        return self.jira_user

    def submit(self):

        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(self.regex, self.mail_var.get())):
            if str(self.checkbox_var.get()) == 'checked':
                self.login_dict = {'login': self.mail_var.get(),
                                   'password': self.token_var.get()}

                with open('logininfo.json', 'w') as f:
                    json.dump(self.login_dict, f)

                self.userLogin()
                self.master.withdraw()
                self.toplevel = Toplevel(self.master)
                SecondWindow(self.toplevel, self.update)
                print('przedelse')
            else:
                self.userLogin()
                self.master.withdraw()
                self.toplevel = Toplevel(self.master)
                SecondWindow(self.toplevel, self.update)
                print('poelse')
        else:
            m_box.showerror('Error', 'Błędny email')

    def update(self):
        return self.mail_var.get(), self.token_var.get()


class SecondWindow:
    def __init__(self, master, update):
        self.master = master
        self.style = tkinter.ttk.Style()

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (790 / 2)
        y = (screen_height / 2) - (880 / 2)
        self.master.geometry('%dx%d+%d+%d' % (790, 880, x, y))
        self.master.configure(background='white')
        self.master.geometry('790x880')

        with open("organizations.json", "r") as organization_file:
            self.organizations_data = json.load(organization_file)

        self.save_frame = self.frame = customtkinter.CTkFrame(self.master, corner_radius=10)
        self.button_report_doc = customtkinter.CTkButton(self.save_frame,
                                                         text="Chose Save directory",
                                                         command=self.select_file,
                                                         border_width=0,
                                                         corner_radius=8,
                                                         text_color='white',
                                                         text_font='OpenSans 12 bold')

        self.button_report_doc.pack(side=LEFT, pady=5, padx=5)
        self.save_label = self.save_label = customtkinter.CTkLabel(self.save_frame, text='')
        self.save_label.pack(pady=5, padx=10)

        self.save_frame.pack(side=TOP,fill='x', padx=10, pady=5)

        self.frame = customtkinter.CTkFrame(self.master, corner_radius=10)

        self.first_window_update_function = update

        # button1 = Button(self.master, text="Save to PDF", command=self.get_csd_data).place(x=110, y=480)

        self.auto_label = customtkinter.CTkLabel(self.frame,
                                                 text='Field to check data',
                                                 corner_radius=8,
                                                 text_color='black',
                                                 text_font='OpenSans 14 bold')
        self.auto_label.pack(pady=5)

        self.frame_csd_number = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label = customtkinter.CTkLabel(self.frame_csd_number, text='Key:',text_font='OpenSans 10 bold')
        self.label.pack(side=TOP)
        self.frame_csd_number.pack()
        self.case_description = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label1 = customtkinter.CTkLabel(self.case_description, text='Summary:',text_font='OpenSans 10 bold')
        self.label1.pack(side=TOP)
        self.case_description.pack()
        self.organization = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label7 = customtkinter.CTkLabel(self.organization, text='Organizations:',text_font='OpenSans 10 bold')
        self.label7.pack(side=TOP)
        self.organization.pack()
        self.assigned_user = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label2 = customtkinter.CTkLabel(self.assigned_user, text='Assignee:',text_font='OpenSans 10 bold')
        self.label2.pack(side=TOP)
        self.assigned_user.pack()
        self.component = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label3 = customtkinter.CTkLabel(self.component, text='Component:',text_font='OpenSans 10 bold')
        self.label3.pack(side=TOP)
        self.component.pack()
        self.quantity = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label4 = customtkinter.CTkLabel(self.quantity, text='Quantity:',text_font='OpenSans 10 bold')
        self.label4.pack(side=TOP)
        self.quantity.pack()
        self.reporter = customtkinter.CTkFrame(self.frame, border_color= 'black', border=2)
        self.label5 = customtkinter.CTkLabel(self.reporter, text='Reporter:',text_font='OpenSans 10 bold')
        self.label5.pack(side=TOP)
        self.reporter.pack()
        self.serial_numbers_frame = customtkinter.CTkFrame(self.frame, border_color='black', border=2)
        self.label6 = customtkinter.CTkLabel(self.serial_numbers_frame, text='Serial Numbers:', text_font='OpenSans 10 bold')
        self.label6.pack(side=TOP)
        self.serial_numbers_frame.pack()


        self.csd_var = StringVar()

        self.button = customtkinter.CTkButton(self.frame,
                                              text="Take data",
                                              command=self.progress_bar_thread,
                                              border_width=0,
                                              corner_radius=8,
                                              text_color='white',
                                              text_font='OpenSans 12 bold')
        self.button.pack(pady=5, side=BOTTOM)

        self.button = customtkinter.CTkButton(self.frame,
                                              text="Clear fields",
                                              command=self.clear_label,
                                              border_width=0,
                                              corner_radius=8,
                                              text_color='white',
                                              text_font='OpenSans 12 bold')
        self.button.pack(pady=3, side=BOTTOM)

        self.frame_csd = customtkinter.CTkFrame(self.frame, corner_radius=8)

        self.csd_label = customtkinter.CTkLabel(self.frame_csd, text='Enter your CSD number, \n and click "Take data"')
        self.csd_label.pack(side=TOP, padx=3, pady=3)

        # self.csd_label_2 = customtkinter.CTkLabel(self.frame_csd, text='CSD:', corner_radius=8)
        # self.csd_label_2.pack(side=LEFT, padx=2, pady=2)

        self.csd_entry = customtkinter.CTkEntry(self.frame_csd,
                                                textvariable=self.csd_var,
                                                width=80,
                                                height=27,
                                                corner_radius=8)

        self.csd_entry.pack(side=BOTTOM, padx=3, pady=3)
        self.frame_csd.pack(side=BOTTOM, padx=20)

        self.frame_form = customtkinter.CTkFrame(self.master, corner_radius=8)

        self.form_label = customtkinter.CTkLabel(self.frame_form,
                                                 text='Fill the form field',
                                                 corner_radius=8,
                                                 text_color = 'black',
                                                 text_font = 'OpenSans 14 bold')
        self.form_label.pack(pady=5)

        self.data_field = Calendar(self.frame_form, selectmode = 'day', date_pattern='dd.mm.yyyy')
        self.data_field.pack(padx=10, pady=10)

        self.fw_label = customtkinter.CTkLabel(self.frame_form, text='FW/HW version: ', corner_radius=8)
        self.fw_label.pack()

        self.fw_var = StringVar()

        self.fw_field = customtkinter.CTkEntry(self.frame_form,
                                               textvariable=self.fw_var,
                                               width=80,
                                               height=27,
                                               corner_radius=8)
        self.fw_field.pack(padx=3, pady=3)

        self.description_label = customtkinter.CTkLabel(self.frame_form, text='Problem description: ', corner_radius=8)
        self.description_label.pack()

        self.description_field = Text(self.frame_form,
                                      width=30,
                                      height=4)
        self.description_field.pack(padx=3, pady=3)

        self.en_eu_slider = customtkinter.CTkSwitch(self.frame_form,text='UE/NoUE', onvalue="on", offvalue="off", command=self.slider_change)
        self.en_eu_slider.pack(padx=5, pady=20)

        self.button2 = customtkinter.CTkButton(self.frame_form,
                                               text="Save form to Docx",
                                               command=self.save_form_thread,
                                               border_width=0,
                                               corner_radius=8,
                                               text_color='white',
                                               text_font='OpenSans 12 bold')

        self.button2.pack(side=BOTTOM, pady=10)

        self.report_frame = customtkinter.CTkFrame(self.master, corner_radius=8)

        self.form_label = customtkinter.CTkLabel(self.report_frame,
                                                 text='Fill the report field',
                                                 corner_radius=8,
                                                 text_color = 'black',
                                                 text_font = 'OpenSans 14 bold')
        self.form_label.pack(pady=5)

        self.date_field1 = Calendar(self.report_frame, selectmode='day', date_pattern='dd.mm.yyyy')
        self.date_field1.pack(padx=10, pady=10)

        self.engineer_report_label = customtkinter.CTkLabel(self.report_frame, text='Engineer report: ', corner_radius=8)
        self.engineer_report_label.pack()

        self.engineer_report = Text(self.report_frame,
                                      width=30,
                                      height=4)
        self.engineer_report.pack(padx=3, pady=3)

        self.veryfication_team_label = customtkinter.CTkLabel(self.report_frame, text='Veryfication team: ', corner_radius=8)
        self.veryfication_team_label.pack(padx=3, pady=3)

        self.veryfication_team_combo = customtkinter.CTkComboBox(self.report_frame,
                                                                 values=["Patryk Kaczmarek", "Mateusz Naderza"])
        self.veryfication_team_combo.pack(padx=3, pady=3)

        self.veryfication_team_combo1 = customtkinter.CTkComboBox(self.report_frame,
                                                                 values=["Adam Czudowski", "Wincenty Klein"])
        self.veryfication_team_combo1.pack(padx=3, pady=3)

        self.service_status = customtkinter.CTkLabel(self.report_frame, text='Status of service: ', corner_radius=8)
        self.service_status.pack(padx=3, pady=3)

        self.service_combo = customtkinter.CTkComboBox(self.report_frame,
                                                                 values=["Repair", "Replacement","Other"])
        self.service_combo.pack(padx=3, pady=3)

        self.button_report_doc = customtkinter.CTkButton(self.report_frame,
                                                         text="Save report to Docx",
                                                         command=self.take_variable,
                                                         border_width=0,
                                                         corner_radius=8,
                                                         text_color='white',
                                                         text_font='OpenSans 12 bold')
        self.button_report_doc.pack(side=BOTTOM, pady=5)

        self.button_report_doc = customtkinter.CTkButton(self.report_frame,
                                                         text="Save report to PDF",
                                                         border_width=0,
                                                         corner_radius=8,
                                                         text_color='white',
                                                         text_font='OpenSans 12 bold')
        self.button_report_doc.pack(side=BOTTOM, pady=3)

        self.progress_bar_frame = customtkinter.CTkFrame(self.master, corner_radius=10)
        self.pg_empty_label = customtkinter.CTkLabel(self.progress_bar_frame, text='')
        self.pg_empty_label.pack(pady=2, padx=5)
        self.progress_bar_frame.pack(padx=10, pady=5, fill='x',side=BOTTOM)

        self.frame.pack(padx=10, pady=5, side=LEFT, fill='y')
        self.frame_form.pack(padx=10, pady=5, side=LEFT, fill='y')
        self.report_frame.pack(padx=10, pady=5, side=LEFT, fill='y')


    def get_csd_data(self):

        self.sec_jira_user = Logowanie('https://globalcontrol5.atlassian.net/',
                                        self.first_window_update_function()[0],
                                        self.first_window_update_function()[1])

        self.descriptiontext = textwrap.fill(self.sec_jira_user.take_csd_data(self.csd_var.get())[1], width=20)
        self.serial_number_twolines = re.sub(r',([^,]*),', r',\1\n', self.sec_jira_user.take_csd_data(self.csd_var.get())[6])

        self.update_progress_bar(0)
        self.label_1 = customtkinter.CTkLabel(self.frame_csd_number, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[0])
        self.label_1.pack(side=BOTTOM)
        self.update_progress_bar(12)
        self.label1_1 = customtkinter.CTkLabel(self.case_description, text=self.descriptiontext)
        self.label1_1.pack(side=BOTTOM)
        self.update_progress_bar(24)
        self.label7_1 = customtkinter.CTkLabel(self.organization, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name)
        self.label7_1.pack(side=BOTTOM)
        self.update_progress_bar(36)
        self.label2_1 = customtkinter.CTkLabel(self.assigned_user, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[3])
        self.label2_1.pack(side=BOTTOM)
        self.update_progress_bar(48)
        self.label3_1 = customtkinter.CTkLabel(self.component, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0])
        self.label3_1.pack(side=BOTTOM)
        self.update_progress_bar(60)
        self.label4_1 = customtkinter.CTkLabel(self.quantity, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[4])
        self.label4_1.pack(side=BOTTOM)
        self.update_progress_bar(72)
        self.label5_1 = customtkinter.CTkLabel(self.reporter, text=self.sec_jira_user.take_csd_data(self.csd_var.get())[5])
        self.label5_1.pack(side=BOTTOM)
        self.update_progress_bar(84)
        self.label6_1 = customtkinter.CTkLabel(self.serial_numbers_frame, text=self.serial_number_twolines.replace(' ',''))
        self.label6_1.pack(side=BOTTOM)
        self.update_progress_bar(100)
        time.sleep(1)

        self.progress_bar.destroy()
        self.loading_label.destroy()

        self.pg_empty_label = customtkinter.CTkLabel(self.progress_bar_frame, text='')
        self.pg_empty_label.pack(pady=2, padx=5)

    def save_to_docx(self):

        self.random_var = 1
        self.update_progress_bar(0)

        if str(self.en_eu_slider.get()) == "off":

            for organizations_key, organizations_value in self.organizations_data.items():

                if str(self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name) == str(organizations_key):

                    if int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]) <= self.random_var:

                        self.rma_regex = re.search("^[a-zA-Z0-9]{3}[/.-](\d{4})[/.-](\d{2})[/.-](\d{2})",self.descriptiontext)

                        self.dokument = DocxTemplate('template_file/RETURN AUTHORIZATION FORM_2.0.docx')
                        self.context = {'rma': self.rma_regex.group(),
                                        'cp': self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name,
                                        'mail': organizations_value,
                                        'csd': self.sec_jira_user.take_csd_data(self.csd_var.get())[0],
                                        'date': self.data_field.get_date(),
                                        'device': self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0],
                                        'sn': self.sec_jira_user.take_csd_data(self.csd_var.get())[6],
                                        'fw': self.fw_var.get(),
                                        'problem': self.description_field.get("1.0",'end-1c')}

                        self.nowydoc = self.dokument.render(self.context)
                        self.dokument.save(self.path + f'/RETURN AUTHORIZATION FORM_{self.sec_jira_user.take_csd_data(self.csd_var.get())[0]}.docx')

                    else:

                        self.rma_regex = re.search("^[a-zA-Z0-9]{3}[/.-](\d{4})[/.-](\d{2})[/.-](\d{2})", self.descriptiontext)

                        self.dokument = DocxTemplate('template_file/RETURN AUTHORIZATION FORM_2.0_loop.docx')

                        self.formRows = []
                        self.iterated_serial_numbers = self.sec_jira_user.take_csd_data(self.csd_var.get())[6].replace(' ','')

                        for sn_item in self.iterated_serial_numbers.split(','):
                            self.formRows.append({"device": "iSMA-B-"+str(self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0]), "sn": sn_item,
                                                 "fw": self.fw_var.get(), "problem":self.description_field.get("1.0",'end-1c')})

                        self.context = {'rma': self.rma_regex.group(),
                                        'cp': self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name,
                                        'mail': organizations_value,
                                        'csd': self.sec_jira_user.take_csd_data(self.csd_var.get())[0],
                                        'date': self.data_field.get_date(),
                                        'formRows': self.formRows
                                        }


                        self.nowydoc = self.dokument.render(self.context)
                        self.dokument.save(self.path + f'/RETURN AUTHORIZATION FORM_{self.sec_jira_user.take_csd_data(self.csd_var.get())[0]}.docx')
                else:
                    pass

        else:

            for organizations_key, organizations_value in self.organizations_data.items():

                if str(self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name) == str(organizations_key):

                    if int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]) <= self.random_var:

                        self.rma_regex = re.search("^[a-zA-Z0-9]{3}[/.-](\d{4})[/.-](\d{2})[/.-](\d{2})",
                                                   self.descriptiontext)

                        self.dokument = DocxTemplate('template_file/RETURN AUTHORIZATION FORM_NON_UE_CLIENT_2.0.docx')
                        self.context = {'rma': self.rma_regex.group(),
                                        'cp': self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name,
                                        'mail': organizations_value,
                                        'csd': self.sec_jira_user.take_csd_data(self.csd_var.get())[0],
                                        'date': self.data_field.get_date(),
                                        'device': self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0],
                                        'sn': self.sec_jira_user.take_csd_data(self.csd_var.get())[6],
                                        'fw': self.fw_var.get(),
                                        'problem': self.description_field.get("1.0", 'end-1c'),
                                        'cpp': self.sec_jira_user.take_csd_data(self.csd_var.get())[5],
                                        'description': str(self.combo_NoUE.get()) + str(self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0]),
                                        'quantity': int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]),
                                        'total': int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]) * 2 }

                        self.nowydoc = self.dokument.render(self.context)
                        self.dokument.save(
                            self.path + f'/RETURN AUTHORIZATION FORM_{self.sec_jira_user.take_csd_data(self.csd_var.get())[0]}.docx')

                    else:

                        self.rma_regex = re.search("^[a-zA-Z0-9]{3}[/.-](\d{4})[/.-](\d{2})[/.-](\d{2})",
                                                   self.descriptiontext)

                        self.dokument = DocxTemplate('template_file/RETURN AUTHORIZATION FORM_NON_UE_CLIENT_2.0_loop.docx')

                        self.formRows = []
                        self.iterated_serial_numbers = self.sec_jira_user.take_csd_data(self.csd_var.get())[6].replace(
                            ' ', '')

                        for sn_item in self.iterated_serial_numbers.split(','):
                            self.formRows.append(
                                {"device": "iSMA-B-" + str(self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0]),
                                 "sn": sn_item,
                                 "fw": self.fw_var.get(), "problem": self.description_field.get("1.0", 'end-1c')})

                        self.context = {'rma': self.rma_regex.group(),
                                        'cp': self.sec_jira_user.take_csd_data(self.csd_var.get())[7][0].name,
                                        'mail': organizations_value,
                                        'csd': self.sec_jira_user.take_csd_data(self.csd_var.get())[0],
                                        'date': self.data_field.get_date(),
                                        'formRows': self.formRows,
                                        'cpp': self.sec_jira_user.take_csd_data(self.csd_var.get())[5],
                                        'description': str(self.combo_NoUE.get()) + str(self.sec_jira_user.take_csd_data(self.csd_var.get())[2][0]),
                                        'quantity': int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]),
                                        'total': int(self.sec_jira_user.take_csd_data(self.csd_var.get())[4]) * 2
                                        }

                        self.nowydoc = self.dokument.render(self.context)
                        self.dokument.save(
                            self.path + f'/RETURN AUTHORIZATION FORM_{self.sec_jira_user.take_csd_data(self.csd_var.get())[0]}.docx')
                else:
                    pass



        self.update_progress_bar(100)
        time.sleep(1)

        self.progress_bar.destroy()
        self.loading_label.destroy()

        self.pg_empty_label = customtkinter.CTkLabel(self.progress_bar_frame, text='')
        self.pg_empty_label.pack(pady=2, padx=5)

    def take_variable(self):
        print(self.en_eu_slider.get())
        print(self.combo_NoUE.get())

    def select_file(self):
        self.path = filedialog.askdirectory()
        self.save_label.destroy()
        self.save_label = customtkinter.CTkLabel(self.save_frame, text=self.path)
        self.save_label.pack(pady=5, padx=10)

    def clear_label(self):
        self.label_1.destroy()
        self.label1_1.destroy()
        self.label2_1.destroy()
        self.label3_1.destroy()
        self.label4_1.destroy()
        self.label5_1.destroy()
        self.label6_1.destroy()
        self.label7_1.destroy()

    def progress_bar_thread(self):

        self.pg_empty_label.destroy()
        self.style.configure("blue.Horizontal.TProgressbar", foreground="blue", background='black')
        self.progress_bar = tkinter.ttk.Progressbar(self.progress_bar_frame, mode="determinate", length=300, maximum=100, style="blue.Horizontal.TProgressbar")
        self.progress_bar.pack(padx=5, pady=5,side=LEFT)
        self.loading_label = customtkinter.CTkLabel(self.progress_bar_frame, text='Loading...')
        self.loading_label.pack(padx=2, pady=2,side=LEFT)

        self.t = threading.Thread(target=self.get_csd_data)
        self.t.start()

    def save_form_thread(self):

        self.pg_empty_label.destroy()
        self.style.configure("blue.Horizontal.TProgressbar", foreground="blue", background='black')
        self.progress_bar = tkinter.ttk.Progressbar(self.progress_bar_frame, mode="determinate", length=300, maximum=100, style="blue.Horizontal.TProgressbar")
        self.progress_bar.pack(padx=5, pady=5,side=LEFT)
        self.loading_label = customtkinter.CTkLabel(self.progress_bar_frame, text='Loading...')
        self.loading_label.pack(padx=2, pady=2,side=LEFT)

        self.t = threading.Thread(target=self.save_to_docx)
        self.t.start()

    def update_progress_bar(self, value):
        self.value = value
        self.progress_bar['value'] = self.value
        self.master.update()

    def slider_change(self):

        if str(self.en_eu_slider.get()) == "on":

            self.description_NoUE = customtkinter.CTkLabel(self.frame_form,text='Description:')
            self.description_NoUE.pack(side=TOP, pady=10)

            self.combo_NoUE = customtkinter.CTkComboBox(self.frame_form, values=["Electronic device: controller for building automation : iSMA-B-", "Electronic device: I/O module for building automation: iSMA-B-"])
            self.combo_NoUE.pack(side=TOP, pady=10)

        else:
            self.description_NoUE.destroy()
            self.combo_NoUE.destroy()

root = Tk()
window = Window(root)
root.mainloop()