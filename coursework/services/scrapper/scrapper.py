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
