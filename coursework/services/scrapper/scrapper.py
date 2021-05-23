# from helpers.config import task_one_output_filename
# from helpers.create_url import get_tree
# from helpers.save_xml import save_to_xml_file
# from models.link import Link
# from models.task_result_1 import TaskResult
# from xml_tree_factories.task1 import create_xml_tree_task
import requests
from lxml import html

from storage.repository import lot_repository


def get_tree(url: str):
    headers = {'Content-Type': 'text/html', }
    response = requests.get(url, headers=headers)
    html_raw = response.text

    tree = html.fromstring(html_raw)

    return tree


def get_last_page(tree):
    links = tree.xpath(
        "body/div[last()]/div[@class='article']/form/div[@class='pages']/div[@class='ArtPager']/a[contains(@href, '?page=')]/@href")
    pages = [float(sub_str.replace('?page=', '')) for sub_str in links]
    pages.sort()
    max_page = pages[-1]
    print(f'Found {max_page} pages of lots')
    return max_page


def get_lot_info(tree):
    pass


def get_lots_id_by_page(tree):
    ids = tree.xpath("//form/table/tbody/tr[contains(@class, 'data-row')]/td[1]/text()")
    return ids


def get_list_item_path(label):
    ul_path = "body/div[last()]/div[@class='article']/ul"
    il_path = f"/li/label[text()='{label}']/following-sibling::span[1]/text()"
    return f"{ul_path}{il_path}"


def get_lot_field(tree, label):
    res = tree.xpath(get_list_item_path(label))
    if len(res) > 0:
        return res[0]

    return None


def get_auction_number(tree):
    res = tree.xpath("//body/div[last()]/div[@class='top']/span[@class='title']/a/text()")
    if len(res) > 0:
        return res[0]

    return ''


class Scrapper:
    base_link = 'http://torgy.land.gov.ua/auction/lots'
    base_lot_url = 'http://torgy.land.gov.ua/auction/lot-card/'

    def __init__(self):
        self.lots_ids = []

    def parse_all_lots(self, start_page=1):
        first_page_tree = get_tree(self.base_link)
        max_parse_page = get_last_page(first_page_tree)
        curr_parse_page = start_page

        while curr_parse_page < max_parse_page:
            print(f'Page {curr_parse_page} of {max_parse_page}')
            curr_parse_page += 1
            self.parse_lots_by_page(curr_parse_page)

        print(f'Found lots: {max_parse_page * 20}')

    def parse_lots_by_page(self, page):
        page_url = f'{self.base_link}?page={page}'
        page_tree = get_tree(page_url)
        page_lots_ids = get_lots_id_by_page(page_tree)

        inserted = 0
        updated = 0

        for id in page_lots_ids:
            lot = self.parse_lot_by_id(id)
            if not lot:
                continue

            if lot_repository.insert(lot):
                inserted += 1
            else:
                updated += 1

        print(f'Inserted: {inserted}, updated: {updated}')

    def parse_lot_by_id(self, id):
        try:
            lot_url = f'{self.base_lot_url}{id}'
            lot_tree = get_tree(lot_url)
            lot_info = {
                '_id': id,
                'auction': get_auction_number(lot_tree),
                'cad_number': get_lot_field(lot_tree, 'Кадастровий номер:'),
                'place': get_lot_field(lot_tree, 'Місце розташування:'),
                'auction_date': get_lot_field(lot_tree, 'Час проведення земельних торгів:'),
                'square': float(get_lot_field(lot_tree, 'Площа земельної ділянки:')),
                'purpose': get_lot_field(lot_tree, 'Цільове призначення земельної ділянки:'),
                'evaluation': get_lot_field(lot_tree, 'НГО земельної ділянки, (грн):'),
                'register_contribution': float(get_lot_field(lot_tree, 'Розмір реєстраційного внеску:')),
                'guarantee_contribution': float(get_lot_field(lot_tree, 'Розмір гарантійного внеску:')),
            }

            start_price = get_lot_field(lot_tree,
                                              'Стартовий розмір річної плати за користування земельною ділянкою (грн):')
            if not start_price:
                lot_info['sell_price'] = float(get_lot_field(lot_tree, 'Стартова ціна продажу земельної ділянки (грн):'))
            else:
                lot_info['start_price'] = float(start_price)

            return lot_info
        except Exception as Argument:
            print(f'Failed parse of id: {id}')
            return None

# def is_continue_parse(links_list, max_links=20):
#     parsed_links = 0
#
#     for tmp_link in links_list:
#         if tmp_link.is_parsed:
#             parsed_links += 1
#
#     print(f'Totally parsed: {parsed_links}')
#     return parsed_links < max_links
#
#
# def find_first_unparsed_link(links_list):
#     for tmp_link in links_list:
#         if not tmp_link.is_parsed:
#             return tmp_link
#
#     raise Exception("Can't find links to parse!")
#
#
# def filter_for_available_links(links_list: list):
#     return list(filter(lambda link_url: link_url.startswith('https') and 'tsn.ua' in link_url, links_list))
#
#
# def fill_links_storage(links_list: list, links_store: list):
#     for link_url in links_list:
#         filename = link_url.split('/')[-1]
#         insert_floato_storage(Link(link_url, filename), links_store)
#
#
# def insert_floato_storage(link_obj: Link, storage: list):
#     for tmp_link in storage:
#         if tmp_link.url == link_obj.url:
#             return
#
#     storage.append(link_obj)
#
#
# if __name__ == '__main__':
#     links = [
#         Link('http://www.tsn.ua', 'base')
#     ]
#     results = []
#     while is_continue_parse(links, 20):
#         try:
#             link = find_first_unparsed_link(links)
#             tree = get_tree(link.url, link.filename)
#
#             available_links = filter_for_available_links(tree.xpath('//a/@href'))
#
#             unsorted_text_lines = \
#                 tree.xpath('body//*[not(self::script or self::style or self::img)]/text()')
#             text_lines = []
#             for line in unsorted_text_lines:
#                 line = line.replace('\n', ' ').strip(', \n')
#                 if len(line):
#                     text_lines.append(line)
#
#             images_url = tree.xpath('body//img/@src | body//img/@data-src')
#
#             results.append(TaskResult(link.url, text_lines, images_url))
#
#             link.set_parsed()
#             fill_links_storage(available_links, links)
#         except Exception as e:
#             print(e)
#             break
#
#         xml_tree = create_xml_tree_task(results)
#         save_to_xml_file(task_one_output_filename, xml_tree)
