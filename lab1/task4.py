import lxml.etree as ET
from helpers.config import task_three_output_filename, task_four_xslt_template
from helpers.save_xml import save_to_xml_file

if __name__ == '__main__':
    dom = ET.parse(task_three_output_filename)
    xslt = ET.parse(task_four_xslt_template)
    transform = ET.XSLT(xslt)
    html_dom = transform(dom)
    save_to_xml_file('task4.html' ,html_dom )
    # print(ET.tostring(html_dom, pretty_print=True))
    # with open('task4.html', 'w') as file:
    #     file.write(html_dom)
