from helpers.config import task_three_target_link as base_link, task_three_output_filename
from helpers.create_url import get_tree, get_tree_by_driver
from models.good import Good
from xml_tree_factories.task3 import create_xml_tree
from helpers.save_xml import save_to_xml_file

GOODS_MAX_COUNT = 20


def parse_good(good_link) -> Good:
    good_tree = get_tree_by_driver(f'{base_link}/{good_link}')

    good_name = good_tree.xpath('//h1/text()')[0] or ''
    good_img = base_link + good_tree.xpath("//div[@class='gallery']//img/@data-src")[0] or ''
    good_price = good_tree.xpath("//span[@class='crate' and @class!='old']/text()")[0] or ''
    good_description = good_tree.xpath("//div[@class='entry']/p/text()")[0] or ''

    # print(good_name, good_img, good_price, good_description, sep='\n')
    return Good(good_name, good_img, good_price, good_description)


if __name__ == '__main__':
    goods_list = []

    page_tree = get_tree(f'{base_link}/sale')
    goods_links = page_tree.xpath("//a[@class='multy-img']/@href")[:20]

    for link in goods_links:
        goods_list.append(parse_good(link))

    xml_tree = create_xml_tree(goods_list)
    save_to_xml_file(task_three_output_filename, xml_tree)
