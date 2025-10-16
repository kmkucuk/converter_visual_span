from getFilesInDir import getFilesInDir
from getTextProperties import getTextProperties
import pandas as pd
import os

parentpath = os.getcwd()
img_path = './images/stim_list'

img_list = getFilesInDir(img_path)
img_list = getTextProperties(font_files=img_list,font_sizes="24",letter_spacings="",line_spacings="")



stim_sheet = {'img_path_triagram': [], 'stimulus_triagram': [], 'position': [], 'distance': [], 'orientation': [], 'full_position': [], 'pixels_triagram': [], 'rendered_pixels_triagram':[], 'viewing_distance_triagram': [], 'logmar_triagram':[], 'vis_degree_triagram': [], 'xheight_cm_triagram': []}

for i in img_list.font_files:
    raw_name = img_list.get_font_name(i)
    print(raw_name)
    if (raw_name.find('_')):
        # triagram letters
        stimulus = raw_name[raw_name.rindex('_')-3:raw_name.rindex('_')] #print(raw_name[raw_name.rindex('_')-3:raw_name.rindex('_')])
        # position 
        position = raw_name[raw_name.rindex('_')+1:len(raw_name)] #print(raw_name[raw_name.rindex('_')+1:len(raw_name)])
        
        if int(position) == 6:
            orientation = 'center'
            distance = '0'
        elif int(position) < 6:
            orientation = 'left'
            distance = str(abs(int(position) - 6))
        elif int(position) > 6:
            orientation = 'right'
            distance = str(abs(int(position) - 6))

        full_position = ''.join([orientation, distance])

        img_path = '/'.join(['stimuli','images',raw_name])
        img_name = '.'.join([img_path, 'PNG'])
    elif (raw_name.find('-')):
        pass
    else:
        raise ValueError('File name is not acceptable: ', raw_name)
    
    stim_sheet['img_path'].append(img_name)
    stim_sheet['stimulus'].append(stimulus)
    stim_sheet['position'].append(position)
    stim_sheet['distance'].append(distance)
    stim_sheet['orientation'].append(orientation)
    stim_sheet['full_position'].append(full_position)
    stim_sheet['pixels'].append(71.45)
    stim_sheet['rendered_pixels'].append(71)
    stim_sheet['viewing_distance'].append(50)
    stim_sheet['logmar'].append(1)
    stim_sheet['vis_degree'].append(0.83)
    stim_sheet['xheight_cm'].append(0.724)


stim_df = pd.DataFrame.from_dict(stim_sheet)

os.chdir(parentpath)

stim_df.to_csv('stimulus_list.csv', index=False)