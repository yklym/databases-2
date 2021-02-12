from typing import List

from lxml import etree as ET

from models.task_result_1 import TaskResult


def fill_text_fragment(fragment, text_lines):
    for line in text_lines:
        text_fragment = ET.SubElement(fragment, 'text_line')
        text_fragment.text = line


def fill_img_fragment(fragment, images):
    for img in images:
        img_fragment = ET.SubElement(fragment, 'img_url')
        img_fragment.text = img


def create_xml_tree_task(results: List[TaskResult]):
    root = ET.Element('data')

    for result in results:
        page = ET.SubElement(root, 'page')
        page.set('url', result.url)

        text_fragment = ET.SubElement(page, 'fragment')
        text_fragment.set('len', str(len(result.text_lines)))
        text_fragment.set('type', 'text')
        fill_text_fragment(text_fragment, result.text_lines)

        img_fragment = ET.SubElement(page, 'fragment')
        img_fragment.set('len', str(len(result.images)))
        img_fragment.set('type', 'image')
        fill_img_fragment(img_fragment, result.images)

    tree = ET.ElementTree(root)
    return tree
