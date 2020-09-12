from gui import Gui, Menu_Delete
from configuration import update_country, delete_country, update_rfi_dir, user_preference, help_document
import PySimpleGUI as sg
import os, subprocess
#import win32gui, win32con


def function_create_folder(RFI_NUM, COUNTRY, TITLE, RFI_Path):
    """
    :param RFI_NUM: int
    :param COUNTRY: str
    :param TITLE: str
    :param RFI_Path: str

    The function doesn't return any value

    Creates: - > RFI-YEAR-RFI_NUM-CC-TITLE
                  -> DOCUMENT
                  -> MXD
                  -> VECTOR
                  -> RASTER
    """
    import datetime
    import os
    from configuration import country_cc
    RFI_NUM = RFI_NUM
    cc = country_cc()[COUNTRY]
    year = datetime.datetime.now()

    flst = ['DOCUMENT', 'MXD', 'VECTOR', 'RASTER']

    rfi_fldr = 'RFI-{}-{}-{}-{}'.format(year.year, RFI_NUM, cc, TITLE)
    directory = RFI_Path
    rfi_dir_fldr = os.path.join(directory, rfi_fldr)
    os.mkdir(rfi_dir_fldr)
    for f in flst:
        os.mkdir(os.path.join(rfi_dir_fldr, f))

    sg.PopupOK(f'{rfi_fldr} was created')


def function_menu_add_window():
    """
    The function allows users to add country with their associated country code.
    :return: [Country, Country Code] = List
    """
    from gui import Menu_Add

    menu_add_window = True
    menu_add_gui = Menu_Add()
    if menu_add_window:
        eventAdd, valueAdd = menu_add_gui.window.read()
        if eventAdd in (sg.WIN_CLOSED, '-CANCEL-'):
            menu_add_gui.close_window()
            return [None, None]
        else:
            country = valueAdd['-COUNTRYNAME-']
            sg.PopupQuickMessage(f'{country} Added!' + '\n' + 'Press x to close')
            return [country, valueAdd['-COUNTRYCODE-']]


def function_menu_delete_window():
    """
    The function deletes the user specific country
    :return: Country - strn\
    """
    menu_delete_window = True
    menu_delete_gui = Menu_Delete()

    if menu_delete_window:
        event, value = menu_delete_gui.window.read()
        if event in (sg.WIN_CLOSED, '-CANCEL-'):
            menu_delete_gui.close_window()
            return None
        else:
            country = value['-DELETECOUNTRY-'][0]
            sg.PopupQuickMessage(f'{country} was removed!' + '\n' + 'Press x to close')
            return country


def function_menu_save_window():
    """
    The function allows the user to save the file path for the directory they select. That path will update in
    the config.json file.
    :return: Path - str
    """
    from gui import Menu_Save_RFI

    menu_save_window = True
    menu_save_gui = Menu_Save_RFI()

    if menu_save_window:
        event, value = menu_save_gui.window.read()
        if event in (sg.WIN_CLOSED, '-CANCEL-'):
            menu_save_gui.close_window()
            return None
        else:
            rfi_dir = value['-INPUT-']
            sg.PopupQuickMessage(f'{rfi_dir} was saved!' + '\n' + 'Press x to close')
            return rfi_dir


def function_menu_version_window():
    from configuration import directory_img, img_icon
    popup = 'Version Number: 1.0' + '\n' + 'Python Verison: 3.6' + '\n' + 'GUI: PySimpleGUI'
    sg.PopupOK(popup,title='Version',icon=os.path.join(directory_img(), img_icon()))


def function_menu_about_window():
    from configuration import directory_img, img_icon
    popup = '''The Create GEOINT RFI graphical user interface will create folder(s) and sub-folders. These folder(s) and sub-folders will help organize customer request for GEOINT operations.'''
    sg.PopupOK(popup, title='About', icon=os.path.join(directory_img(), img_icon()))


