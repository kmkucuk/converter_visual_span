import random
from datetime import datetime
import csv
from os import getcwd
from getFilesInDir import getFilesInDir
import json
def getFontName(font_path):   
    if '/' in font_path:
        font_path = font_path.replace('/', '\\')
    elif '//' in font_path:
        font_path = font_path.replace('//', '\\')

    try:
        # check if there is a file extension
        font_path = font_path[font_path.rindex('\\')+1:font_path.rindex('.')]
        return font_path
    except (IndexError, ValueError) as err:
        raise err(f"File path either does not have a parent path or does not include a file extension: {font_path}")


def getFonts(font_dir):
    font_files = getFilesInDir(font_dir)
    fonts = []
    for fi in font_files:
        fonts.append(getFontName(fi))
    if len(fonts):
        return fonts
    else:
        raise FileExistsError(f"Failed to find font files in directory {font_dir}")
    
def generateTriagramCSV(list_length=550, triagram_length=3, save_format=None):
    with open("config_triagram.json", "r") as f:
        CONFIG = json.load(f)        
    alphabet = 'abcdefghjklmnopqrstuvwxyz'
    current_triagram = []
    triagram_list = []
    while len(triagram_list) < list_length:
        triagram_string = []
        current_triagram = []
        while len(current_triagram) < triagram_length:
            current_char = random.choice(alphabet)
            if current_triagram.count(current_char):
                continue
            else:
                current_triagram.append(current_char)
        triagram_string = "".join(current_triagram)
        if triagram_list.count(triagram_string):
            continue
        else:
            triagram_list.append(triagram_string)

        if save_format:
            triagram_file = CONFIG["DATA_OUT"]+'triagram_list_'+ save_format + '.csv'
        else:
            triagram_file = CONFIG["DATA_OUT"]+'triagram_list'+ datetime.today().strftime('%m-%d-%Y') + '.csv'

    with open(triagram_file, 'w', newline='') as myfile:
        print("Writing triagram list to file: {triagram_file}")
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(triagram_list)

def main():
    parent_path = getcwd()
    font_dir = parent_path + "\\fonts"
    fonts = getFonts(font_dir)
    multifont = True
    if multifont:
        for fonti in fonts:
            generateTriagramCSV(save_format=fonti)
    else:
        generateTriagramCSV()


if __name__ == '__main__':
    main()