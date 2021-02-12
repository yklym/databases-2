# Find least count of imgs
from lxml import etree

from helpers.config import task_one_output_filename

if (__name__ == "__main__"):
    with open(task_one_output_filename, 'r', encoding='utf-8') as xml_content:
        tree = etree.parse(xml_content)

        print(f"""Fragments found : {tree.xpath("count(//page/fragment[@type='image'])")}""")
        print(f"""Images found : {tree.xpath("count(//page/fragment[@type='image']/img_url)")}""")
        
        image_fragments = tree.xpath(f"//page/fragment[@type='image']")
        min_value = min(list(map(lambda fragment: fragment.xpath('count(./img_url)'), image_fragments)))
        print(f'Min images per single fragment: {min_value}')

