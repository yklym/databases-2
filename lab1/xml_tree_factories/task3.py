from typing import List

from lxml import etree as ET

from models.good import Good


def create_xml_tree(results: List[Good]):
    root = ET.Element('data')
    i = 0

    for result in results:
        item = ET.SubElement(root, 'item')
        item.set('index', str(i))

        img = ET.SubElement(item, 'img')
        img.text = result.img

        price = ET.SubElement(item, 'price')
        price.text = result.price

        description = ET.SubElement(item, 'description')
        description.text = result.description

        name = ET.SubElement(item, 'name')
        name.text = result.name

        i += 1

    tree = ET.ElementTree(root)
    return tree
