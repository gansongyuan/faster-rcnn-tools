import os
import random
import create_Annotations


def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

def chek_file(filepath, name):
    filename = os.path.join(filepath, name)
    return os.path.isfile(filename)

def create_JPEGImages(input_filepath, input_name):
    source = os.path.join(input_filepath, input_name)
    target = os.path.join(JPEGImages_path, input_name)
    os.system('cp ' + source + ' ' + target)

def create_imageset(image_file_name):
    global imageset_max
    global imageset_count

    name = image_file_name[:6]
    if imageset_max == []:
        imageset_max.append(int(images_count * percentage[0]))
        imageset_max.append(int(images_count * percentage[1]))
        imageset_max.append(int (images_count - imageset_max[0] - imageset_max[1]))

    if imageset_count[0] != imageset_max[0]:
        filname = os.path.join(ImageSets_main_path, imageset[0])
        imageset_count[0] += 1
    elif imageset_count[1] != imageset_max[1]:
        filname = os.path.join(ImageSets_main_path, imageset[1])
        trainval_filname = os.path.join(ImageSets_main_path, 'trainval.txt')
        imageset_count[1] += 1
        with open(trainval_filname, 'a+') as tranval:
            tranval.write(name + '\n')
    else:
        filname = os.path.join(ImageSets_main_path, imageset[2])
        trainval_filname = os.path.join(ImageSets_main_path, 'trainval.txt')
        imageset_count[2] += 1
        with open(trainval_filname, 'a+') as tranval:
            tranval.write(name + '\n')

    with open(filname, 'a+') as f:
        f.write(name + '\n')

lable_txt = '/home/gsy/workspace/myVOCdevkit/OK-lable'
image_path = '/home/gsy/workspace/myVOCdevkit/OK-img'
VOCdevkit = '/home/gsy/workspace/myVOCdevkit/VOC2007'
classname = 'aeroplane'
imageset   = ('test.txt', 'val.txt', 'train.txt')
percentage = (0.25,     0.25,  0.5)

imageset_max = []
imageset_count = [0,0,0]
images_count = 0

Annotations_path = VOCdevkit + '/Annotations'
ImageSets_path   = VOCdevkit + '/ImageSets'
ImageSets_main_path = ImageSets_path + '/Main'
JPEGImages_path  = VOCdevkit + '/JPEGImages'

if os.path.exists(VOCdevkit):
    os.system('rm -rf ' + VOCdevkit + '-old')
    os.system('mv ' + VOCdevkit + ' ' + VOCdevkit + '-old')
    print 'move old VOC2007 to VOC2007-old'

check_path(VOCdevkit)
check_path(Annotations_path)
check_path(ImageSets_path)
check_path(ImageSets_main_path)
check_path(JPEGImages_path)

imgs = os.listdir(image_path)

lable_file = open(lable_txt)
lines = lable_file.readlines()

images_count = lines.__len__()
random.shuffle(lines)
for index, line in enumerate(lines, start=1):
    line = line.rstrip('\n')
    array = line.split()

    if chek_file(image_path, array[0]) == False:
        print array[0] + ' is not exists, skipping'
        continue
    # generate Annotations xml
    create_Annotations.create_annotation(array, classname, image_path, Annotations_path)

    # copy to JPEGImages
    create_JPEGImages(image_path, array[0])

    # split into (train.txt test.txt trainval.txt val.txt)
    create_imageset(array[0])
    print("Rate : %.1f%%"% ((float(index) / float(images_count)) * 100 ))

print 'train :' + str(imageset_count[2]) + ' val :' + str(imageset_count[1]) + ' test :' + str(imageset_count[0])