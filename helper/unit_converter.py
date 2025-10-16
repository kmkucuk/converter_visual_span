import numpy as np
import pandas as pd
import json


### SIZE ESTIMATIONS USING SCALING COEFFICIENT DIRECTLY (Without y_scale/y_scale_init)###
# figure out getting pixel values without using screen scale ratio
#       - Using the same pixels for all images will work given:
#           - Image cm values are different for each sentence
#           - Resolution sharpness/degradation in large/small sizes are accounted for
#
# 1) get x_height in cm for every size (look up set values)
#
# 2) define image dimensions in cm using x-height
#       -  img_width = 20*x_height_cm
#       -  img_height = 12*x_height_cm
# 3) Enter cm values into dimensions, multiply them by scaling coefficients 
#       -  img_width * y_scale, img_height * y_scale

################################################
### SIZE ESTIMATIONS FROM SCREEN SCALE RATIO ###
################################################
# to get pix size in logmar=0, we need to solve following
# 1) logmar0_cm = (heightpix * height_unit * scaling_ratio) / device_pix_ratio
# above follows:
# heightpix = (logmar0_cm * device_pix_ratio) / (height_unit * scaling_ratio) 
# height_unit = txt.get_glyph_height(font_path[0],'x')
# heightpix = (logmar0_cm * device_pix_ratio) / (height_unit * scaling_ratio) 

# real height in cm for logmar=0, vis_degree=0.083, distance=40cm, size=0.05789
# real height in cm for logmar=0, vis_degree=0.083, distance=50cm, size=0.0724
# formula for pixel to cm 
# (pixel * scaling_ratio) / device_pix_ratio = logmar0_cm
# Range of LOGMAR values we'll test in MNREAD
with open("config_triagram.json", "r") as f:
    CONFIG = json.load(f)   

start=-0.2
interval = 0.1
n=12
logmar0_cm=0.0724

logmar_vals=list(np.round(np.arange(start, interval * n , interval),2))
training_vals = [2, 1.8, 1.4]
logmar_vals.reverse()
logmar_vals = training_vals + logmar_vals
vis_degree_vals=[round(0.083*(10**i),3) for i in logmar_vals]

x_height_cm_vals=[round(logmar0_cm*(i/0.083),4) for i in vis_degree_vals]
x_height_inc_vals =[round(i/2.54,3) for i in x_height_cm_vals]

pix_vals=[]
for i in x_height_cm_vals:
    if i > 0.40:
        pix_vals.append(40)
    else:
        pix_vals.append(20)

size_dict = {}
size_dict['logmar'] = logmar_vals
size_dict['vis_degree'] = vis_degree_vals
size_dict['x_height_cm'] = x_height_cm_vals
size_dict['x_height_inch'] = x_height_inc_vals
size_dict['pixels'] = pix_vals

stim_df = pd.DataFrame.from_dict(size_dict)
stim_df.to_csv(CONFIG["DATA_OUT"]+'size_properties_mnread.csv', index=False)