'''

Author: Ian McIntosh
Script: configuration.py
Purpose: Functions that will be used during the GUI and init file

'''


import json
import os


def directory_img():
    ''' Sets and gets the abspath for image directory'''
    abs_path_img = os.path.abspath('img')

    return abs_path_img


def img_icon():
    ''' sets the image icon'''

    img_file = 'logo.ico'
    return img_file


def directory_config():
    ''' Sets the congfiguration directory'''
    abs_path_json = os.path.abspath('configuration')
    return abs_path_json


def name_config():
    ''' Sets the config file name'''
    config_file = 'config.json'
    return config_file


def read_config_file():
    ''' Reads and returns json file    '''

    with open(os.path.join(directory_config(), name_config()), 'r') as json_file:
        data = json.load(json_file)

        return [data['COUNTRY'], data['User_Preference']]


def country_cc():
    return read_config_file()[0]


def user_preference():
    return read_config_file()[1]['Folder_Path']


def update_country(country_name: str, country_code: str):
    update_key_val = {country_name: country_code}
    country = read_config_file()[0]
    country.update(update_key_val)

    user_pref = read_config_file()[1]

    data = {}
    data.update({'COUNTRY': country})
    data.update({'User_Preference': user_pref})

    with open(os.path.join(directory_config(), name_config()), 'w') as out_json_file:
        json.dump(data, out_json_file)


def delete_country(country_name: str):
    country = read_config_file()[0]

    del country[country_name]
    user_pref = read_config_file()[1]

    data = {}
    data.update({'COUNTRY': country})
    data.update({'User_Preference': user_pref})

    with open(os.path.join(directory_config(), name_config()), 'w') as out_json_file:
        json.dump(data, out_json_file)


def update_rfi_dir(rfi_path: str):
    country = read_config_file()[0]
    user_pref = read_config_file()[1]
    user_pref.update({'Folder_Path': rfi_path})

    data = {}
    data.update({'COUNTRY': country})
    data.update({'User_Preference': user_pref})

    with open(os.path.join(directory_config(), name_config()), 'w') as out_json_file:
        json.dump(data, out_json_file)

def help_document():
    abs_help_doc_dir = os.path.abspath('doc')

    return os.path.join(abs_help_doc_dir, 'help.pdf')