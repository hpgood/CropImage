# -*- encoding=utf-8 -*-

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance

import os,sys
import numpy as np

last_cropBox=[0,0,0,0]
init_ins=False

def auto_crop_image(p):

    image = Image.open(p)  # image 对象
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.take(3,axis=2)
    #image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1, :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(p )

def crop_image(p):
    global last_cropBox
    image = Image.open(p)  # image 对象
    image.load()
    image_data = np.asarray(image)
    cropBox = last_cropBox
    print("->", cropBox)
    image_data_new = image_data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1, :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(p)
def count_image(p):
    global init_ins
    global last_cropBox

    image = Image.open(p)  # image 对象
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.take(3,axis=2)
    #image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    #print(p ,"last ->", last_cropBox)
    if not init_ins:
        last_cropBox=[cropBox[0],cropBox[1],cropBox[2],cropBox[3]]
        print("not init")
        init_ins=True
    else:
        if cropBox[0]<last_cropBox[0]:
            last_cropBox[0]=cropBox[0]
        if cropBox[1]<last_cropBox[1]:
            last_cropBox[1]=cropBox[1]
        if cropBox[2]>last_cropBox[2]:
            last_cropBox[2]=cropBox[2]
        if cropBox[3]>last_cropBox[3]:
            last_cropBox[3]=cropBox[3]

    print(cropBox,"->",last_cropBox)
    #print(  last_cropBox)

def list_dir(dir, filter=None):
    list = os.listdir(dir)  # 列出目录下的所有文件和目录
    i = 1
    out = ''
    for line in list:
        #print(line,",", line.find(".png"))
        if line.find(".png")!=-1:
            count_image(dir + '/' + line)
    global last_cropBox
    print("use rect:",last_cropBox)
    for line in list:
        #print(line,",", line.find(".png"))
        if line.find(".png")!=-1:
            crop_image(dir + '/' + line)



print("__name__=",__name__)
if __name__ == "__main__":
    print("Usage:CropImage.py path")
    if len(sys.argv)== 2 :
        path = sys.argv[1]
        print("path=",path)
        list_dir(path)
