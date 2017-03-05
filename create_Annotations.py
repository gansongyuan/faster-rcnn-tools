# -*- coding:utf-8 -*-

__author__ = "peic"

import xml.dom
import xml.dom.minidom
import os

from PIL import Image

'''
根据下面的路径和文件，将output.txt制作成xml的标注
'''

# xml文件规范定义
# _INDENT = ' ' * 4
_INDENT = '\t'
_NEW_LINE = '\n'
_FOLDER_NODE = 'VOC2007'
_ROOT_NODE = 'annotation'
_DATABASE_NAME = 'neulab'
_ANNOTATION = 'my VOC2007'
_AUTHOR = 'gsy'

_SEGMENTED = '0'
_DIFFICULT = '0'
_TRUNCATED = '0'
_POSE = 'Unspecified'

_ANNOTATION_SAVE_PATH = 'Annotations'

_IMAGE_CHANNEL = 3


# 封装创建节点的过程
def createElementNode(doc, tag, attr):
    # 创建一个元素节点
    element_node = doc.createElement(tag)

    # 创建一个文本节点
    text_node = doc.createTextNode(attr)

    # 将文本节点作为元素节点的子节点
    element_node.appendChild(text_node)
    
    return element_node


# 封装添加一个子节点的过程
def createChildNode(doc, tag, attr, parent_node):

    child_node = createElementNode(doc, tag, attr)
    parent_node.appendChild(child_node)

# object节点比较特殊
def createObjectNode(doc, attrs):
    object_node = doc.createElement('object')
    createChildNode(doc, 'name', attrs['classification'], object_node)
    createChildNode(doc, 'pose', _POSE, object_node)
    createChildNode(doc, 'truncated', _TRUNCATED, object_node)
    createChildNode(doc, 'difficult', _DIFFICULT, object_node)

    bndbox_node = doc.createElement('bndbox')
    createChildNode(doc, 'xmin', attrs['xmin'], bndbox_node)
    createChildNode(doc, 'ymin', attrs['ymin'], bndbox_node)
    createChildNode(doc, 'xmax', attrs['xmax'], bndbox_node)
    createChildNode(doc, 'ymax', attrs['ymax'], bndbox_node)
    object_node.appendChild(bndbox_node)

    return object_node

# 将documentElement写入XML文件中
def writeXMLFile(doc, filename):
    tmpfile = open('tmp.xml', 'w')
    doc.writexml(tmpfile, addindent=_INDENT, newl=_NEW_LINE, encoding='utf-8')
    tmpfile.close()

    # 删除第一行默认添加的标记
    fin = open('tmp.xml')
    fout = open(filename, 'w')
    lines = fin.readlines()

    for line in lines[1:]:
        if line.split():
            fout.writelines(line)

    fin.close()
    fout.close()

    os.remove('tmp.xml')

# 创建XML文档并写入节点信息
def createXMLFile(attrs, width, height, filename):

    # 创建文档对象, 文档对象用于创建各种节点
    my_dom = xml.dom.getDOMImplementation()
    doc = my_dom.createDocument(None, _ROOT_NODE, None)

    # 获得根节点
    root_node = doc.documentElement

    # folder节点
    createChildNode(doc, 'folder', _FOLDER_NODE, root_node)
    
    # filename节点
    createChildNode(doc, 'filename', attrs['name'], root_node)

    # source节点
    source_node = doc.createElement('source')
    # source的子节点
    createChildNode(doc, 'database', _DATABASE_NAME, source_node)
    createChildNode(doc, 'annotation', _ANNOTATION, source_node)
    createChildNode(doc, 'image', 'flickr', source_node)
    createChildNode(doc, 'flickrid', 'NULL', source_node)
    root_node.appendChild(source_node)

    # owner节点
    owner_node = doc.createElement('owner')
    # owner的子节点
    createChildNode(doc, 'flickrid', 'NULL', owner_node)
    createChildNode(doc, 'name', _AUTHOR, owner_node)
    root_node.appendChild(owner_node)

    # size节点
    size_node = doc.createElement('size')
    createChildNode(doc, 'width', str(width), size_node)
    createChildNode(doc, 'height', str(height), size_node)
    createChildNode(doc, 'depth', str(_IMAGE_CHANNEL), size_node)
    root_node.appendChild(size_node)

    # segmented节点
    createChildNode(doc, 'segmented', _SEGMENTED, root_node)

    # object节点
    object_node = createObjectNode(doc, attrs)
    root_node.appendChild(object_node)

    # 写入文件
    writeXMLFile(doc, filename)

def create_annotation(array, classname, image_path, Annotations_path):
    attrs = dict()
    attrs['name'] = array[0]
    attrs['classification'] = classname
    attrs['xmin'] = array[1]
    attrs['ymin'] = array[2]
    attrs['xmax'] = array[3]
    attrs['ymax'] = array[4]

    # 构建XML文件名称
    xml_file_name = os.path.join(Annotations_path, (attrs['name'].split('.'))[0] + '.xml')
    # print xml_file_name

    if os.path.exists( xml_file_name):
        # print('already exists')
        existed_doc = xml.dom.minidom.parse(xml_file_name)
        root_node = existed_doc.documentElement

        # 如果XML存在了, 添加object节点信息即可
        object_node = createObjectNode(existed_doc, attrs)
        root_node.appendChild(object_node)

        # 写入文件
        writeXMLFile(existed_doc, xml_file_name)

    else:
        # print('do not exists')
        # 如果XML文件不存在, 创建文件并写入节点信息
        img_name = attrs['name']
        img_path = os.path.join(image_path, img_name)
        # 获取图片信息
        img = Image.open(img_path)
        width, height = img.size
        img.close()

        # 创建XML文件
        createXMLFile(attrs, width, height, xml_file_name)