def save_to_xml_file(filename, tree):
    return tree.write(filename, pretty_print=True, xml_declaration=True, encoding="utf-8")
