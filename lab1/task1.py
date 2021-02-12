from helpers.config import task_one_output_filename
from helpers.create_url import get_tree
from helpers.save_xml import save_to_xml_file
from models.link import Link
from models.task_result_1 import TaskResult
from xml_tree_factories.task1 import create_xml_tree_task


def is_continue_parse(links_list, max_links=20):
    parsed_links = 0

    for tmp_link in links_list:
        if tmp_link.is_parsed:
            parsed_links += 1

    print(f'Totally parsed: {parsed_links}')
    return parsed_links < max_links


def find_first_unparsed_link(links_list):
    for tmp_link in links_list:
        if not tmp_link.is_parsed:
            return tmp_link

    raise Exception("Can't find links to parse!")


def filter_for_available_links(links_list: list):
    return list(filter(lambda link_url: link_url.startswith('https') and 'tsn.ua' in link_url, links_list))


def fill_links_storage(links_list: list, links_store: list):
    for link_url in links_list:
        filename = link_url.split('/')[-1]
        insert_into_storage(Link(link_url, filename), links_store)


def insert_into_storage(link_obj: Link, storage: list):
    for tmp_link in storage:
        if tmp_link.url == link_obj.url:
            return

    storage.append(link_obj)


if __name__ == '__main__':
    links = [
        Link('http://www.tsn.ua', 'base')
    ]
    results = []
    while is_continue_parse(links, 20):
        try:
            link = find_first_unparsed_link(links)
            tree = get_tree(link.url, link.filename)

            available_links = filter_for_available_links(tree.xpath('//a/@href'))

            unsorted_text_lines = \
                tree.xpath('body//*[not(self::script or self::style or self::img)]/text()')
            text_lines = []
            for line in unsorted_text_lines:
                line = line.replace('\n', ' ').strip(', \n')
                if len(line):
                    text_lines.append(line)

            images_url = tree.xpath('body//img/@src | body//img/@data-src')

            results.append(TaskResult(link.url, text_lines, images_url))

            link.set_parsed()
            fill_links_storage(available_links, links)
        except Exception as e:
            print(e)
            break

        xml_tree = create_xml_tree_task(results)
        save_to_xml_file(task_one_output_filename, xml_tree)
