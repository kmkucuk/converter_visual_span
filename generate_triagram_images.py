from statistics import median
from PIL import Image, ImageDraw, ImageFont
from getFilesInDir import getFilesInDir
from os import chdir, makedirs, path, getcwd
import math
import pandas as pd
import json
import csv
from fontTools.ttLib import TTFont

def getGlyphHeight(font_path, character):
    """
    Get height of a character using fonttools library

    Returns a character height value, it should be multiplied by the font size (pixels)
    to get the exact pixel value of that character's height.            
    """
    font = TTFont(font_path)

    if 'glyf' in font:
        glyfTableTag = 'glyf'
    elif 'CFF ' in font:
        glyfTableTag = 'CFF'
    elif 'CFF2' in font:
        glyfTableTag = 'CFF2'
    else:            
        raise KeyError('Font file does not have a glyf table!')

    units_per_em = font['head'].unitsPerEm

    glyph_name = font.getBestCmap().get(ord(character))
    if not glyph_name:
        print(f"Character '{character}' not found in the font.")
        return None

    glyph = font[glyfTableTag][glyph_name]

    if glyph.isComposite():
        print(f"Character '{character}' is a composite glyph, height calculation may not be accurate.")
        return None

    height = (glyph.yMax - glyph.yMin) / units_per_em
    return height

def getFontName(font_path):   
    if '/' in font_path:
        font_path = font_path.replace('/', '\\')
    elif '//' in font_path:
        font_path = font_path.replace('//', '\\')

    try:
        font_path = font_path[font_path.rindex('\\')+1:font_path.rindex('.')]
        return font_path
    except (IndexError, ValueError) as err:
        raise err(f"File path either does not have a parent path or does not include a file extension: {font_path}")

def ellipseCoordinates(img_h, RENDER_PIXEL, unitw):
    radius = RENDER_PIXEL/10
    right_shift = unitw/2
    center_shift = -radius/3
    xyt=[unitw*median(POS_COOR) + right_shift + center_shift, (img_h*0.5/4) - radius]
    xyb=[unitw*median(POS_COOR) + right_shift + center_shift, (img_h*3.5/4) + radius] 
    ellipse_xy_top = (xyt[0] - radius, xyt[1] - radius, xyt[0] + radius, xyt[1] + radius)                
    ellipse_xy_bottom = (xyb[0] - radius, xyb[1] - radius, xyb[0] + radius, xyb[1] + radius)

    return ellipse_xy_top, ellipse_xy_bottom

def readTriagramCSV(csv_file='triagram_list_11-28-2024.csv'):
    triagram_list=[]
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            triagram_list.append(''.join(line))
        return triagram_list   


def drawBlankStimulus(image, ellipse_xy_top, ellipse_xy_bottom, color="red"):
    match (color):
        case "red":
            color_tuple = (0,255,0)
        case "blue":            
            color_tuple = (0, 0, 255)
        case "green":            
            color_tuple = (255, 0, 0)
        case default:
            raise ValueError(f"Incorrect color name {color}, please enter ""red"", ""blue"", or ""green""")
    draw = ImageDraw.Draw(image)    
    draw.ellipse(ellipse_xy_top, color_tuple, color_tuple, 1)
    draw.ellipse(ellipse_xy_bottom, color_tuple, color_tuple, 1)    
    return image

def saveImageFile(image, output_path, file_name):    
    pathName =  "\\".join([output_path, file_name]) + ".PNG"
    if not path.isdir(output_path):
        makedirs(output_path)
    image.save(pathName)

