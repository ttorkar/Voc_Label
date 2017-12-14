import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


#classes = ["aeroplane", "bicycle", "bird", "boat", "bus", "car", "cat", "cow", "dog", "horse", "motorbike", "person", "sheep", "train", "drone", "tree", 'pole', 'sun', 'moon']
classes = ['bird', 'mavic', 'phantom']

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(id_):
    in_file = open('Valid_XML/%s.xml'%(id_))
    out_file = open('Valid_Labels/%s.txt'%(id_), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()



list_file = open('Valid_Images.txt', 'w')
for image_id in os.listdir('Valid_Images'):
	id_ = (image_id[:-4])
	print(id_)
	list_file.write('data/Valid_Images/%s.jpg\n'%(id_))
	convert_annotation(id_)
list_file.close()

