'''

Author: Ian McIntosh
Script: gui.py
Purpose: Classes that will be used to create the main GUI and other GUI that are called

'''

import PySimpleGUI as sg
from configuration import country_cc, directory_img, img_icon

import os


sg.ChangeLookAndFeel('DarkAmber')


class Gui:
    '''
        Create a GUI to create RFI Request folders
    '''

    def __init__(self):
        # Get the country list
        self.country = list(country_cc().keys())
        self.country.sort()

        # Set up the layout of the gui
        self.layout1= [sg.Text('RFI Number:', size=(11, 1)), sg.Input(size=(40, 1), focus=True, key='-RFI#-')]

        self.layout2 = [sg.Text('Country:', size=(11, 1)),
                        sg.Listbox(values= self.country, size=(100, 28), enable_events=False, key='-ListBox-')]

        self.layout3 = [sg.Text('Product Title:', size=(11, 1)), sg.Input(size=(40, 1), focus=False, key='-TITLE-')]

        self.layout4 = [sg.Button('Create', size=(10, 1), key='-Create-'),
                        sg.Button('Quit', size=(10, 1), key='-QUIT-'),
                        sg.FolderBrowse(button_text='Temp RFI Folder', size=(13, 1), key='-FolderBrowse-',
                                        tooltip= 'Temporary set RFI folder path')]

        self.layout5 = [sg.Menu([['&File', ['Version', '---','About...']],
                                 ['&Preference', ['Add Country', 'Delete Country', 'Save RFI Path']],
                                 ['&Help', ['Help']]])]

        self.gui_layout: list = [self.layout1, self.layout2, self.layout3, self.layout4, self.layout5]

        # Set the gui in the window
        self.window: object = sg.Window('Create GEOINT RFI Folder', self.gui_layout, element_justification='left',
                                        icon= os.path.join(directory_img(), img_icon())).Finalize()



class Menu_Add:

    def __init__(self):
        self.layout1: list = [sg.Text('Enter Country Name:', size= (len('Enter Country Name'),1)),
                             sg.Input(size=(15,1), focus=True, key='-COUNTRYNAME-')]

        self.layout2: list = [sg.Text('Enter Country Code:', size= (len('Enter Country Code'),1)),
                             sg.Input(size=(15,1), focus=False, key='-COUNTRYCODE-')]

        self.layout3: list = [sg.Button('Add', size=(10,1), key='-ADD-'),
                             sg.Button('Cancel', size=(10,1), key='-CANCEL-')]

        self.menu_add_layout: list = [self.layout1, self.layout2, self.layout3]

        self.window: object= sg.Window('Add', self.menu_add_layout, element_justification='left',
                                       icon= os.path.join(directory_img(), img_icon())).Finalize()

    def close_window(self):
        self.window.close()



class Menu_Delete:

    def __init__(self):
        # Get the country list
        self.country = list(country_cc().keys())
        self.country.sort()

        self.layout1: list = [sg.Listbox(values= self.country, size=(100, 28), enable_events=False, key='-DELETECOUNTRY-')]

        self.layout2: list = [sg.Button('Delete', size=(10, 1), key='-DELETE-'),
                              sg.Button('Cancel', size=(10, 1), key='-CANCEL-')]

        self.menu_delete_layout: list = [self.layout1, self.layout2]

        self.window: object= sg.Window('Delete', self.menu_delete_layout, element_justification='left',
                                       icon= os.path.join(directory_img(), img_icon())).Finalize()

    def close_window(self):
        self.window.close()

class Menu_Save_RFI:
    def __init__(self):
        self.layout1: list = [sg.Text('RFI Folder:', size=(8, 1)),
                              sg.Input(size=(50,1), focus=False, key='-INPUT-'),
                              sg.FolderBrowse(button_text='RFI Folder', size=(10, 1), key='-FolderBrowse-',
                                              tooltip= 'Permanently set RFI folder path'),
                              sg.Button('Set', size=(10,1), key='-SET-'),
                              sg.Button('Cancel', size=(10,1), key='-CANCEL-')]

        self.menu_save_layout: list= [self.layout1]

        self.window: object= sg.Window('Save', self.menu_save_layout, element_justification='left',
                                       icon= os.path.join(directory_img(), img_icon())).Finalize()

    def close_window(self):
        self.window.close()