def main():
    init_gui = Gui()
    while True:
        eventM, valueM = init_gui.window.read()

        if eventM == 'Help':
            subprocess.Popen(help_document(), shell=True)
        elif eventM == 'About...':
            function_menu_about_window()
        elif eventM == 'Version':
            function_menu_version_window()
        # If user wants to Add a new Country
        elif eventM == 'Add Country':
            val_name, val_cc = function_menu_add_window()
            if val_name is not None and val_cc is not None:
                # Update JSON with Country
                update_country(val_name, val_cc)
                # Insert the country into the Listbox to show new country
                init_gui.country.insert(0, val_name)
                init_gui.window.FindElement('-ListBox-').Update(init_gui.country)

                # Add to Delete Menu GUI
                menu_delete_gui = Menu_Delete()
                menu_delete_gui.window.FindElement('-DELETECOUNTRY-').Update(init_gui.country)
                menu_delete_gui.close_window()

        # If user wants to Delete a country
        elif eventM == 'Delete Country':
            val_name = function_menu_delete_window()
            if val_name is not None:
                # Delete Country Key and Value from JSON file
                delete_country(val_name)
                # Add to Delete Menu GUI/ doesn't update from the Delete Menu GUI
                #menu_delete_gui = Menu_Delete()
                #menu_delete_gui.window.FindElement('-DELETECOUNTRY-').Update(init_gui.country)
                #menu_delete_gui.close_window()

                # Remove Country from Main GUI
                init_gui.country.remove(val_name)
                init_gui.window.FindElement('-ListBox-').Update(init_gui.country)

        # If User wants to save RFI Directory so that they don't have to set each time
        elif eventM == 'Save RFI Path':
            val_name = function_menu_save_window()
            if val_name is not None:
                # Update the RFI Directory Path so that the user
                # doesnt have to keep setting the path temporarily
                update_rfi_dir(val_name)

        # Close Main GUI if user quits
        elif eventM in (sg.WIN_CLOSED, '-QUIT-'):
            break
        else:
            # Handle when user selects create
            rfi_num = valueM['-RFI#-']
            country_fullName = valueM['-ListBox-'][0] if valueM['-ListBox-'] else None
            prod_title = valueM['-TITLE-']

            if rfi_num != '' and country_fullName is not None and prod_title != '':
                try:
                    rfi_num = int(rfi_num)
                    #print(valueM)

                    if user_preference() is None and valueM['-FolderBrowse-'] == '':
                        sg.PopupQuickMessage('Set temporary RFI path or Save RFI path')
                    elif user_preference() is not None and valueM['-FolderBrowse-'] == '':
                        directory = user_preference()
                        rfi = [f for f in os.listdir(directory) if
                               'RFI' in f and os.path.isdir(os.path.join(directory, f))]

                        if str(rfi_num) in [request.split('-')[2] for request in rfi]:
                            sg.PopupError('RFI Number Exists!')
                        else:
                            function_create_folder(rfi_num, country_fullName, prod_title, directory)
                    else:
                        directory = valueM['-FolderBrowse-']
                        rfi = [f for f in os.listdir(directory) if
                               'RFI' in f and os.path.isdir(os.path.join(directory, f))]

                        if str(rfi_num) in [request.split('-')[2] for request in rfi]:
                            sg.PopupError('RFI Number Exists!')
                        else:
                            function_create_folder(rfi_num, country_fullName, prod_title, directory)
                except ValueError:
                    sg.PopupQuickMessage('Please Enter an integer')
            else:
                if rfi_num == '':
                    sg.PopupQuickMessage('Please Enter RFI Number!')
                elif country_fullName is None:
                    sg.PopupQuickMessage('Please Select Country')
                else:
                    sg.PopupQuickMessage('Please Enter Product Title')


if __name__ == '__main__':
    # the_program_to_hide = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)
    print('Starting Application...')
    main()