def main():
    with open("config_triagram.json", "r") as f:
        CONFIG = json.load(f)    
    global POS_COOR    
    RENDER_PIXEL = CONFIG["RENDER_PIXEL"]
    X_HEIGHT_CM = CONFIG["X_HEIGHT_CM"]
    X_HEIGHT_DEGREE = CONFIG["X_HEIGHT_DEGREE"]
    X_HEIGHT_LOGMAR = CONFIG["X_HEIGHT_LOGMAR"]
    POS_COOR = CONFIG["POS_COOR"]    
    
    parent_path = getcwd()
    font_dir = parent_path + "\\fonts"
    output_path = parent_path + "\\images"
    font_files = getFilesInDir(font_dir)
    multifont = True

    if multifont:

        for font_path in font_files:
            font_name = getFontName(font_path)
            triagram_list = readTriagramCSV(csv_file='triagram_list_'+ font_name + '.csv')

            x_height_unit = getGlyphHeight(font_path, 'x')
            x_height_pixel = x_height_unit * RENDER_PIXEL

            font = ImageFont.truetype(font_path, RENDER_PIXEL)
            unitw = font.getlength('x') * 1.16
            img_w = 13 * unitw
            img_h = x_height_pixel * 4

            img_x_cm = X_HEIGHT_CM * (img_w / x_height_pixel)
            img_y_cm = X_HEIGHT_CM * 4

            ellipse_xy_top, ellipse_xy_bottom = ellipseCoordinates(img_h, RENDER_PIXEL, unitw)

            POS_COOR=POS_COOR*int(len(triagram_list)/len(POS_COOR))

            STIM_SHEET = CONFIG["STIM_SHEET"]

            for pos, triagram in zip(POS_COOR, triagram_list):
                # dotted stimulus - full list # 
                image = Image.new('RGB', (math.ceil(img_w), math.ceil(img_h)), 'white')
                draw = ImageDraw.Draw(image)
                draw.ellipse(ellipse_xy_top, (0,255,0), (0,255,0), 1)
                draw.ellipse(ellipse_xy_bottom, (0,255,0), (0,255,0), 1)
                draw.text(((pos-1)*unitw, img_h/5), triagram, font=font, fill='black')
                
                stim_output = "\\".join([output_path, "stim_list", font_name])                
                raw_name = "_".join(['stim', triagram,str(pos)])              

                saveImageFile(image, stim_output, raw_name)

                if int(pos) == 6:
                    orientation = 'center'
                    distance = '0'
                elif int(pos) < 6:
                    orientation = 'left'
                    distance = str(abs(int(pos) - 6))
                elif int(pos) > 6:
                    orientation = 'right'
                    distance = str(abs(int(pos) - 6))

                full_position = ''.join([orientation, distance])

                img_path = '/'.join(['stimuli','images', font_name, raw_name])
                img_name = '.'.join([img_path, 'PNG'])
                STIM_SHEET['img_path_triagram'].append(img_name)
                STIM_SHEET['stimulus_triagram'].append(triagram)
                STIM_SHEET['position'].append(pos)
                STIM_SHEET['distance'].append(distance)
                STIM_SHEET['orientation'].append(orientation)
                STIM_SHEET['full_position'].append(full_position)
                STIM_SHEET['pixels_triagram'].append(RENDER_PIXEL)
                STIM_SHEET['rendered_pixels_triagram'].append(round(RENDER_PIXEL))
                STIM_SHEET['img_x_cm_triagram'].append(img_x_cm)
                STIM_SHEET['img_y_cm_triagram'].append(img_y_cm)
                STIM_SHEET['viewing_distance_cm'].append(50) # fixed
                STIM_SHEET['logmar_triagram'].append(X_HEIGHT_LOGMAR)
                STIM_SHEET['vis_degree_triagram'].append(X_HEIGHT_DEGREE)
                STIM_SHEET['x_height_cm_triagram'].append(X_HEIGHT_CM)
                STIM_SHEET['x_height_inch_triagram'].append(round(X_HEIGHT_CM/2.54,3)) 

            stim_df = pd.DataFrame.from_dict(STIM_SHEET)

            chdir(parent_path)

            stim_df.to_csv(CONFIG["DATA_OUT"] + 'stimulus_list_'+font_name+'.csv', index=False)

            blank_stim_colors = ["red", "green"]
            for colori in blank_stim_colors:
                image = Image.new('RGB', (math.ceil(img_w), math.ceil(img_h)), 'white')
                image = drawBlankStimulus(image=image, ellipse_xy_top=ellipse_xy_top, ellipse_xy_bottom=ellipse_xy_bottom, color=colori)     
                saveImageFile(image, output_path, "blank_"+colori)


if __name__ == '__main__':
    main()
    print("Successfuly saved all images!")