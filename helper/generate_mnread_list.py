from PIL import Image, ImageDraw, ImageFont
from getFilesInDir import getFilesInDir
from os import chdir, makedirs, path, getcwd
import json
import pandas as pd

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

mnread_sentences = pd.read_csv('mnread_size_props_practice.csv', index_col=False)
resolution_multiplier=1
initial_resolution_multipler=1
resolution_ratio=1
reference_pixel=0

parent_path = getcwd()
font_dir = parent_path + "\\fonts"
font_files = getFilesInDir(font_dir)
stim_out_path = parent_path + "\\mnread_images"

font_json_dict = {}
for font_path in font_files:
    render_pixels=[]
    pixel_multiply_ratio=[]
    img_x=[]
    img_y=[]
    img_x_cm=[]
    img_y_cm=[]
    img_path=[]
    text_input_cm=[]    
    multiplier_list=[]
    mnread_sentences_temp = pd.DataFrame()
    mnread_sentences_temp = mnread_sentences
    for index, row in mnread_sentences_temp.iterrows():

        font_name = getFontName(font_path)
        multiplier_list.append(resolution_multiplier)
        render_pixel = round(row['pixels']*resolution_multiplier)
        render_pixels.append(render_pixel)
        pixel_multiply_ratio.append((row['pixels']*resolution_multiplier)/render_pixel)
        font = ImageFont.truetype(font_path, render_pixel)
        
        unitw=font.getlength('x')
        x_height_unit=txt.get_glyph_height(font_path,'x')
        x_height_pixel=x_height_unit*render_pixel
        text_input_cm.append(row['x_height_cm']/x_height_unit)

        img_w=x_height_pixel*20
        img_h=x_height_pixel*12
        img_x_cm.append(row['x_height_cm']*20)
        img_y_cm.append(row['x_height_cm']*12)

        img_x.append(img_w)
        img_y.append(img_h)
                
        yaxis= img_h/3 - render_pixel/2
        xpos=0
        charit=1

        words=row['sentence'].split(' ')
        print(words)
        line_length=0
        current_words=[]
        prev_char=' '

        image = Image.new('RGB', (math.ceil(img_w), math.ceil(img_h)), 'white')
        draw = ImageDraw.Draw(image)        

        for word in words:            
            exceptionSentence1 = (row['id_sentence']=='mnread1_s3') & (word=='the')
            exceptionSentence2 = (row['id_sentence']=='mnread1_s6') & (word=='a')
            exceptionSentence3 = (row['id_sentence']=='mnread1_s10') & (word=='a')
            exceptionSentence4 = (row['id_sentence']=='mnread1_s11') & (word=='so')
            exceptionSentence5 = (row['id_sentence']=='mnread1_s11') & (word=='play')
            exceptionSentence6 = (row['id_sentence']=='mnread_practice3') & (word=='a')
            if (exceptionSentence1):
                charLineMax=21
            elif exceptionSentence2:
                charLineMax=19
            elif exceptionSentence3:
                charLineMax=18
            elif exceptionSentence4:
                charLineMax=19
            elif exceptionSentence5:
                charLineMax=33
            elif exceptionSentence6:
                charLineMax=19
            else:
                charLineMax=20

            if ((line_length + len(word)) > charLineMax):
                current_words=[]
                line_length=0
                xpos=0
                yaxis = yaxis + render_pixel

            word = ''.join([word,' '])
            line_length+=len(word)

            prev_char=' '
            for char in word:
                unitw=font.getlength(prev_char)
                xpos=unitw+xpos        
                draw.text((xpos, yaxis), char, font=font, fill='black')
                prev_char=char

        pathName =  "/".join([stim_out_path, row['id_sentence']]) + ".PNG"
        img_path.append('/'.join(['stimuli','mnread_images',row['id_sentence']+'.PNG']))
        if not path.isdir(stim_out_path):
            makedirs(stim_out_path)

        if not stim_out_path == getcwd():
            chdir(stim_out_path)

        image.save(pathName)

    mnread_sentences_temp['text_input_cm']=text_input_cm
    mnread_sentences_temp['img_x_cm']=img_x_cm
    mnread_sentences_temp['img_y_cm']=img_y_cm
    mnread_sentences_temp['rendered_pixels']=render_pixels
    mnread_sentences_temp['multiply_ratio']=pixel_multiply_ratio
    mnread_sentences_temp['img_x']=img_x
    mnread_sentences_temp['img_y']=img_y
    mnread_sentences_temp['img_path']=img_path
    mnread_sentences_temp['resolution_multiplier']=multiplier_list

    mnread_sentences_temp.to_csv('mnread_list_render_' + font_name + '.csv',index=False)
    font_json_dict[font_name] = {'text_input_cm': text_input_cm,
                                 'img_x_cm': img_x_cm,
                                 'img_y_cm': img_y_cm,
                                 'img_x': img_x,
                                 'img_y': img_y}

    font_json_dict[font_name] = {}
    font_json_dict[font_name]['text_input_cm'] = text_input_cm
    font_json_dict[font_name]['img_x_cm'] = img_x_cm
    font_json_dict[font_name]['img_y_cm'] = img_y_cm
    font_json_dict[font_name]['rendered_pixels'] = render_pixels
    font_json_dict[font_name]['multiply_ratio']=pixel_multiply_ratio
    font_json_dict[font_name]['resolution_multiplier']=multiplier_list
   
with open("sample_practice.json", "w") as outfile:    
    json.dump(font_json_dict, outfile, indent=4)


